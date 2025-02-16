.data
	str: .asciiz "OR bit a bit entre 5 e 3:\n"
	str2: .asciiz "Resultado: \n"
.text

	main:

	la $a0, str
	li $v0, 4
	syscall

	li $a0, 5
	move $t0, $a0

	li $a0, 3
	move $t1, $a0

	or $t2, $t0, $t1  

	la $a0, str2
	li $v0, 4
	syscall

	li $v0, 1
	move $a0, $t2
	syscall

#OR bit a bit entre 5 e 3:
#Resultado: 
#7