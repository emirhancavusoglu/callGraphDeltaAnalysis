import os
import subprocess
import json
import re


def generate_call_graph(repo_name):
    # Find all C files in the repo
    c_files = subprocess.check_output(["find", repo_name, "-name", "*.c"]).decode("utf-8").strip().split("\n")

    # Initialize an empty byte string to store the output
    output = b""

    # Generate the call graph for each C file
    for c_file in c_files:
        try:
            output += subprocess.check_output(["cflow", c_file])
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while processing {c_file}: {e}")

    # Write the output to a file
    if len(txt_dosyalari) == 0:
        callgraph_file = f"{repo_name}_current.txt"
        with open(callgraph_file, "wb") as f:
            f.write(output)
        return callgraph_file

    else:
        callgraph_file = f"{repo_name}_previous.txt"
        with open(callgraph_file, "wb") as f:
            f.write(output)
        return callgraph_file


# malloc, calloc, free fonksiyonlarını bulma ve sayma
def count_memory_functions(file_name):
    memory_functions = {
        'malloc': [],
        'calloc': [],
        'free': []
    }

    main_found = False
    main_line = 0
    line_number = 0

    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line_number += 1
            if 'main' in line.lower():
                main_found = True
                main_line = line_number

            if main_found:
                if 'malloc' in line:
                    distance = line_number - main_line
                    paths = find_paths_to_main(main_line, line_number, lines)
                    memory_functions['malloc'].append({'line_number': line_number, 'distance_to_main': distance})
                if 'calloc' in line:
                    distance = line_number - main_line
                    paths = find_paths_to_main(main_line, line_number, lines)
                    memory_functions['calloc'].append({'line_number': line_number, 'distance_to_main': distance})
                if 'free' in line:
                    distance = line_number - main_line
                    paths = find_paths_to_main(main_line, line_number, lines)
                    memory_functions['free'].append({'line_number': line_number, 'distance_to_main': distance})

    return memory_functions

def find_paths_to_main(main_line, target_line, lines):
    paths = []

    def backtrack(current_line, current_path):
        if current_line == main_line:
            paths.append(list(current_path))
            return
        elif current_line < main_line:
            return

        # Geriye git ve geçişler üzerinden yolları keşfet
        for i in range(current_line - 1, 0, -1):
            if lines[i - 1].strip().endswith(';') or lines[i - 1].strip().endswith('}'):
                current_path.append(i)
                backtrack(i, current_path)
                current_path.pop()

    # Başlangıç olarak, hedef satıra kadar olan yolları bul
    backtrack(target_line, [])

    # Yolları tersine çevir, çünkü yollar geriye doğru bulunuyor
    reversed_paths = [list(reversed(path)) for path in paths]

    return reversed_paths




# main ve program çıkışını temsil eden fonksiyonları bulma ve sayma
def count_entry_exit_functions(file_name):
    entry_exit_functions_count = {
        'main': 0,
        'program_exit': 0
    }

    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            function_name = re.findall(r'<(.+?)>', line)
            if function_name:
                function_name = function_name[0].lower()
                if 'main' in function_name:
                    entry_exit_functions_count['main'] += 1
                elif 'exit' in function_name or 'return' in line.lower():
                    entry_exit_functions_count['program_exit'] += 1

    return entry_exit_functions_count

# Güvenlik açığı olan fonksiyonları, main'i ve program çıkışını bulma
def find_functions_statistics(file_name):
    functions_stats = {
        'security_vulnerabilities': {}
    }

    security_vulnerable_functions = ['malloc', 'calloc', 'free']  # Güvenlik açığı olan fonksiyonlar

    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            matches = re.findall(r'<(.+?)>', line)
            if matches:
                function_name = matches[0]
                # Güvenlik açığı olan fonksiyonları ve kaç kez çağrıldıklarını say
                if function_name in functions_stats['security_vulnerabilities']:
                    functions_stats['security_vulnerabilities'][function_name] += 1
                else:
                    functions_stats['security_vulnerabilities'][function_name] = 1

                # Özel fonksiyonları kontrol et
                if function_name.lower() in security_vulnerable_functions:
                    if function_name in functions_stats['security_vulnerabilities']:
                        functions_stats['security_vulnerabilities'][function_name] += 1
                    else:
                        functions_stats['security_vulnerabilities'][function_name] = 1

    return functions_stats


if __name__ == "__main__":
    # Mevcut dizindeki .txt dosyalarını listele
    txt_dosyalari = [dosya for dosya in os.listdir() if dosya.endswith(".txt")]

    if len(txt_dosyalari) == 0:
        print("Plese enter the CURRENT repo name!")
    else:
        print("Plese enter the PREVIOUS repo name!")
    repo_name = input("Enter the repository name: ")
    callgraph_file = generate_call_graph(repo_name)
    print(f"Call graph has been generated and saved to {callgraph_file}.")


    # Mevcut dizindeki .txt dosyalarını listele
    txt_dosyalari = [dosya for dosya in os.listdir() if dosya.endswith(".txt")]

    # Mevcut dizindeki .txt dosyalarını listele
    txt_current = [ds for ds in os.listdir() if ds.endswith("_current.txt")]

    # Mevcut dizindeki .txt dosyalarını listele
    txt_previous = [ws for ws in os.listdir() if ws.endswith("_previous.txt")]

    call_graphs = {
            "previous": txt_previous[0],
            "current": txt_current[0]
    }

    # JSON dosyasına veri yazma
    with open("config.json", "w") as config_dosyasi:
        json.dump({"call_graphs": call_graphs}, config_dosyasi, indent=4)


    if len(txt_dosyalari) > 0 :
        # Dosya adlarını config.json dosyasından al
        with open('config.json', 'r') as config_file:
            data = json.load(config_file)
            current_callgraph = data['call_graphs']['current']

        functions_statistics = find_functions_statistics(current_callgraph)
        memory_functions_distance = count_memory_functions(current_callgraph)
        entry_exit_functions_count = count_entry_exit_functions(current_callgraph)

        memory_functions_data = {}
        for func_name, line_numbers in memory_functions_distance.items():
            distance = ",".join(str(x['line_number']) for x in line_numbers)
            paths = ",".join(str(x['distance_to_main']) for x in line_numbers)
            count = len(line_numbers)
            memory_functions_data[func_name] = {
                'count': count,
                'line_number': distance,
                'paths': paths #her line'ın maine uzaklığı
            }

        functions_count = {
            'memory_functions': memory_functions_data,
            'entry_exit_functions': entry_exit_functions_count,
            'func_stat': functions_statistics
        }

        with open('functions_stats.json', 'w') as json_file:
            json.dump(functions_count, json_file, indent=4)