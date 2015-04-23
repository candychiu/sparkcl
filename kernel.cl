kernel void ArraySum(__global int *A,__global int *B){
	int i = get_global_id(0);
	int isPrime=1;
	float sq_num = sqrt((float)A[i]);
	if(A[i]>2){
		for(int j=2;j<=sq_num;j++){
			if(A[i]%j==0){
				isPrime=0;
				break;
			}
		}
	}
	if(isPrime==0 || A[i]==1)
		B[i]=0;
	else
		B[i]=A[i];
}