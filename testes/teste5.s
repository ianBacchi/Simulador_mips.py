.data
	str: .asciiz "Verificando se 4 < 10:\n"
	str2: .asciiz "Resultado (1 = verdadeiro, 0 = falso): \n"
.text

	main:

	la $a0, str
	li $v0, 4
	syscall

	li $a0, 4
	move $t0, $a0

	li $a0, 10
	move $t1, $a0

	slt $t2, $t0, $t1  

	la $a0, str2
	li $v0, 4
	syscall

	li $v0, 1
	move $a0, $t2
	syscall


#Verificando se 4 < 10:
#Resultado (1 = verdadeiro, 0 = falso): 
#1