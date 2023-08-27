// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.



@8193
D=A
@stop // last screen register
M=D

(INIT)
@i
M=0
@SCREEN
D=A
@address
M=D





(KEYWORDLOOP)
@i
D=M
@stop
D=D-M
@INIT
D;JEQ

@i
M=M+1

@KBD
D=M
@PAINT
D;JNE

@CLEAN
D;JEQ

@KEYWORDLOOP
0;JMP

(PAINT)
@address
A=M
M=-1
@address
M=M+1

@KEYWORDLOOP
0;JMP

(CLEAN)
@address
A=M
M=0
@address
M=M+1

@KEYWORDLOOP
0;JMP











