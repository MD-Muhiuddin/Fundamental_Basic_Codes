#include<bits/stdc++.h>
using namespace std;

class Node{
    public:
    int value;
    Node* left;
    Node *right;

    Node(int value){
        this->value = value;
        this->right = NULL;
        this->left = NULL;
    }
};

void pre_order(Node *root){
    if (root == NULL) return;

    // (1) Set Stack[0]=Null and Top=1 and Ptr=Root
    Node* Stack[1000]; // Assuming a maximum stack depth of 1000
    Stack[0] = NULL;
    int Top = 1;
    Node* Ptr = root;

    // (2) Repeat steps (3) to (5) until Ptr ≠ NULL
    while(Ptr != NULL){
        // (3) Process Ptr->Info.
        cout << Ptr->value << " ";

        // (4) if Ptr->Right ≠ NULL then set Stack[Top]=Ptr->Right and Top=Top+1
        if(Ptr->right != NULL){
            Stack[Top] = Ptr->right;
            Top = Top + 1;
        }

        // (5) If Ptr->Left ≠ NULL then set Ptr=Ptr->Left
        // else Set Ptr=Stack[Top] and Top=Top-1
        if(Ptr->left != NULL){
            Ptr = Ptr->left;
        } else {
            Top = Top - 1;       // Decrement Top first to access the correct current index
            Ptr = Stack[Top];    // Pop the element
        }
    }
}

int main(){
    Node *root = new Node(10);
    Node *a = new Node(20);
    Node *b = new Node(30);
    Node *c = new Node(40);
    Node *d = new Node(50);
    Node *e = new Node(60);
    Node *f = new Node(70);
    Node *g = new Node(80);
    Node *h = new Node(90);
    Node *i = new Node(100);
    
    root->left = a;
    root->right = b;

    a->left = c;
    a->right = h;

    b->right = d;

    c->right = e;

    h->right = i;
    
    d->left = f;
    d->right = g;
    
    pre_order(root);

    return 0;
}