.data
	str: .asciiz "Multiplicação de 7 por 2 usando shift left:\n"
	str2: .asciiz "Resultado: \n"
.text

	main:

	la $a0, str
	li $v0, 4
	syscall

	li $a0, 7
	move $t0, $a0

	sll $t1, $t0, 1  

	la $a0, str2
	li $v0, 4
	syscall

	li $v0, 1
	move $a0, $t1
	syscall


#Multiplicação de 7 por 2 usando shift left:
#Resultado: 
#14