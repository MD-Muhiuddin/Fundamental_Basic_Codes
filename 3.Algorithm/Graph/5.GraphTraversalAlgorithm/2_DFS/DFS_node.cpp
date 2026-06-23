#include<bits/stdc++.h>
using namespace std;

const int WHITE = 0;
const int GRAY = 1;
const int BLACK = 2;
const int NIL = -1;
const int INF = 1e9;

struct vertex {
    int id;
    char name;
    int color;
    int d; // Discovery time
    int f; // Finish time
    int prev;
    vector<int> adj_list; 

    vertex(int _id, char _name) {
        id = _id;
        name = _name;
        color = WHITE;
        d = INF;
        f = INF;
        prev = NIL;
    }
};

// Recursive visit function
void DFS_Visit(vector<vertex>& graph, int u, int& time){
    graph[u].color = GRAY;
    time = time + 1;
    graph[u].d = time;

    for(int v : graph[u].adj_list){
        if(graph[v].color == WHITE){
            graph[v].prev = u;
            DFS_Visit(graph, v, time);
        }
    }
    
    graph[u].color = BLACK;
    time = time + 1;
    graph[u].f = time;
} 

// Main DFS function that ensures disconnected components are also visited
void DFS(vector<vertex>& graph){
    int time = 0;
    for(int u = 0; u < graph.size(); u++){
        if(graph[u].color == WHITE){
            DFS_Visit(graph, u, time);
        }
    }
}

int main(){
    int n, e;
    cin >> n >> e;

    vector<vertex> graph;
    map<char, int> name_to_id; 

    // Read the character names of all vertices
    for(int i = 0; i < n; i++) {
        char node_name;
        cin >> node_name;
        name_to_id[node_name] = i; 
        graph.push_back(vertex(i, node_name));
    }
    
    // Read edges using character names
    while(e--){
        char u, v;
        cin >> u >> v;
        
        int a = name_to_id[u];
        int b = name_to_id[v];
      
        graph[a].adj_list.push_back(b);
        // Note: Remove the line below if your DFS graph is directed
        graph[b].adj_list.push_back(a); 
    }
    
    // Note: Standard DFS does not take a single source node input
    // because the main DFS loop naturally iterates through all vertices.

    // Print the Adjacency List
    cout << "\n--- Graph Structure ---" << endl;
    for(int i = 0; i < n; i++) {
        cout << "vertex " << graph[i].name << " connects to: ";
        for(int neighbor : graph[i].adj_list) {
            cout << graph[neighbor].name << " ";
        }
        cout << endl;
    }

    // Execute Depth-First Search
    DFS(graph);

    // Print the DFS Results Table
    cout << "\n--- DFS Traversal Results ---" << endl;
    cout << "-----------------------------------------------------------------" << endl;
    
    cout << left << setw(10) << "vertex" << "| ";
    for(int i = 0; i < n; i++) cout << setw(4) << graph[i].name; 
    cout << endl;

    cout << left << setw(10) << "Color" << "| ";
    for(int i = 0; i < n; i++){
        if (graph[i].color == WHITE) cout << setw(4) << "W";
        else if (graph[i].color == GRAY) cout << setw(4) << "G";
        else if (graph[i].color == BLACK) cout << setw(4) << "B";
    }
    cout << endl;

    cout << left << setw(10) << "d (start)" << "| ";
    for(int i = 0; i < n; i++){
        if (graph[i].d == INF) cout << setw(4) << "inf";
        else cout << left << setw(4) << graph[i].d;
    }
    cout << endl;

    cout << left << setw(10) << "f (end)" << "| ";
    for(int i = 0; i < n; i++){
        if (graph[i].f == INF) cout << setw(4) << "inf";
        else cout << left << setw(4) << graph[i].f;
    }
    cout << endl;

    cout << left << setw(10) << "prev" << "| ";
    for(int i = 0; i < n; i++){
        if (graph[i].prev == NIL) cout << setw(4) << "nil";
        else cout << setw(4) << graph[graph[i].prev].name; 
    }
    cout << endl;
    
    cout << "-----------------------------------------------------------------" << endl;

    return 0;
}