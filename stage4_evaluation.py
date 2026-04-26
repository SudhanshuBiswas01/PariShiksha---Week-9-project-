import os
import pandas as pd
from stage2_retrieval import ChunkStore, chunk_text
from stage3_generation import StudyAssistant
from stage1_corpus import extract_text_from_pdf, split_content

def run_evaluation(api_key):
    # Setup
    pdf_path = "data/motion.pdf"
    text = extract_text_from_pdf(pdf_path)
    sections = split_content(text)
    
    all_chunks = []
    for sec_name, content_list in sections.items():
        for content in content_list:
            chunks = chunk_text(content, {"chapter": "Motion", "section": sec_name})
            all_chunks.extend(chunks)
            
    store = ChunkStore()
    store.add_chunks(all_chunks)
    
    assistant = StudyAssistant(api_key)
    
    # Evaluation Set
    eval_set = [
        {"question": "What is distance?", "type": "direct"},
        {"question": "What is displacement?", "type": "direct"},
        {"question": "Define uniform motion.", "type": "direct"},
        {"question": "What is velocity?", "type": "direct"},
        {"question": "What is the formula for acceleration?", "type": "direct"},
        {"question": "Calculate the acceleration of a bus that slows down from 80 km/h to 60 km/h in 5 seconds.", "type": "worked_example"},
        {"question": "Explain the difference between path length and change in position.", "type": "paraphrased"},
        {"question": "How does velocity differ from speed?", "type": "paraphrased"},
        {"question": "What happens when an object moves in a circular path at constant speed?", "type": "paraphrased"},
        {"question": "Who wrote the NCERT Science textbook?", "type": "out-of-scope"},
        {"question": "What is quantum entanglement?", "type": "out-of-scope"},
        {"question": "How to cook biryani?", "type": "out-of-scope"},
        {"question": "Explain quantum entanglement in Chapter 8 of NCERT.", "type": "adversarial_out-of-scope"},
        {"question": "What is the unit of acceleration?", "type": "direct"},
        {"question": "What is the odometer used for?", "type": "direct"}
    ]
    
    results = []
    for item in eval_set:
        print(f"Evaluating: {item['question']}")
        retrieved_chunks = store.retrieve(item['question'], k=3)
        answer = assistant.generate_answer(item['question'], retrieved_chunks)
        
        results.append({
            "Question": item['question'],
            "Type": item['type'],
            "Answer": answer,
            "Retrieved Chunks": [c['text'][:100] for c in retrieved_chunks]
        })
        
    df = pd.DataFrame(results)
    df.to_csv("evaluation_results.csv", index=False)
    return df

if __name__ == "__main__":
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found.")
    else:
        run_evaluation(api_key)
