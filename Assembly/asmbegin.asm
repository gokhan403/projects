.MODEL SMALL
.STACK 100H

; Programda kullan?lacak veriler tan?mlan?r
.DATA
MSG DB 'Enter the string : $'
STRING DB ?, '$'
STRING1 DB 'String is palindrome$'
STRING2 DB 'String is not palindrome$'

.CODE
MAIN PROC FAR

MOV AX, @data
MOV DS, AX

; Ekrana mesaj yazd?r?l?r
LEA DX, MSG
MOV AH, 9
INT 21H

; string de?i?keninin ba?lang?? adresi SI register'?nda saklan?r
; girilen harfler s?rayla, indeksler SI ile takip edilerek
; string de?i?kenine kaydedilir ve enter'a bas?ld???nda 
; okuma sonlan?r 
MOV SI, OFFSET STRING
READ :
    MOV AH, 1
    INT 21H
    CMP AL, 0DH
    JE CONTINUE
    MOV [SI], AL
    INC SI
    JMP READ
    
CONTINUE : 
   
; Girilen stringin palindrome olup olmad???n? kontrol eden fonksiyon 
CALL Palindrome

; Program? sonland?ran interrupt
MOV AH, 4CH
INT 21H
MAIN ENDP

Palindrome PROC
   
LABEL1 :
    ; DI string de?i?keninin ba?lang?? adresini (ilk indeksini) tutar
    ; SI ise ?nceden yazma i?lemi s?ras?nda son indekste bulunur
    ; yani dolar? g?sterir. Bu y?zden bir azalt?larak son indekse getirilir
    MOV DI, OFFSET STRING
    DEC SI
    
    ; SI ve DI ile sondaki ve ba?taki karakterler kar??la?t?r?l?r
    ; Sonuca g?re uygun etikete gidilir
    LOOP2 :
        CMP SI, DI
        JL OUTPUT1
        MOV AX, [SI]
        MOV BX, [DI]
        CMP AL, BL
        JNE OUTPUT2
        
    DEC SI
    INC DI
    JMP LOOP2
    
OUTPUT1 :
    ; Girdi palindrom ise ekrana string is palindrome yazd?r?l?r
    LEA DX, STRING1
    MOV AH, 9
    INT 21H
    RET
    
OUTPUT2 :
    ; Girdi palindrom de?il ise ekrana string is not palindrome yazd?r?l?r
    LEA DX, STRING2
    MOV AH, 9
    INT 21H
    RET
    
Palindrome ENDP
END MAIN
