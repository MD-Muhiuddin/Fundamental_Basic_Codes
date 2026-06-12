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

void in_order(Node *root){
    if (root == NULL) return;

    // (1) Set Stack[0]=NULL and Top=1 and Ptr=Root
    Node* Stack[1000]; // Assuming a maximum stack depth of 1000
    Stack[0] = NULL;
    int Top = 1;
    Node* Ptr = root;

    // Wrap the logic in an outer loop to replace the need for a 'goto'
    while(true){
        
        // (2) Repeat while Ptr != NULL
        while(Ptr != NULL){
            // (a) Set Stack[Top]=Ptr and Top=Top+1
            Stack[Top] = Ptr;
            Top = Top + 1;
            // (b) Set Ptr=Ptr->Left
            Ptr = Ptr->left;
        }

        // (3) Set Ptr=Stack[Top] and Top := Top -1
        Top = Top - 1;
        Ptr = Stack[Top];

        // (4) Repeat steps 5 to 7 while Ptr != NULL
        while(Ptr != NULL){
            // (5) Process Ptr->Info
            cout << Ptr->value << " ";

            // (6) If Ptr->Right != NULL then set Ptr=Ptr->Right and go to step 2.
            if(Ptr->right != NULL){
                Ptr = Ptr->right;
                break; // This breaks the inner loop, sending control back to the top of the outer loop (Step 2)
            }

            // (7) Set Ptr=Stack[Top] and Top=Top-1
            Top = Top - 1;
            Ptr = Stack[Top];
        }

        // (8) Exit
        // If the inner loop finishes without breaking and Ptr is NULL, we hit Stack[0] and are done.
        if(Ptr == NULL){
            break;
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
    
    in_order(root);

    return 0;
}