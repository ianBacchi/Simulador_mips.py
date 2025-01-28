import tkinter as tk
from tkinter import filedialog

def upload_profile_picture():
    # Abre o seletor de arquivos com filtros corrigidos
    file_path = filedialog.askopenfilename(
        title="Select File", 
        filetypes=[("S files", "*.s"), ("Txt files", "*.txt")]
    )
    if file_path:
        print("Selected File:", file_path)
        
        try:
            # Abre o arquivo para leitura
            with open(file_path, 'r') as file:
                data_segment = []  # Armazena linhas do segmento .data
                text_segment = []  # Armazena linhas do segmento .text
                current_segment = None  # Controla o segmento atual

                # Lê o arquivo linha por linha
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
                
                # Exibe os segmentos separados
                print("Segmento .data:", data_segment)
                print("Segmento .text:", text_segment)

        except Exception as e:
            print("Erro ao processar o arquivo:", e)

# Interface gráfica
root = tk.Tk()
root.title("Assembly File Reader")

open_button = tk.Button(root, text="Open File", command=upload_profile_picture)
open_button.pack(pady=10)

root.mainloop()
