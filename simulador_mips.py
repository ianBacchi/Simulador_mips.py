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
            with open(file_path, "+r") as file:
                
                print("Conteudo do arquivo: ")
                for line in file:
                    clean_line = line.strip()
                    print(clean_line)
        except Exception as e:
            print("Erro ao abrir arquivo", e)

# Interface gráfica
root = tk.Tk()
root.title("Assembly File Reader")

open_button = tk.Button(root, text="Open File", command=upload_profile_picture)
open_button.pack(pady=10)

root.mainloop()

