# Simulador_mips.py
Simulador de processador MIPS de 32 bits que permite a execução de programas em Assembly com interface gráfica em Python. Suporta operações aritméticas, lógicas, de memória e chamadas de sistema. Apresenta o estado dos registradores a cada passo e gera relatório final. Ferramenta educacional para integrar conceitos de hardware e software

## Instruções para Usar

1. **Execute o Simulador:**
   Abra o arquivo `Simulador_mips.py` e execute-o em seu ambiente Python.

2. **Abra o Arquivo de Teste:**
   Após executar o simulador, você será solicitado a abrir um arquivo com código Assembly no padrão especificado (exemplo no formato `.data` e `.text`).

3. **Execução do Código:**
   O programa será executado **passo a passo**, mostrando as linhas do código lidas e o output gerado a cada instrução.

4. **Funções Suportadas:**
   O simulador suporta as seguintes funções em Assembly:

   ### Operações Aritméticas e Lógicas:
   - `add`, `addi`, `sub`, `mul`
   - `and`, `or`, `sll`

   ### Operações de Memória:
   - `lw`, `sw`, `lui`

   ### Operações de Comparação:
   - `slt`, `slti`

   ### Chamadas de Sistema (`syscall`):
   - **Imprimir Inteiro:** `li $v0, 1`  
   - **Imprimir String:** `li $v0, 4`
   - **Sair:** `li $v0, 10`

---