__kernel void MatrixMul(__global int *A,__global int *B,__global int *C,int dim){
	int idx = get_global_id(0);
	int sum = 0;
	for(int i=0;i<dim;i++){
                sum=0;
		for(int j=0;j<dim;j++){                       
			sum += A[idx*dim + j] * B[j*dim + idx];
		}
		C[idx*dim+i] = sum;
	}
}
