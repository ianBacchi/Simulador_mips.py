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
    "$zero": 0, "$at": 0, "$v0": 0, "$v1": 0, "$a0": 0, "$a1": 0,
    "$a2": 0, "$a3": 0, "$t0": 0, "$t1": 0, "$t2": 0, "$t3": 0,
    "$t4": 0, "$t5": 0, "$t6": 0, "$t7": 0, "$s0": 0, "$s1": 0,
    "$s2": 0, "$s3": 0, "$s4": 0, "$s5": 0, "$s6": 0, "$s7": 0,
    "$t8": 0, "$t9": 0, "$k0": 0, "$k1": 0, "$gp": 0, "$sp": 0,
    "$fp": 0, "$ra": 0
}

def selecionar_arquivo():
    """Abre um seletor de arquivos e retorna o caminho do arquivo escolhido."""
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecionar Arquivo", filetypes=[("Arquivos Assembly", ".s"), ("Arquivos de Texto", ".txt")]
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

def sair():
    print("Programa encerrado")

def simulate_mips(instrucao, registradores, dados):
    memory = dados
    output = []
    
    if not instrucao:
        return ""
    instrucao = instrucao.split()
    instr = instrucao[0]
    
    if instr == "li":
        registradorUsado = instrucao[1].replace(",", "")
        registradores[registradorUsado] = int(instrucao[2])
    elif instr == "move":
        registrador1 = instrucao[1].replace(",", "")
        registrador2 = instrucao[2]
        registradores[registrador1] = registradores[registrador2]
    elif instr == "add":
        registradorDestino = instrucao[1].replace(",", "")
        registradorSoma1 = instrucao[2].replace(",", "")
        registradorSoma2 = instrucao[3]
        registradores[registradorDestino] = registradores[registradorSoma1] + registradores[registradorSoma2]
    elif instr == "syscall":
        if registradores["$v0"] == 1:
            output.append(str(registradores["$a0"]))
        elif registradores["$v0"] == 10:
            sair()
    
    return "Executando: " + " ".join(instrucao) + "\n", output

def processar_segmento_dados(segmento_dados):
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

def executar_instrucao():
    if segmento_texto:
        instrucao = segmento_texto.pop(0)
        resultado, output = simulate_mips(instrucao, REGISTRADORES, dados)
        atualizar_interface(resultado, output)

def iniciar_processamento():
    global segmento_texto, dados
    caminho_arquivo = selecionar_arquivo()
    if caminho_arquivo:
        segmento_dados, segmento_texto = ler_arquivo(caminho_arquivo)
        dados = processar_segmento_dados(segmento_dados)
        atualizar_interface("Arquivo carregado\n", [])

def atualizar_interface(mensagem, output):
    terminal_text.delete("1.0", tk.END)
    terminal_text.insert(tk.END, mensagem)
    for reg, val in REGISTRADORES.items():
        terminal_text.insert(tk.END, f"{reg}: {val}\n")
    
    if output:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "\n".join(output))

janela = tk.Tk()
janela.title("Leitor de Arquivo Assembly")

botao_abrir = tk.Button(janela, text="Abrir Arquivo", command=iniciar_processamento)
botao_abrir.pack(pady=10)

terminal_text = tk.Text(janela, height=20, width=50)
terminal_text.pack()

output_label = tk.Label(janela, text="Output:")
output_label.pack()
output_text = tk.Text(janela, height=5, width=50)
output_text.pack()

botao_executar = tk.Button(janela, text="Executar Instrução", command=executar_instrucao)
botao_executar.pack(pady=10)

janela.mainloop()