.data
	valor: .word 42
	str: .asciiz "Carregando e armazenando valor na memória:\n"
	str2: .asciiz "Novo valor armazenado: \n"
.text

	main:

	la $a0, str
	li $v0, 4
	syscall

	lw $t0, valor  
	addi $t0, $t0, 1  
	sw $t0, valor  

	lw $t1, valor  

	la $a0, str2
	li $v0, 4
	syscall

	li $v0, 1
	move $a0, $t1
	syscall
