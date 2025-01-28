import tkinter as tk
from tkinter import filedialog

def select_file():
    # Abre o seletor de arquivos e retorna o caminho do arquivo selecionado.
    file_path = filedialog.askopenfilename(
        title="Select File", 
        filetypes=[("S files", "*.s"), ("Txt files", "*.txt")]
    )
    return file_path

def process_file(file_path):
    #Lê o arquivo e separa os segmentos .data e .text
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

def display_results(data_segment, text_segment, data_dict):
    
    print("Segmento .data:")
    for line in data_segment:
        print(line)
    
    print("\nSegmento .text:")
    for line in text_segment:
        print(line)

    print("\nDados processados do .data:")
    for var, value in data_dict.items():
        print(f"{var}: {value}")

def upload_profile_picture():
    
    file_path = select_file()
    if file_path:
        print("Selected File:", file_path)
        
        # Processa o arquivo
        data_segment, text_segment = process_file(file_path)
        
        # Processa o segmento .data
        data_dict = process_data_segment(data_segment)
        
        # Exibe os resultados
        display_results(data_segment, text_segment, data_dict)

# Interface gráfica
root = tk.Tk()
root.title("Assembly File Reader")

open_button = tk.Button(root, text="Open File", command=upload_profile_picture)
open_button.pack(pady=10)

root.mainloop()

