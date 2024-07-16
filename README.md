# callGraphProc



# Call Graph Analysis from Source Code Snapshots

## Overview

This project aims to apply static analysis on successive versions of source code to extract call graphs from its snapshots. By comparing these graph models from different versions, we can calculate a set of metrics, identify vulnerabilities, and understand software evolution.

## Features

1. **GitHub Repository Fetching**: The script can clone a given GitHub repository and even checkout to a specific commit if provided.
2. **Call Graph Generation**: Using the `cflow` tool, a call graph is generated for the given source code.
3. **Graph Processing and Visualization**: The call graph is processed into a NetworkX graph model and visualized using Matplotlib.
4. **Metrics Calculation**: Basic metrics like degree centrality are calculated for the graph to provide insights into the software's structure and potential vulnerabilities.

## Dependencies

- Python 3.x
- NetworkX
- Matplotlib
- `git` (for repository cloning)
- `cflow` (for call graph generation)

## Usage

1. Clone this repository:
   ```bash
   git clone [YOUR REPOSITORY LINK]
   cd [YOUR REPOSITORY NAME]
   ```

2. Run the script:
   ```bash
   python3 main.py
   ```

## Future Improvements

1. Integrate more sophisticated metrics for graph analysis.
2. Improve visualization aesthetics and clarity.
3. Enhance vulnerability detection capabilities by mapping known vulnerabilities to call graph nodes.

