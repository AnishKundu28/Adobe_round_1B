# Adobe_round_1B



Persona-Driven Document Intelligence Analyst
This project is an intelligent document analysis system built for the "Connect What Matters — For the User Who Matters" challenge. It processes a collection of PDF documents, understands a user's specific role (Persona) and goal (Job-to-be-Done), and then extracts, ranks, and summarizes the most relevant sections from the documents.

The entire system is containerized with Docker for easy, dependency-free execution and is designed to run completely offline, meeting all challenge constraints.

Features
Semantic Section Ranking: Uses sentence-transformer models (all-MiniLM-L6-v2) to understand the meaning of document sections and rank them based on their relevance to the user's query.

Persona-Based Analysis: The analysis is tailored to the user's specific role and task, ensuring the extracted information is highly relevant.

Extractive Summarization: Generates concise summaries of the most important sections to provide quick insights.

Intelligent PDF Parsing: Extracts structured content (headings and corresponding text) from PDFs.

Offline & Containerized: Fully containerized with Docker, with all models pre-loaded to run without any internet connection.

Project Structure
The project is organized as follows:

/Adobe/
├── input/
│   ├── config.json               # --- Configuration for persona, job, and documents
│   └── (Place your PDFs here)    # --- All input PDF files go here
│
├── output/
│   └── challenge1b_output.json   # --- The final analysis result
│
├── src/
│   ├── _init_.py
│   ├── main.py                   # --- Main execution script
│   ├── intelligence_system.py    # --- Core logic for ranking and summarization
│   └── pdf_parser.py             # --- PDF content extraction logic
│
├── Dockerfile                    # --- Instructions to build the container
│
└── requirements.txt              # --- Python dependencies
Setup and Usage
Follow these steps to set up and run the document analyst.

1. Prerequisites
Make sure you have Docker installed and running on your system.

2. Configuration
Place all the PDF documents you want to analyze directly inside the input/ folder.

Open the input/config.json file and edit it to define your use case:

persona: Describe the user's role (e.g., "Investment Analyst").

job_to_be_done: Describe the specific task (e.g., "Analyze revenue trends and R&D investments").

documents: Provide a list of the exact filenames of the PDFs you placed in the input folder.

Example config.json:

JSON

{
  "persona": "Investment Analyst",
  "job_to_be_done": "Analyze revenue trends, R&D investments, and market positioning strategies from the latest annual reports.",
  "documents": [
    "annual_report_company_a.pdf",
    "annual_report_company_b.pdf"
  ]
}
3. Build the Docker Image
Open a terminal in the project's root directory (Adobe/) and run the following command to build the Docker image. This will download all dependencies and models.

Bash

docker build -t doc-intel-challenge .
4. Run the Analysis
Execute the following command to run the analysis. This command links your local input and output folders to the container.

For Windows (PowerShell):

PowerShell

docker run --rm -v "${PWD}/input:/app/input" -v "${PWD}/output:/app/output" doc-intel-challenge
For Linux and macOS:

Bash

docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" doc-intel-challenge
The script will start, process the documents, and save the results.

5. View the Results
Once the script finishes, you can find the complete analysis in the output/challenge1b_output.json file.

Technology Stack
Language: Python 3.9

Containerization: Docker

NLP / Embeddings: sentence-transformers (all-MiniLM-L6-v2 model)

PDF Processing: PyMuPDF

Core Libraries: PyTorch, NLTK
