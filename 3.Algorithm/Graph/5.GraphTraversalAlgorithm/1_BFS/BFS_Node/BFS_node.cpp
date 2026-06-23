#include<bits/stdc++.h>
using namespace std;

const int WHITE = 0;
const int GRAY = 1;
const int BLACK = 2;
const int NuL = -1;
const int INF = 1e9;


struct vertex {
    int id;
    int color;
    int d;
    int prev;
    vector<int> adj_list; 

    
    vertex(int _id) {
        id = _id;
        color = WHITE;
        d = INF;
        prev = NuL;
    }
};

void bfs(vector<vertex>& graph, int src){
    queue<int> q;

    graph[src].color = GRAY;
    graph[src].d = 0;
    
    q.push(src);

    while(!q.empty()){
        int u = q.front();
        q.pop();

        for(int child_id : graph[u].adj_list){
            if(graph[child_id].color == WHITE){
                graph[child_id].color = GRAY;
                graph[child_id].d = graph[u].d + 1;
                graph[child_id].prev = u;
                q.push(child_id);
            }
        }
        graph[u].color = BLACK;
    }
} 

int main(){
    int n, e;
    cin >> n >> e;

    vector<vertex> graph;
    for(int i = 0; i < n; i++) {
        graph.push_back(vertex(i));
    }
    
    while(e--){
        int a, b;
        cin >> a >> b;
      
        graph[a].adj_list.push_back(b);
        graph[b].adj_list.push_back(a);
    }

    
    
    int src;
    cin >> src;

    // Print the Adjacency List
    cout << "\n--- Graph Structure ---" << endl;
    for(int i = 0; i < n; i++) {
        cout << "vertex " << graph[i].id << " connects to: ";
        for(int neighbor : graph[i].adj_list) {
            cout << neighbor << " ";
        }
        cout << endl;
    }

    bfs(graph, src);

    // Print the BFS Results Table
    cout << "\n--- BFS Traversal Results ---" << endl;
    cout << left << setw(10) << "vertex" << "| ";
    for(int i = 0; i < n; i++) cout << setw(4) << graph[i].id; 
    cout << endl;

    cout << left << setw(10) << "Color" << "| ";
    for(int i = 0; i < n; i++){
        if (graph[i].color == WHITE) cout << setw(4) << "W";
        else if (graph[i].color == GRAY) cout << setw(4) << "G";
        else if (graph[i].color == BLACK) cout << setw(4) << "B";
    }
    cout << endl;

    cout << left << setw(10) << "d" << "| ";
    for(int i = 0; i < n; i++){
        if (graph[i].d == INF) cout << setw(4) << "inf";
        else cout << left << setw(4) << graph[i].d;
    }
    cout << endl;

    cout << left << setw(10) << "prev" << "| ";
    for(int i = 0; i < n; i++){
        if (graph[i].prev == NuL) cout << setw(4) << "nil";
        else cout << setw(4) << graph[i].prev;
    }
    cout << endl;

    return 0;
}