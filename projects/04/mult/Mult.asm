// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.


@R0
D=M
@value
M=D
@sum
M=0
@R1
D=M
@stop
M=D
@i
M=1

@R2
M=0



(LOOP)
@stop
D=M
@i
D=D-M
@STOP
D;JLT

@value
D=M
@sum
M=M+D
@i
M=M+1
@LOOP
0;JMP

(STOP)
@sum
D=M
@R2
M=D

(END)
@END
0;JMP


