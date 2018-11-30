/*

 dx/dt = a*x - b*x*y
 dy/dt = d*x*y - c*y


*/


var x float = 1.0;
var y float = 1.0;
var shift_x float;
var shift_y float;
var max float;
var n int = 1000;
var counter float;
const a = 0.66;
const b = 1.5;
const d = 1.0;
const c = 1.0;


while true {

    x += (a*x - b*x*y) * 0.01;
    y += (d*x*y - c*y) * 0.01;

    shift_x = x * 30.;
    shift_y = y * 30.;

    if (shift_x > shift_y) {max = shift_x;} else {max = shift_y;}

    counter = 0.0;

    while counter <= max {
        print ' ';

        if (counter < shift_x) && (shift_x < counter + 1.0){
            print '*';
        }

        if (counter < shift_y) && (shift_y < counter + 1.0){
            print '#';
        }

        counter += 1.0;
    }
    print '\n';

}
