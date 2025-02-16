.data
	str: .asciiz "Verificando se 8 < 10 usando imediato:\n"
	str2: .asciiz "Resultado (1 = verdadeiro, 0 = falso): \n"
.text

	main:

	la $a0, str
	li $v0, 4
	syscall

	li $a0, 8
	move $t0, $a0

	slti $t1, $t0, 10  

	la $a0, str2
	li $v0, 4
	syscall

	li $v0, 1
	move $a0, $t1
	syscall


#Verificando se 8 < 10 usando imediato:
#Resultado (1 = verdadeiro, 0 = falso): 
#1