# PariShiksha - Retrieval-Ready Study Assistant

PariShiksha is a grounded study assistant designed to answer NCERT Science questions reliably using Retrieval-Augmented Generation (RAG).

## Features
- **PDF Extraction**: Extracts text from NCERT PDFs using PyMuPDF.
- **Categorized Content**: Heuristic-based splitting into concepts, examples, and exercises.
- **Hybrid Retrieval**: Supports both Lexical (BM25) and Dense (Sentence Transformers) retrieval.
- **Grounded Generation**: Uses Gemini 1.5 Flash with a strict grounding prompt to prevent hallucinations.
- **Comprehensive Evaluation**: Includes 15+ questions across direct, paraphrased, and out-of-scope categories.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SudhanshuBiswas01/PariShiksha---Week-9-project-.git
   cd PariShiksha
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API Key**:
   Create a `.env` file or set the environment variable:
   ```bash
   export GOOGLE_API_KEY="your-api-key"
   ```

4. **Run the Notebook**:
   Open `PariShiksha_Assistant.ipynb` and run all cells.

## Corpus
The primary corpus is the NCERT Class 9 Science textbook, Chapter 8: Motion.
Source: [NCERT Chapter 8](https://ncert.nic.in/textbook/pdf/iesc108.pdf)

## Project Structure
- `data/`: PDF storage (ignored by git).
- `src/`: Modular code for extraction, retrieval, and generation.
- `PariShiksha_Assistant.ipynb`: Main implementation notebook.
- `evaluation_results.csv`: Results of the evaluation run.
- `reflection.md`: Project reflection and analysis.

## Evaluation Results
See `evaluation_results.md` (generated after running evaluation).
