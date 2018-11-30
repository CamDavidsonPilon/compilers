3: PrintStatement(value=IntegerLiteral) type: None
3:     IntegerLiteral(value=3) type: int
4: PrintStatement(value=FloatLiteral) type: None
4:     FloatLiteral(value=3.5) type: float
5: PrintStatement(value=CharLiteral) type: None
5:     CharLiteral(value='a') type: char
; ModuleID = "module"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define void @"main"() 
{
entry:
  call void @"_print_int"(i32 3)
  ret void
}

declare void @"_print_int"(i32 %".1") 

declare void @"_print_float"(double %".1") 

declare void @"_print_byte"(i8 %".1") 

