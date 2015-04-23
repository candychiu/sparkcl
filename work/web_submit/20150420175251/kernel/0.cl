__kernel void CheckPrime(__global int *A,__global int *B){
	int i = get_global_id(0);
	int A_sqrt = sqrt(A[i]);
	int check = 1;
	for(int i=2;i<A_sqrt;i++){
		if(A[i]%i == 0)
			check = 0;
	}
	B[i] = check ;
}