import re

def simplify_call_graph(input_file):
    output_file = "simplified_call_graph.txt"
    # Fonksiyon tanımlarını ve çağrıları bulmak için düzenli ifade
    function_def_pattern = re.compile(r'^(\w+)\(\)')
    call_pattern = re.compile(r'\s+(\w+)\(\)')

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        current_function = None
        for line in infile:
            # Fonksiyon tanımını ara
            def_match = function_def_pattern.match(line)
            if def_match:
                current_function = def_match.group(1)
                continue
            # Eğer mevcut fonksiyon varsa, çağrıları ara
            if current_function:
                call_matches = call_pattern.findall(line)
                for call in call_matches:
                    outfile.write(f"{current_function} -> {call}\n")

if __name__ == "__main__":
    input_file = input("Enter the path to the original call graph file: ")
    simplify_call_graph(input_file)