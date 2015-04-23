__kernel void MatrixSum(__global int *A,__global int *B,__global int *C,int dim){
	int idx = get_global_id(0);
	for(int i=0;i<dim;i++){
		C[idx*dim+i] = A[idx*dim+i] + B[idx*dim+i]; 
	}
}