import networkx as nx
import Levenshtein
import json

def process_call_graph(callgraph_file):
    G = nx.DiGraph()
    with open(callgraph_file, 'r') as f:
        lines = f.readlines()

    stack = []
    for line in lines:
        level = len(line) - len(line.lstrip())
        func_name = line.strip().split()[0]
        while len(stack) > level:
            stack.pop()
        if stack:
            G.add_edge(stack[-1], func_name)
        stack.append(func_name)

    return G

def calculate_edit_distance(graph1, graph2):
    added_nodes = set(graph2.nodes) - set(graph1.nodes)
    removed_nodes = set(graph1.nodes) - set(graph2.nodes)

    return added_nodes, removed_nodes

def compare_call_graphs_similarity(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        content1 = f1.read()
        content2 = f2.read()

    distance = Levenshtein.distance(content1, content2)
    max_len = max(len(content1), len(content2))

    similarity_percentage = ((max_len - distance) / max_len) * 100
    return similarity_percentage

if __name__ == "__main__":
    print("CallGraph.txt files are automatically pulled from the config.json file...")
    try:
        # Read file names from config.json
        with open('config.json') as config_file:
            config = json.load(config_file)
            file1 = config["call_graphs"]["previous"]
            file2 = config["call_graphs"]["current"]

        # Process call graphs
        G1 = process_call_graph(file1)
        G2 = process_call_graph(file2)

        # Calculate edit distance
        added_nodes, removed_nodes = calculate_edit_distance(G1, G2)

        # Compare graphs similarity
        similarity_percentage = compare_call_graphs_similarity(file1, file2)
        print(f"Similarity percentage between the two call graphs: {similarity_percentage:.2f}%")

        # Number of operations
        # şu an sadece node hesabı yapılıyor, edge hesabı da yapılmalı mı hocaya sor!
        num_operations = len(added_nodes) + len(removed_nodes)
        print(f"Number of operations required to write the current callgraph.txt file from the previous callgraph.txt file: {num_operations}")

        # Added and removed nodes
        print("Added Nodes:", added_nodes)
        print("Removed Nodes:", removed_nodes)
    except FileNotFoundError:
        print("One or both of the call graph files not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
