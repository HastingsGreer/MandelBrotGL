__kernel void mandel(__global double* ref_real_array,
                     __global double* ref_imag_array, 
                     __global double* dc_real_array, 
                     __global double* dc_imag_array, 
                     __global int* depth_pointer,
                     __global int* count_array)
{
  unsigned int i = get_global_id(0);
  
  

  int depth = depth_pointer[0];

  double dc_real = dc_real_array[i];
  double dc_imag = dc_imag_array[i];

  int count = 0;
  double d_real = 0;
  double d_imag = 0;
  double d_real_temp;
  while((d_real + ref_real_array[count]) * (d_real + ref_real_array[count]) + 
                   (d_imag + ref_imag_array[count]) * (d_imag + ref_imag_array[count]) < 4 && 
                   count < depth){
    
    double z_real = ref_real_array[count];
    double z_imag = ref_imag_array[count];
    d_real_temp = 2 * z_real * d_real - 2 * z_imag * d_imag + d_real * d_real - d_imag * d_imag + dc_real;
    d_imag = 2 * z_real * d_imag + 2 * z_imag * d_real + 2 * d_real * d_imag + dc_imag;
    d_real = d_real_temp;
    count ++;
  }
  count_array[i] = count;
  
}
