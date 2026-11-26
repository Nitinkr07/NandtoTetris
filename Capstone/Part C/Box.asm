// Box.asm for K = 41
// Draws a 32x20 pixel (2 words wide x 20 rows tall) black box starting at Row 41
// Starting Screen Address = SCREEN (16384) + 32 * 41 = 17696

(LOOP)
    // Read keyboard status
    @KBD
    D=M
    @SET_BLACK
    D;JNE           // If any key is pressed (KBD != 0), set color to black (-1)

    @color
    M=0             // Otherwise, set color to white (0)
    @DRAW_INIT
    0;JMP

(SET_BLACK)
    @color
    M=-1            // -1 in 2's complement is 1111111111111111 (all black)

(DRAW_INIT)
    @17696          // Base address for Row 41 (16384 + 32 * 41)
    D=A
    @addr
    M=D

    @20             // Height = 20 rows
    D=A
    @rows
    M=D

(ROW_LOOP)
    @rows
    D=M
    @LOOP
    D;JEQ           // If rows == 0, return to main keyboard polling loop

    // Draw Word 0 (leftmost 16 pixels of the current row)
    @color
    D=M
    @addr
    A=M
    M=D

    // Draw Word 1 (next 16 pixels of the current row -> total 32 pixels wide)
    @color
    D=M
    @addr
    A=M+1
    M=D

    // Move addr down by 1 row (+32 words)
    @32
    D=A
    @addr
    M=D+M

    // Decrement remaining row counter
    @rows
    M=M-1

    @ROW_LOOP
    0;JMP