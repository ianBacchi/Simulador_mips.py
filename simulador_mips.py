import sys

def main():
    # Verificar se foi passado o arquivo como argumento
    if len(sys.argv) != 2:
        print("Uso correto: python simulador_mips.py <caminho_do_arquivo>")
        sys.exit(1)

    arquivo_mips = sys.argv[1]

    # Chama a função para processar o arquivo
    processar_arquivo(arquivo_mips)

def processar_arquivo(arquivo):
    try:
        with open(arquivo, 'r') as f:
            # Lê cada linha do arquivo
            for linha in f:
                # Aqui você vai processar as instruções
                print(f"Lendo instrução: {linha.strip()}")
                # Adicione o código para interpretar e simular a instrução MIPS
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo}' não foi encontrado.")
        sys.exit(1)

if __name__ == "__main__":
    main()
