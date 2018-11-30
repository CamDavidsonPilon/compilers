/* mandel.g */
const xmin = -2.0;
const xmax = 1.0;
const ymin = -1.5;
const ymax = 1.5;
const width = 320.0;
const height = 160.0;
const threshhold = 1000;
var dx float = (xmax - xmin)/width;
var dy float = (ymax - ymin)/height;
var y float = ymax;
var x float;
var n int;
var _x float;
var _y float;
var xtemp float;
while y >= ymin {
    x = xmin;
    while x < xmax {
       _x = 0.0;
       _y = 0.0;
       n = threshhold;
       while n > 0 {
           xtemp = _x*_x - _y*_y + x;
           _y = 2.0*_x*_y + y;
           _x = xtemp;
           n = n - 1;
           if _x*_x + _y*_y > 4.0 {
              print '.';
              n = -1;
           }
       }
       if n == 0 {
            print '*';
       }
       x = x + dx;
    }
    print '\n';
    y = y - dy;
}
