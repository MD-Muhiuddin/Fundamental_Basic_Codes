#include <iostream>
#include <vector>

using namespace std;

// The merge function combines two sorted sub-arrays into one sorted array.
void merge(int arr[], int left_Index, int mid_Indix, int right_Index) {
    int leftArraySize = mid_Indix - left_Index + 1;
    int rightArraySize = right_Index - mid_Indix;

    vector<int> leftArray(leftArraySize);
    vector<int> rightArray(rightArraySize);

    // Copy data to temporary arrays
    for (int i = 0; i < leftArraySize; i++) {
        leftArray[i] = arr[left_Index + i];
    }
    for (int j = 0; j < rightArraySize; j++) {
        rightArray[j] = arr[mid_Indix + 1 + j];
    }

    // Merge the temporary arrays back into arr[left_Index..right_Index]
    int k = left_Index; 
    int i = 0;
    int j = 0;
    
    // Sort in ascending order: smaller elements get placed first
    while(i < leftArraySize && j < rightArraySize){
        if(leftArray[i] <= rightArray[j]){
            arr[k] = leftArray[i];
            i++;
        }
        else{
            arr[k] = rightArray[j];
            j++; 
        }
        k++;
    }

    // Copy any remaining elements of leftArray
    while (i < leftArraySize) {
        arr[k++] = leftArray[i++];
    }

    // Copy any remaining elements of rightArray
    while (j < rightArraySize) {
        arr[k++] = rightArray[j++];
    }
}

// The recursive mergeSort function
void mergeSort(int arr[], int left_Index, int right_Index) {
    if (left_Index >= right_Index) {
        return; // Base case: array of size 1 is already sorted
    }

    int mid_Indix = left_Index + (right_Index - left_Index) / 2; // Prevents overflow

    // Recursively sort the first and second halves
    mergeSort(arr, left_Index, mid_Indix);
    mergeSort(arr, mid_Indix + 1, right_Index);

    // Merge the sorted halves
    merge(arr, left_Index, mid_Indix, right_Index);
}

int main() {
    int arr[] = {3, 2, 1, 4, 5};
    int n = sizeof(arr) / sizeof(arr[0]);
    
    cout << "Original Array: ";
    for(int i = 0; i < n; i++){
        cout << arr[i] << " ";
    }
    cout << endl;

    // Call the recursive mergeSort function on the entire array
    mergeSort(arr, 0, n - 1); 

    cout << "Sorted Array: ";
    for(int i = 0; i < n; i++){
        cout << arr[i] << " ";
    }
    cout << endl;

    return 0;
}