.data
	str: .asciiz "Soma de 10 e 5:\n"
	str2: .asciiz "Resultado: \n"
.text

	main:

	la $a0, str
	li $v0, 4
	syscall

	li $a0, 10
	move $t2, $a0

	li $a0, 5
	move $t1, $a0

	add $t0, $t1, $t2  

	la $a0, str2
	li $v0, 4
	syscall

	li $v0, 1
	move $a0, $t0
	syscall
