# Adobe_round_1B


# 📘 Persona-Driven Document Intelligence Analyst

**Challenge Track:** _Connect What Matters — For the User Who Matters (Adobe India Hackathon)_

This project is an intelligent PDF analysis system that extracts, ranks, and summarizes document sections based on a user’s **persona** and **job-to-be-done**. Built for Round 1B, it runs completely **offline** and is fully **containerized with Docker** for seamless execution.

---

## 🚀 Features

- 🔍 **Semantic Section Ranking**  
  Understands and ranks sections using the `all-MiniLM-L6-v2` transformer model.

- 🧑‍💼 **Persona-Based Analysis**  
  Adapts the analysis to the user's role and specific task.

- ✂️ **Extractive Summarization**  
  Summarizes relevant document sections for quick insights.

- 📄 **PDF Parsing & Structure Extraction**  
  Intelligent extraction of headings and content using PyMuPDF.

- 🐳 **Fully Offline & Dockerized**  
  No internet required; containerized for easy setup.

---

## 📁 Project Structure

Adobe/
├── input/
│ ├── config.json # Persona, job, and file names
│ └── *.pdf # Input PDF files
├── output/
│ └── challenge1b_output.json # Final output
├── src/
│ ├── init.py
│ ├── main.py # Main entrypoint
│ ├── intelligence_system.py # Ranking and summarization logic
│ └── pdf_parser.py # PDF structure extractor
├── Dockerfile # Build instructions
└── requirements.txt # Python dependencies

yaml
Copy
Edit

---

## ⚙️ Setup & Usage

### 📌 Prerequisites

- Docker installed: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

---

### ✏️ Step 1: Prepare Input

1. Place PDF files inside the `input/` folder.
2. Edit `input/config.json` to describe your use case.

Example `config.json`:
json
{
  "persona": "Investment Analyst",
  "job_to_be_done": "Analyze revenue trends, R&D investments, and market positioning strategies from the latest annual reports.",
  "documents": [
    "annual_report_company_a.pdf",
    "annual_report_company_b.pdf"
  ]
}
🛠️ Step 2: Build Docker Image
In the Adobe/ folder:

bash
Copy
Edit
docker build -t doc-intel-challenge .
▶️ Step 3: Run the Analysis
Linux/macOS:

bash
Copy
Edit
docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" doc-intel-challenge
Windows PowerShell:

powershell
Copy
Edit
docker run --rm -v "${PWD}/input:/app/input" -v "${PWD}/output:/app/output" doc-intel-challenge
📄 Step 4: View Output
Check the generated file:

bash
Copy
Edit
output/challenge1b_output.json
