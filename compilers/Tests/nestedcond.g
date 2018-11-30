/* A simple conditional */

var a int = 2;
var b int = 3;
var c int = 4;

if a < b {
     if b < c {
         print b;
     } else {
         print c;
    }
} else {
    print b;
}
