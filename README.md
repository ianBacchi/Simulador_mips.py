# Simulador_mips.py
Simulador de processador MIPS de 32 bits que permite a execução de programas em Assembly com interface gráfica em Python. Suporta operações aritméticas, lógicas, de memória e chamadas de sistema. Apresenta o estado dos registradores a cada passo e gera relatório final. Ferramenta educacional para integrar conceitos de hardware e software

#Instruções para Usar

Executar o simulador_mips.py e abrir o arquivo dentre os da pasta de teste ou algum com o mesmo padrão de formatação

O programa será executado passo a passo mostrando as linhas lidas e o output que o codigo forneceria

As funções que nosso simulador aceita são: 
    - "add", "addi", "sub", "mul", "and", "or", "sll"
    - "lw", "sw", "lui"
    - "slt", "slti"
    -syscall: 
        - imprimir Inteiro (1) 
        - imprimir String (4) 
        - sair(10) 