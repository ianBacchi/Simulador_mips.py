.data
	str: .asciiz "Carregando valor grande com LUI:\n"
	str2: .asciiz "Valor carregado: \n"
.text

	main:

	la $a0, str
	li $v0, 4
	syscall

	lui $t0, 0x1234  

	la $a0, str2
	li $v0, 4
	syscall

	li $v0, 1
	move $a0, $t0
	syscall
