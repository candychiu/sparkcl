__kernel void ArraySum(__global float *A,__global float *B,__global float *C,int dim){
       int i = get_global_id(0);
       int j = get_global_id(1);
       C[i*dim+j] = A[i*dim+j]+B[i*dim+j];
}
