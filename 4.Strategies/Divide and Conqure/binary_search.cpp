#include <iostream>
using namespace std;





int binarySearch(int arr[], int l,int h,int mid, int target) {
    if(l>h){
        cout<<"Element not found in the array."<<endl;
        return -1;
    }
    if(arr[mid] == target){
        cout<<"Element found at index : "<<mid<<endl;
        return mid;
    }
    else if(arr[mid] > target){
        return binarySearch(arr, l, mid-1, (l+mid-1)/2, target);
    }
    else{
        return binarySearch(arr, mid+1, h, (mid+1+h)/2, target);
    }
}


int main(){
    int arr[] ={31, 32, 33, 34, 35, 36, 37, 38, 39, 40};
    int n = sizeof(arr)/sizeof(arr[0]);

    cout<<"Array elements are : ";
    for(int i=0; i<n; i++){
        cout<<arr[i]<<" ";
    }
    cout<<endl;
    int target = 35;

    int result = binarySearch(arr, 0, n-1, (0+n-1)/2, target);

    return 0;
}