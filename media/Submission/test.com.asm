org 100h
.DATA ; Data segment starts
A db 3, 1, 2 ;1-D array for number
message db 'Enter the value of N:$' ;1-D array for string
.CODE ; Code segment starts
MAIN PROC
mov ax, @DATA
mov ds, ax
xor ax,ax
mov si, OFFSET A
mov dx, OFFSET message ; similar to lea dx, message
mov ah, 09h ;display string function
int 21h ;display message
mov ah, 01h
int 21h
mov cl, al
sub cl, 48 ; convert the ascii value of 3 to decimal 3
xor al, al
Loop_1:
add al, [Si]
inc Si
loop Loop_1
mov bl, al
add bl, 48 ; convert back the decimal value back to ascii for printing
mov ah, 02h
mov dl, 0Dh
int 21h
mov dl, 0Ah
int 21h
mov dl, bl
int 21h
MAIN ENDP
END MAIN
RET

