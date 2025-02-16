.data
	str: .asciiz "Multiplicação de 6 e 3, subtraindo 4:\n"
	str2: .asciiz "Resultado: \n"
.text

	main:

	la $a0, str
	li $v0, 4
	syscall

	li $a0, 6
	move $t0, $a0

	li $a0, 3
	move $t1, $a0

	mul $t2, $t0, $t1  

	li $a0, 4
	move $t3, $a0

	sub $t4, $t2, $t3  

	la $a0, str2
	li $v0, 4
	syscall

	li $v0, 1
	move $a0, $t4
	syscall


#Multiplicação de 6 e 3, subtraindo 4:
#Resultado: 
#14