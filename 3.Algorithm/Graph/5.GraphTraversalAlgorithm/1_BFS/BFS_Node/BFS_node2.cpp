#include<bits/stdc++.h>
using namespace std;

const int WHITE = 0;
const int GRAY = 1;
const int BLACK = 2;
const int NuL = -1;
const int INF = 1e9;

struct vertex {
    int id;
    char name; // New field to hold the character
    int color;
    int d;
    int prev;
    vector<int> adj_list; 

    // Constructor updated to require a name
    vertex(int _id, char _name) {
        id = _id;
        name = _name;
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
    map<char, int> name_to_id; // Dictionary to map chars to indices

    // 1. Read the character names of all vertices first
    for(int i = 0; i < n; i++) {
        char node_name;
        cin >> node_name;
        name_to_id[node_name] = i; 
        graph.push_back(vertex(i, node_name));
    }
    
    // 2. Read edges using character names
    while(e--){
        char u, v;
        cin >> u >> v;
        
        // Convert the input characters to internal integer IDs
        int a = name_to_id[u];
        int b = name_to_id[v];
      
        graph[a].adj_list.push_back(b);
        graph[b].adj_list.push_back(a);
    }
    
    // 3. Read the source node as a character
    char src_char;
    cin >> src_char;
    int src = name_to_id[src_char];

    // Print the Adjacency List using names
    cout << "\n--- Graph Structure ---" << endl;
    for(int i = 0; i < n; i++) {
        cout << "vertex " << graph[i].name << " connects to: ";
        for(int neighbor : graph[i].adj_list) {
            cout << graph[neighbor].name << " ";
        }
        cout << endl;
    }

    bfs(graph, src);

    // Print the BFS Results Table
    cout << "\n--- BFS Traversal Results ---" << endl;
    
    // Vertex row now prints the char name
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

    cout << left << setw(10) << "d" << "| ";
    for(int i = 0; i < n; i++){
        if (graph[i].d == INF) cout << setw(4) << "inf";
        else cout << left << setw(4) << graph[i].d;
    }
    cout << endl;

    // Predecessor row converts the stored integer ID back into a character name
    cout << left << setw(10) << "prev" << "| ";
    for(int i = 0; i < n; i++){
        if (graph[i].prev == NuL) cout << setw(4) << "nil";
        else cout << setw(4) << graph[graph[i].prev].name; 
    }
    cout << endl;

    return 0;
}