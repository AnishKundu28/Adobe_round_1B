# src/intelligence_system.py

import time
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
import torch
import nltk
from pdf_parser import PDFParser

class DocumentIntelligenceSystem:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        print("Initializing intelligence system...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        self.model = SentenceTransformer(model_name, device=self.device)
        self.parser = PDFParser()
        # Ensure NLTK data is available
        try:
            nltk.data.find('tokenizers/punkt')
        except nltk.downloader.DownloadError:
            nltk.download('punkt')
        print("Initialization complete.")

    # --- THIS IS THE METHOD THAT WAS ADDED ---
    def _get_query(self, persona: str, job_to_be_done: str) -> str:
        """Combines persona and job into a descriptive query."""
        return f"User Persona: {persona}. Task: {job_to_be_done}"

    def analyze(self, input_dir: Path, output_dir: Path):
        start_time = time.time()
        
        # 1. Load inputs
        config_path = input_dir / "config.json"
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # This line now works because the _get_query method exists
        query = self._get_query(config['persona'], config['job_to_be_done'])
        
        doc_files = config['documents']
        
        # 2. Extract content from all documents
        all_sections = []
        print("Extracting sections from documents...")
        for doc_name in doc_files:
            doc_path = input_dir / doc_name
            if doc_path.exists():
                sections = self.parser.extract_sections(str(doc_path))
                all_sections.extend(sections)
            else:
                print(f"Warning: Document {doc_name} not found.")

        if not all_sections:
            print("No sections extracted. Exiting.")
            return

        # 3. Rank sections
        print("Ranking sections for relevance...")
        query_embedding = self.model.encode(query, convert_to_tensor=True, device=self.device)
        section_contents = [sec['content'] for sec in all_sections]
        section_embeddings = self.model.encode(section_contents, convert_to_tensor=True, device=self.device)
        
        similarities = util.cos_sim(query_embedding, section_embeddings)[0]
        
        for i, sec in enumerate(all_sections):
            sec['relevance_score'] = similarities[i].item()
            
        ranked_sections = sorted(all_sections, key=lambda x: x['relevance_score'], reverse=True)

        # 4. Generate output JSON
        print("Generating final output...")
        output_data = {
            "metadata": {
                "input_documents": [str(p) for p in doc_files],
                "persona": config['persona'],
                "job_to_be_done": config['job_to_be_done'],
                "processing_timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            },
            "extracted_sections": [],
            "sub_section_analysis": []
        }

        # Let's take the top 5 most relevant sections for the final output
        for rank, section in enumerate(ranked_sections[:5], 1):
            output_data["extracted_sections"].append({
                "document": section['source_doc'],
                "page_number": section['page'],
                "section_title": section['title'],
                "importance_rank": rank
            })
            
            # 5. Perform sub-section analysis (summarization)
            refined_text = self._summarize(section['content'], query_embedding)
            
            output_data["sub_section_analysis"].append({
                "document": section['source_doc'],
                "section_title": section['title'],
                "refined_text": refined_text,
                "page_number": section['page']
            })

        output_file = output_dir / "challenge1b_output.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)
            
        end_time = time.time()
        print(f"Processing complete in {end_time - start_time:.2f} seconds.")
        print(f"Output saved to {output_file}")

    def _summarize(self, content: str, query_embedding: torch.Tensor, num_sentences=3) -> str:
        """Extractive summary based on semantic similarity to the query."""
        sentences = nltk.sent_tokenize(content)
        if not sentences:
            return ""
            
        sentence_embeddings = self.model.encode(sentences, convert_to_tensor=True, device=self.device)
        similarities = util.cos_sim(query_embedding, sentence_embeddings)[0]
        
        top_sentence_indices = torch.topk(similarities, k=min(num_sentences, len(sentences))).indices
        top_sentences = [sentences[i] for i in sorted(top_sentence_indices.tolist())]
        
        return " ".join(top_sentences)