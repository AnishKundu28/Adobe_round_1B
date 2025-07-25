# PDF Outline Extractor

This is a solution for extracting structured outlines from PDF documents. The tool processes PDF files and generates a JSON output containing the document title and a hierarchical outline of headings (H1, H2, H3) with their respective page numbers.

## Features

- Extracts document title from PDF metadata (falls back to filename)
- Identifies headings (H1, H2, H3) using font size and style heuristics
- Supports PDFs with embedded table of contents
- Processes multiple PDFs in batch
- Containerized solution using Docker

## Requirements

- Docker
- Python 3.9+ (for local development)

## Installation

1. Clone this repository
2. Build the Docker image:
   ```bash
   docker build --platform linux/amd64 -t pdf-outline-extractor:latest .
   ```

## Usage

1. Place your PDF files in the `input` directory
2. Run the container:
   ```bash
   docker run --rm \
     -v $(pwd)/input:/app/input \
     -v $(pwd)/output:/app/output \
     --network none \
     pdf-outline-extractor:latest
   ```
3. Find the extracted outlines in the `output` directory as JSON files

## Output Format

The output is a JSON file with the following structure:

```json
{
  "title": "Document Title",
  "outline": [
    {"level": "H1", "text": "Main Heading", "page": 1},
    {"level": "H2", "text": "Subheading", "page": 2},
    ...
  ]
}
```

## How It Works

1. The tool first tries to use the PDF's built-in table of contents if available
2. If no TOC is found, it analyzes the text blocks in the document, looking for text with larger font sizes and bold styling to identify headings
3. Headings are classified into H1, H2, and H3 based on their relative sizes
4. The results are saved as JSON files with the same name as the input PDF

## Performance

- Processes a 50-page PDF in under 10 seconds
- Container size is approximately 300MB
- Works offline with no external dependencies

## Limitations

- Works best with properly structured PDFs
- May not work well with scanned documents or images of text
- Heading detection heuristics might need adjustment for documents with unusual formatting

## License

This project is open source and available under the MIT License.
