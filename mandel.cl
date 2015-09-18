__kernel void mandel(__global double* c_real_array, 
                     __global double* c_imag_array, 
                     __global int* depth_pointer,
                     __global int* count_array)
{
  unsigned int i = get_global_id(0);
  
  
  int j = i + 1;
  int depth = depth_pointer[0];
  if(j > depth_pointer[1]){
    j = depth_pointer[1];
  }
    double c_real = c_real_array[i];
    double c_imag = c_imag_array[i];
    
    int count = 0;
    double z_real = 0;
    double z_imag = 0;
    double zreal_temp;
    while((z_real * z_real + z_imag * z_imag < 4) && count < depth){
      count ++;
      zreal_temp = z_real * z_real - z_imag * z_imag + c_real;
      z_imag = z_real * z_imag * 2 + c_imag;
      z_real = zreal_temp;
    count_array[i] = count;
  }
}
