#include <stdio.h>
#include <stdlib.h> 
int main(int argc, char *argv[]){
  int dim = 100;        /*defaults produce a nice overview of the mandelbrot set*/
  int depth = 300;
  double minx = -2;
  double maxx = 2;
  double miny = -1.5;
  double maxy = 1.5;     
  
  if(argc > 6){
      minx = atof(argv[1]);
      maxx = atof(argv[2]);
      miny = atof(argv[3]);
      maxy = atof(argv[4]);
      dim = atoi(argv[5]);
      depth = atoi(argv[6]);
  }
  
  double xstep = (maxx - minx)/dim;
  double ystep = (maxy - miny)/dim;
  
  int i, j;
  for(i = 0; i < dim; i++){
    double c_real = minx + i * xstep;
    for(j = 0; j < dim; j++){
      double c_imag = miny + j * ystep;
      int count = 0;
      double z_real = 0;
      double z_imag = 0;
      double zreal_temp;
      while((z_real * z_real + z_imag * z_imag < 4) && count < depth){
          count ++;
          zreal_temp = z_real * z_real - z_imag * z_imag + c_real;
          z_imag = z_real * z_imag * 2 + c_imag;
          z_real = zreal_temp;
      }
      printf("%d ", count);
    }   
  }
}

          
