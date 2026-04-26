import fitz  # PyMuPDF
from transformers import AutoTokenizer
import pandas as pd
import os

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

def split_content(text):
    # Heuristic splitting based on common patterns in NCERT
    sections = {
        "concepts": [],
        "examples": [],
        "exercises": []
    }
    
    # Common headers in NCERT
    example_markers = ["Example", "Example:", "EXAMPLE"]
    exercise_markers = ["Questions", "Exercises", "EXERCISES", "Terminal Exercises"]
    
    current_section = "concepts"
    paragraphs = text.split('\n\n') # Often paragraphs are separated by double newlines
    
    for p in paragraphs:
        p = p.strip()
        if not p: continue
        
        # Check for section changes
        is_example = any(marker in p for marker in example_markers) and any(char.isdigit() for char in p[:20])
        is_exercise = any(marker in p for marker in exercise_markers)
        
        if is_example:
            current_section = "examples"
        elif is_exercise:
            current_section = "exercises"
            
        sections[current_section].append(p)
        
    return sections

def compare_tokenizers(text_samples):
    tokenizers = {
        "GPT-2 (BPE)": AutoTokenizer.from_pretrained("gpt2"),
        "BERT (WordPiece)": AutoTokenizer.from_pretrained("bert-base-uncased"),
        "T5 (SentencePiece)": AutoTokenizer.from_pretrained("t5-small")
    }
    
    results = []
    for name, tokenizer in tokenizers.items():
        for i, sample in enumerate(text_samples):
            tokens = tokenizer.tokenize(sample)
            results.append({
                "Tokenizer": name,
                "Sample Index": i,
                "Token Count": len(tokens),
                "Sample Snippet": sample[:50] + "..."
            })
    
    return pd.DataFrame(results)

if __name__ == "__main__":
    pdf_path = "data/motion.pdf"
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found.")
    else:
        text = extract_text_from_pdf(pdf_path)
        sections = split_content(text)
        
        print(f"Extracted {len(text)} characters.")
        print(f"Sections found: Concepts: {len(sections['concepts'])}, Examples: {len(sections['examples'])}, Exercises: {len(sections['exercises'])}")
        
        # Select some samples for tokenizer comparison
        samples = []
        if sections['concepts']: samples.append(sections['concepts'][0][:500])
        if sections['examples']: samples.append(sections['examples'][0][:500])
        if sections['exercises']: samples.append(sections['exercises'][0][:500])
        
        if samples:
            comparison_df = compare_tokenizers(samples)
            print("\nTokenizer Comparison Results:")
            print(comparison_df)
            comparison_df.to_csv("tokenizer_comparison.csv", index=False)
