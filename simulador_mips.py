import tkinter as tk
from tkinter import filedialog
import re

# Listas de opcodes conhecidos
OPCODES_ARITMETICOS = {"add", "addi", "sub", "mul", "and", "or", "sll"}
OPCODES_MEMORIA = {"lw", "sw", "lui"}
OPCODES_CONDICIONAIS = {"slt", "slti"}

OPCODES = set.union(OPCODES_ARITMETICOS, OPCODES_CONDICIONAIS, OPCODES_MEMORIA)

# Lista de registradores MIPS
REGISTRADORES = {
    "$zero": 0, "$at": 1, "$v0": 2, "$v1": 3, "$a0": 4, "$a1": 5,
    "$a2": 6, "$a3": 7, "$t0": 8, "$t1": 9, "$t2": 10, "$t3": 11,
    "$t4": 12, "$t5": 13, "$t6": 14, "$t7": 15, "$s0": 16, "$s1": 17,
    "$s2": 18, "$s3": 19, "$s4": 20, "$s5": 21, "$s6": 22, "$s7": 23,
    "$t8": 24, "$t9": 25, "$k0": 26, "$k1": 27, "$gp": 28, "$sp": 29,
    "$fp": 30, "$ra": 31
}

def selecionar_arquivo():
    """Abre um seletor de arquivos e retorna o caminho do arquivo escolhido."""
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecionar Arquivo", filetypes=[("Arquivos Assembly", "*.s"), ("Arquivos de Texto", "*.txt")]
    )
    return caminho_arquivo

def ler_arquivo(caminho_arquivo):
    """Lê o arquivo Assembly e separa os segmentos .data e .text."""
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            segmento_dados, segmento_texto = [], []
            segmento_atual = None

            for linha in arquivo:
                linha_limpa = linha.strip()
                if not linha_limpa or linha_limpa.startswith("#"):
                    continue
                
                if "#" in linha_limpa:
                    linha_limpa = linha_limpa.split("#")[0].strip()
                
                if linha_limpa == ".data":
                    segmento_atual = "dados"
                    continue
                elif linha_limpa == ".text":
                    segmento_atual = "texto"
                    continue
                
                if segmento_atual == "dados":
                    segmento_dados.append(linha_limpa)
                elif segmento_atual == "texto":
                    segmento_texto.append(linha_limpa)

            return segmento_dados, segmento_texto
    except Exception as e:
        print("Erro ao ler o arquivo:", e)
        return [], []
    
def simulate_mips(instrucao, registradores, dados):
    print(registradores)
    memory = dados # Simula a memória para armazenar símbolos
    output = []  # Simula a saída do programa
    print(memory)
    
    if not instrucao:  # Pula linhas vazias
        return
    instrucao = instrucao.split(' ')
    instr = instrucao[0]  # Nome da instrução (ex: 'li', 'add', 'syscall')
    print(instr)
    #instrucao = [arg[0].strip(',') for arg in instrucao[1:]]  # Remove vírgulas dos argumentos
    print(instrucao)
    if instr == "li":  # Carrega um valor imediato no registrador
        registradores[instrucao[1]] = int(instrucao[1])

    elif instr == "la":  # Carrega um endereço de símbolo (simulado)
        registradorUsado = instrucao[1].replace(",", "")  
        print(registradorUsado)
        registradores[registradorUsado] = 10

    elif instr == "move":  # Move valor de um registrador para outro
        registradores[instrucao[1]] = registradores[instrucao[2]]

    elif instr == "add":  # Soma dois registradores e armazena o resultado
        registradores[instrucao[0]] = registradores[instrucao[1]] + registradores[instrucao[2]]

    elif instr == "syscall":  # Simula chamadas do sistema
        if registradores["$v0"] == 1:  # Imprimir inteiro
            output.append(str(registradores["$a0"]))
        elif registradores["$v0"] == 4:  # Imprimir string (simulada)
            output.append(f"[STRING AT] {registradores['$a0']}")
        elif registradores["$v0"] == 5:  # Ler inteiro (simulado)
            registradores["$v0"] = 10  # Exemplo fixo

    #elif instr.endswith(":"):  # Se for uma label, apenas registra
     #   memory[instr[:-1]] = len(output)
    #print(registradores)
    return output  # Retorna a saída do programa

def processar_segmento_dados(segmento_dados):
    """Processa o segmento .data e armazena as variáveis e valores."""
    dados = {}
    
    for linha in segmento_dados:
        partes = linha.split(":")
        if len(partes) < 2:
            continue
        
        nome_variavel = partes[0].strip()
        conteudo = partes[1].strip()
        
        if ".asciiz" in conteudo:
            valor = conteudo.split(".asciiz")[1].strip().strip('"')
            dados[nome_variavel] = valor
        elif ".word" in conteudo:
            valores = [int(v.strip()) for v in conteudo.split(".word")[1].strip().split(",")]
            dados[nome_variavel] = valores
    
    return dados


def processar_segmento_texto(segmento_texto, dados):
    """Processa o segmento .text e analisa os tokens."""
    texto_processado = []
    registradores = {reg: 0 for reg in REGISTRADORES.keys()}  # Inicializa registradores com 0
    
    for linha in segmento_texto:
        print("LINHA "+ linha)
        print(simulate_mips(linha, registradores, dados))
        input(' ')
        texto_processado.append(linha)
    
    return texto_processado

def exibir_resultados(segmento_dados, segmento_texto, dados, texto_processado):
    """Exibe os resultados no console."""
    print("Segmento .data:")
    for linha in segmento_dados:
        print(linha)

    print("\nSegmento .text:")
    for linha in segmento_texto:
        print(linha)
    
    print("\nDados processados do segmento .data:")
    for chave, valor in dados.items():
        print(f"{chave}: {valor}")
    
    print("\nTokens do segmento .text:")
    for tokens in texto_processado:
        print(tokens)

def iniciar_processamento():
    """Função principal que integra todas as etapas."""
    caminho_arquivo = selecionar_arquivo()
    
    if caminho_arquivo:
        print("Arquivo selecionado:", caminho_arquivo)
        segmento_dados, segmento_texto = ler_arquivo(caminho_arquivo)
        dados = processar_segmento_dados(segmento_dados)
        print(dados)
        input()
        texto_processado = processar_segmento_texto(segmento_texto, dados)
        exibir_resultados(segmento_dados, segmento_texto, dados, texto_processado)

# Interface gráfica
janela = tk.Tk()
janela.title("Leitor de Arquivo Assembly")

botao_abrir = tk.Button(janela, text="Abrir Arquivo", command=iniciar_processamento)
botao_abrir.pack(pady=10)

janela.mainloop()