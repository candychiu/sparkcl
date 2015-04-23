__kernel void Mul2(__global float *A,__global float *B){
       int i = get_global_id(0);
       B[i] = A[i]+A[i];
}
