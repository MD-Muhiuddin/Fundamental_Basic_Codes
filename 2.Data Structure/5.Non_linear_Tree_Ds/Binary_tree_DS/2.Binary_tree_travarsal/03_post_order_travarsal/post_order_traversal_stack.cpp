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

void post_order(Node *root){
    if (root == NULL) return;

    // Initialize the two stacks using your array pattern
    Node* Stack1[1000];
    int Top1 = 0;
    
    Node* Stack2[1000];
    int Top2 = 0;

    // 1. Push root to first stack.
    Stack1[Top1] = root;
    Top1 = Top1 + 1;

    // 2. Loop while first stack is not empty
    while(Top1 > 0){
        // 2.1 Pop a node from first stack and push it to second stack
        Top1 = Top1 - 1;
        Node* ptr = Stack1[Top1];
        
        Stack2[Top2] = ptr;
        Top2 = Top2 + 1;

        // 2.2 Push left and right children of the popped node to first stack
        if(ptr->left != NULL){
            Stack1[Top1] = ptr->left;
            Top1 = Top1 + 1;
        }
        if(ptr->right != NULL){
            Stack1[Top1] = ptr->right;
            Top1 = Top1 + 1;
        }
    }

    // 3. Print contents of second stack
    while(Top2 > 0){
        Top2 = Top2 - 1;
        cout << Stack2[Top2]->value << " ";
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
    
    post_order(root);

    return 0;
}