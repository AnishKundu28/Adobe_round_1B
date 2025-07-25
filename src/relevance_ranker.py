# src/relevance_ranker.py
import re
from typing import List, Tuple

def normalize(text):
    return re.sub(r"[^a-z0-9]", " ", text.lower())

def rank_sections(outlines: List[dict], persona: str, job: str) -> List[dict]:
    job_keywords = set(normalize(persona + " " + job).split())

    for item in outlines:
        section_keywords = set(normalize(item["text"]).split())
        overlap = job_keywords.intersection(section_keywords)
        item["score"] = len(overlap)

    sorted_outlines = sorted([o for o in outlines if o["score"] > 0],
                             key=lambda x: -x["score"])

    # Assign importance rank
    for idx, item in enumerate(sorted_outlines, start=1):
        item["importance_rank"] = idx

    return sorted_outlines
