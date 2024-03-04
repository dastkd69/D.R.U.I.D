# Deep Research Utility and Intelligent Discovery

This project provides a comprehensive pipeline for processing scientific papers from ArXiv. The pipeline includes several steps:

## Features

- **Fetching Papers:** Fetch papers using the ArXiv API based on user-defined search terms.

- **Downloading and Parsing Papers:** Each paper is downloaded and parsed. The parsing method depends on the format of the files (e.g., PDF, HTML, LaTeX).

- **Extracting Information:** Extract entities and relationships from the content of each paper using Named Entity Recognition (NER) and Relationship Extraction techniques.

- **Summarizing Papers:** Generate a summary of each paper using a T5 model from the Hugging Face Transformers library.

- **Storing Results:** The extracted information and summary of each paper are stored in a SQLite database for further processing.

- **Creating a Knowledge Graph:** Create a knowledge graph from the extracted entities and relationships using the NetworkX library.

- **Visualizing the Knowledge Graph:** The knowledge graph is visualized using matplotlib.

## Installation

1. Clone the repository to your local machine.
2. Install the required Python packages using pip:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Open the Python file `process_papers.py`.
2. Modify the `search_terms` variable to the terms you want to search for on ArXiv.
3. Run the script:
    ```bash
    python process_papers.py
    ```

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.
