.data	
	str: .asciiz "Recebendo primeiro numero (12)\n"
	str2: .asciiz "recebendo segundo numero (8) \n"
	str3: .asciiz "O resultado eh: \n"
.text 

	main:
	
	la $a0, str 
	li $v0, 4
	syscall
	
	li $a0, 12
	move $t2, $a0
	
	la $a0, str2 
	li $v0, 4
	syscall 
	
	li $a0, 8
	move $t1, $a0
	
	add $t0, $t1, $t2  
	
	la $a0, str3 
	li $v0, 4
	syscall
	
	li $v0, 1
	move $a0, $t0
	syscall 
