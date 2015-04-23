__kernel void CheckPrime(__global int *A,__global int *B){
	int i = get_global_id(0);
	int check = 1;
	for(int j=2;j<A[i]-1;j++){
		if(A[i]%j== 0)
			check = 0;
	}
	B[i] = check ;
}