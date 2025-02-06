import tkinter as tk
from tkinter import filedialog
import re

# Lista de opcodes conhecidos (pode ser expandida)

OPCODES_ARITIMETICOS = {"add","ADD", "addi","ADDI","SUB", "sub","MUL", "mul","AND", "and","OR", "or","SLL", "sll"}

OPCODES_MEMORIA = {"LW","lw","sw","lui", "SW", "LUI"}

OPCODE_CONDICIONAIS = {"SLT","slt","slti", "SLTI"}


# Lista de registradores MIPS (pode ser expandida)
REGISTER_INFO = {
    "$zero": (0, "constante 0"),
    "$at": (1, "reservado para o montador"),
    "$v0": (2, "avaliação de expressão e resultados de uma função"),
    "$v1": (3, "avaliação de expressão e resultados de uma função"),
    "$a0": (4, "argumento 1"),
    "$a1": (5, "argumento 2"),
    "$a2": (6, "argumento 3"),
    "$a3": (7, "argumento 4"),
    "$t0": (8, "temporário (não preservado pela chamada)"),
    "$t1": (9, "temporário (não preservado pela chamada)"),
    "$t2": (10, "temporário (não preservado pela chamada)"),
    "$t3": (11, "temporário (não preservado pela chamada)"),
    "$t4": (12, "temporário (não preservado pela chamada)"),
    "$t5": (13, "temporário (não preservado pela chamada)"),
    "$t6": (14, "temporário (não preservado pela chamada)"),
    "$t7": (15, "temporário (não preservado pela chamada)"),
    "$s0": (16, "temporário salvo"),
    "$s1": (17, "temporário salvo"),
    "$s2": (18, "temporário salvo"),
    "$s3": (19, "temporário salvo"),
    "$s4": (20, "temporário salvo"),
    "$s5": (21, "temporário salvo"),
    "$s6": (22, "temporário salvo"),
    "$s7": (23, "temporário salvo"),
    "$t8": (24, "temporário (não preservado pela chamada)"),
    "$t9": (25, "temporário (não preservado pela chamada)"),
    "$k0": (26, "reservado para o kernel do sistema operacional"),
    "$k1": (27, "reservado para o kernel do sistema operacional"),
    "$gp": (28, "ponteiro para área global"),
    "$sp": (29, "stack pointer"),
    "$fp": (30, "frame pointer"),
    "$ra": (31, "endereço de retorno (usado por chamada de função)")
}


def select_file():
    """Abre o seletor de arquivos e retorna o caminho do arquivo selecionado."""
    file_path = filedialog.askopenfilename(
        title="Select File", 
        filetypes=[("S files", "*.s"), ("Txt files", "*.txt")]
    )
    return file_path

def process_file(file_path):
    """Lê o arquivo e separa os segmentos .data e .text"""
    try:
        with open(file_path, 'r') as file:
            data_segment = []  # Armazena linhas do segmento .data
            text_segment = []  # Armazena linhas do segmento .text
            current_segment = None  # Controla o segmento atual

            for line in file:
                clean_line = line.strip()  # Remove espaços extras e quebras de linha
                if not clean_line:  # Ignora linhas vazias
                    continue
                
                # Remove comentários no final da linha
                if "#" in clean_line:
                    clean_line = clean_line.split("#")[0].strip()
                
                # Ignora linhas que ficaram vazias após remover o comentário
                if not clean_line:
                    continue
                
                # Verifica qual segmento está sendo lido
                if clean_line == ".data":
                    current_segment = "data"
                    continue
                elif clean_line == ".text":
                    current_segment = "text"
                    continue
                
                # Adiciona a linha ao segmento correspondente
                if current_segment == "data":
                    data_segment.append(clean_line)
                elif current_segment == "text":
                    text_segment.append(clean_line)

            return data_segment, text_segment

    except Exception as e:
        print("Erro ao processar o arquivo:", e)
        return [], []

def process_data_segment(data_segment):
    """Processa o segmento .data e armazena as variáveis e valores."""
    data_dict = {}
    
    for line in data_segment:
        parts = line.split(":")
        if len(parts) < 2:
            continue  # Ignora linhas inválidas

        var_name = parts[0].strip()  # Nome da variável
        content = parts[1].strip()  # Tipo e valor

        # Processa .asciiz
        if ".asciiz" in content:
            string_value = content.split(".asciiz")[1].strip().strip('"')
            data_dict[var_name] = string_value

        # Processa .word
        elif ".word" in content:
            values = content.split(".word")[1].strip().split(",")
            values = [int(v.strip()) for v in values]  # Converte para números
            data_dict[var_name] = values
    
    return data_dict

def tokenize_line(line):
    """Recebe uma linha de código assembly e retorna uma lista de tokens categorizados."""
    tokens = line.split()  # Divide a linha em palavras
    categorized_tokens = []

    for token in tokens:
        # Verifica se é um rótulo (label)
        if token.endswith(":"):
            categorized_tokens.append((token[:-1], "LABEL"))  # Remove o ':' do final
        
        # Verifica se é um opcode
        elif token in OPCODES:
            categorized_tokens.append((token, "OPCODE"))
        
        # Verifica se é um registrador (mesmo que venha como símbolo)
        elif token in REGISTERS or (token.startswith("$") and token in REGISTERS):
            categorized_tokens.append((token, "REGISTER"))
        
        # Verifica se é um número imediato (constante)
        elif re.match(r"^-?\d+$", token):  
            categorized_tokens.append((token, "IMMEDIATE"))
        
        # Se não for nenhuma das opções acima, assume que é um símbolo (nome de variável, rótulo, etc.)
        else:
            categorized_tokens.append((token, "SYMBOL"))
    
    return categorized_tokens


def process_text_segment(text_segment):
    """Processa o segmento .text e analisa os tokens de cada linha."""
    processed_text = []
    
    for line in text_segment:
        tokens = tokenize_line(line)
        processed_text.append(tokens)
    
    return processed_text

def display_results(data_segment, text_segment, data_dict, processed_text):
    """Exibe os resultados no console."""
    print("Segmento .data:")
    for line in data_segment:
        print(line)

    print("\nSegmento .text:")
    for line in text_segment:
        print(line)

    print("\nDados processados do .data:")
    for var, value in data_dict.items():
        print(f"{var}: {value}")

    print("\nTokens do segmento .text:")
    for tokens in processed_text:
        print(tokens)

def upload_profile_picture():
    """Função principal que integra todas as funções."""
    file_path = select_file()
    
    if file_path:
        print("Selected File:", file_path)
        
        # Processa o arquivo
        data_segment, text_segment = process_file(file_path)
        
        # Processa o segmento .data
        data_dict = process_data_segment(data_segment)
        
        # Processa o segmento .text
        processed_text = process_text_segment(text_segment)
        
        # Exibe os resultados
        display_results(data_segment, text_segment, data_dict, processed_text)

# Interface gráfica
root = tk.Tk()
root.title("Assembly File Reader")

open_button = tk.Button(root, text="Open File", command=upload_profile_picture)
open_button.pack(pady=10)

root.mainloop()
