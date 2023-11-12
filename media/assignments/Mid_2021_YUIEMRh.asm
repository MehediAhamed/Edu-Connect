ORG 0100H
.DATA
.CODE
MAIN PROC
    MOV AH, 1
    INT 21h
    MOV BL, AL
    INT 21h
    CMP AL, BL
    
    ;JE L3
    ;JG L2
    ;JL L1
    
    ;L1:
    ;    ADD AL,BL 
    ;    JMP ENDIF
    ;L2:
    ;    SUB AL,BL
    ;    JMP ENDIF
    ;L3:
    ;    XOR AL, BL
    ;    JMP ENDIF 
    ;ENDIF:
       
    MAIN ENDP
END MAIN
RET