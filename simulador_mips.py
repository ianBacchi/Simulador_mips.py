import tkinter as tk
from tkinter import ttk, filedialog
import re
import time
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
    

def sair():
    print("programa encerrado")

def simulate_mips(instrucao, registradores, dados):
    print(registradores)
    memoria = dados # Simula a memória para armazenar símbolos
    output = []  # Simula a saída do programa
    #print(memoria)
    
    if not instrucao:  # Pula linhas vazias
        return
    instrucao = instrucao.split(' ')
    instr = instrucao[0]  # Nome da instrução (ex: 'li', 'add', 'syscall')
    #print(instr)
    #instrucao = [arg[0].strip(',') for arg in instrucao[1:]]  # Remove vírgulas dos argumentos
    #print(instrucao)
    if instr == "li":  # Carrega um valor imediato no registrador
        registradorUsado = instrucao[1].replace(",", "")
        registradores[registradorUsado] = int(instrucao[2])

    elif instr == "la":  # Carrega um endereço de símbolo (simulado)
        registradorUsado = instrucao[1].replace(",", "")  
        registradores[registradorUsado] = instrucao[2]

    elif instr == "move":  # Move valor de um registrador para outro
        registrador1 = instrucao[1].replace(",", "")
        registrador2 = instrucao[2]
        registradores[registrador1] = registradores[registrador2]

    elif instr == "add":  # Soma dois registradores e armazena o resultado
        registradorDestino = instrucao[1].replace(",", "")
        registradorSoma1 = instrucao[2].replace(",", "")
        registradorSoma2 = instrucao[3]
        registradores[registradorDestino] = int(registradores[registradorSoma1]) + int(registradores[registradorSoma2])
    elif instr == "addi": 
        registradorDestino = instrucao[1].replace(",", "")
        registradorSoma1 = instrucao[2].replace(",", "")
        valorSoma2 = int(instrucao[3])
        registradores[registradorDestino] = int(registradores[registradorSoma1] + valorSoma2)
    elif instr == "sub":
        registradorDestino = instrucao[1].replace(",", "")
        registradorSub1 = instrucao[2].replace(",", "")
        registradorSub2 = instrucao[3]
        registradores[registradorDestino] = int(registradores[registradorSub1]) - int(registradores[registradorSub2])
    elif instr == "mult":
        registradorDestino = instrucao[1].replace(",", "")
        registradorMult1 = instrucao[2].replace(",", "")
        registradorMult2 = instrucao[3]
        registradores[registradorDestino] = int(registradores[registradorMult1]) * int(registradores[registradorMult2])
    elif instr == "sll":  # Shift Left Logical
        registradorDestino = instrucao[1].replace(",", "")
        registradorOrigem = instrucao[2].replace(",", "")
        shiftAmount = int(instrucao[3])  # Número de bits a deslocar
        registradores[registradorDestino] = registradores[registradorOrigem] << shiftAmount
    elif instr == "syscall":  # Simula chamadas do sistema
        if registradores["$v0"] == 1:  # Imprimir inteiro
            numero = registradores["$a0"]
            output = numero
        elif registradores["$v0"] == 4:  # Imprimir string 
            palavra = registradores["$a0"]
            output = memoria[palavra]
        #elif registradores["$v0"] == 5: # Le inteiro
            #input()
        elif registradores["$v0"] == 10:
            sair()  # Exemplo fixo

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
        output = simulate_mips(linha, registradores, dados)
        atualizar_interface(linha, registradores, output)
        input(" ")
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

def atualizar_interface(linha, registradores, output):
    """Atualiza a interface gráfica com os registradores e saída"""
    
    # Atualiza o terminal com a instrução atual
    terminal_text.delete("1.0", tk.END)
    terminal_text.insert(tk.END, linha)

    # Limpa e insere os valores atualizados dos registradores na tabela
    tree.delete(*tree.get_children())
    for reg, val in registradores.items():
        tree.insert("", "end", values=(reg, val))
    
    # Atualiza a saída do programa
    if output:
        #output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, str(output) + "\n")
        output_text.see(tk.END)  # Rola automaticamente para a última linha

# Criando a janela principal
janela = tk.Tk()
janela.title("Simulador MIPS")

# Configurar o grid
janela.columnconfigure(0, weight=1)
janela.columnconfigure(1, weight=2)
janela.columnconfigure(2, weight=2)

# Criando a Tabela de Registradores (Coluna 1)
tree = ttk.Treeview(janela, columns=("Registrador", "Valor"), show="headings", height=20)
tree.heading("Registrador", text="Registrador")
tree.heading("Valor", text="Valor")
tree.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)

# Criando um Frame para a linha lida (Coluna 2)
frame_linha = tk.Frame(janela)
frame_linha.grid(row=0, column=1, sticky="nsew", padx=5, pady=(5, 2))  # Reduz espaço inferior

linha_label = tk.Label(frame_linha, text="Linha Lida:", font=("Arial", 10, "bold"))
linha_label.pack(anchor="w")

terminal_text = tk.Text(janela, height=5, width=40)
terminal_text.grid(row=1, column=1, sticky="nsew", padx=5, pady=(2, 5))  # Reduz espaço superior

# Criando um Frame para o output (Coluna 3)
frame_output = tk.Frame(janela)
frame_output.grid(row=0, column=2, sticky="nsew", padx=5, pady=(5, 2))

output_label = tk.Label(frame_output, text="Output:", font=("Arial", 10, "bold"))
output_label.pack(anchor="w")

output_text = tk.Text(janela, height=5, width=40)
output_text.grid(row=1, column=2, sticky="nsew", padx=5, pady=(2, 5))

# Botão para abrir arquivo
botao_abrir = tk.Button(janela, text="Abrir Arquivo", command=lambda: iniciar_processamento())
botao_abrir.grid(row=2, column=1, columnspan=2, pady=10)

janela.mainloop()