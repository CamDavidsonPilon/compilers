/* main.c */
#include <stdio.h>

extern int hello();
extern double dsquared(double, double);
extern double distance(double, double);
extern double x;
extern void incr();

int main() {
  printf("Hello returned: %i\n", hello());
  printf("dsquared(3, 4) = %f\n", dsquared(3.0, 4.0));
  printf("distance(3, 4) = %f\n", distance(3.0, 4.0));
  printf("x is %f\n", x);
  incr();
  printf("x is now %f\n", x);
}
