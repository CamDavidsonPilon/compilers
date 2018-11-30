; ModuleID = "hello"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"hello"() 
{
entry:
  ret i32 37
}

define double @"dsquared"(double %".1", double %".2") 
{
entry:
  %".4" = fmul double %".1", %".1"
  %".5" = fmul double %".2", %".2"
  %".6" = fadd double %".4", %".5"
  ret double %".6"
}

declare double @"sqrt"(double %".1") 

define double @"distance"(double %".1", double %".2") 
{
entry:
  %".4" = call double @"dsquared"(double %".1", double %".2")
  %".5" = call double @"sqrt"(double %".4")
  ret double %".5"
}

@"x" = global double              0x0
define void @"incr"() 
{
entry:
  %".2" = load double, double* @"x"
  %".3" = fadd double %".2", 0x3ff0000000000000
  store double %".3", double* @"x"
  ret void
}

