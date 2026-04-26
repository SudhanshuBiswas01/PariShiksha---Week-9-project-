# Reflection: PariShiksha Study Assistant

## Part A — Your implementation artifacts

### A1. Your chunking parameters
**Parameters:**
- Chunk size: 500 words
- Overlap: 50 words
- Handling: Content split into `concepts`, `examples`, and `exercises` before chunking.

**Rationale:**
During initial testing with Chapter 8 (Motion), I observed that fixed-size chunking without overlap often cut off "Worked Examples" halfway through the solution. By adding a 50-word overlap and pre-splitting the content by type, I ensured that semantic units like "Example 8.1" were more likely to be retrieved in their entirety. A larger chunk size (500) was preferred over smaller ones (200) because NCERT's explanatory paragraphs are dense and require context to understand the relationship between distance and displacement.

### A2. A retrieved chunk that was wrong for its query
**Query:** "Explain quantum entanglement in Chapter 9 of NCERT."
**Retrieved Chunk:** "...The study of motion of objects along a straight line is called linear motion. In this chapter, we shall first learn to describe the motion of objects along a straight line..."
**Reasoning:**
The retriever returned this because Chapter 9 (or Chapter 8 in my current setup) does not contain the term "quantum entanglement". However, because BM25 is a lexical retriever, it attempted to match terms like "Explain", "Chapter", and "NCERT". Since these terms appear frequently in the introductory paragraphs of the textbook, it retrieved the general introduction as the "best match" even though the semantic core of the query was missing.

### A3. Your grounding prompt, v1 and v(final)
**v1 (Initial):**
"Answer the following question based on the context: {context}. Question: {question}"

**v(final):**
"You are PariShiksha, a grounded study assistant... RULES: 1. Use ONLY the provided context... 2. If the answer is not in context, say: 'I am sorry, but I cannot find the answer...' 3. Stay strictly grounded... 4. Do not use outside knowledge."

**Observation:**
The initial version was too permissive. When asked "Who wrote this book?", the model would sometimes hallucinate a name based on general knowledge. The final version added explicit "Refusal" rules and a persona ("PariShiksha"), which significantly improved the refusal rate for out-of-scope questions.

## Part B — Numbers from your evaluation

### B1. Your evaluation scores
- (a) Correct: 11/15
- (b) Grounded: 13/15
- (c) Appropriate refusals: 4/5

**Analysis:**
The number that bothered me most was the **Grounded** score vs **Correct** score. Two answers were "grounded" (used the text) but "incorrect" because the retriever picked a similar but wrong example (e.g., retrieving Example 8.1 when the question asked for 8.2). This highlights that retrieval quality is the bottleneck, not generation.

## Part C — Debugging moments

### C1. The most frustrating bug
The most frustrating issue was the PDF extraction splitting words like "acceleration" into "ac- celeration" due to line breaks in the PDF. This caused the BM25 retriever to fail on key terms. 
**Fix:** Implemented a regex-based cleaning step to join words split by hyphens at line endings before chunking.

### C2. What still bothers you
The system still struggles with "Reasoning" questions that span multiple chunks. For example, "Why is displacement zero if an object returns to the start?" requires connecting the definition of displacement from one chunk with the concept of a circular path from another. Hybrid retrieval (BM25 + Dense) helped, but didn't fully solve the multi-hop reasoning gap.

## Part D — Architecture and reasoning

### D1. Why not just ChatGPT?
ChatGPT is a generalist. While it knows about Motion, it might use definitions or examples not found in the NCERT textbook (e.g., using Imperial units or advanced calculus not in Class 9). For PariShiksha, trust is built on textbook alignment. If a student is told a formula different from their book, it creates confusion. My RAG system ensures that the answer is exactly what is in their textbook.

### D2. The GANs reflection
GANs (Generative Adversarial Networks) are designed for creating new, realistic data (like images or creative text) by pitting a generator against a discriminator. In a textbook assistant, we don't want "creative" or "new" facts; we want exact retrieval and summarization. GANs lack the grounding mechanism required for factual accuracy. This taught me that for high-stakes, fact-based tasks, "Constrained Generation" (RAG) is superior to "Adversarial Generation".

### D3. Honest pilot readiness
I would **not** launch this Monday. 
Three things to fix first:
1. **Mathematical Rendering**: Formulas in the PDF are currently extracted as plain text, which can be messy. I need a better OCR/Formula extractor.
2. **Multi-hop Retrieval**: Implement a reranker to handle questions that require context from two different pages.
3. **Safety Guardrails**: Test more extensively for prompt injection and language switching (Hinglish).

## Part E — Effort and self-assessment

### E1. Effort rating
**Rating: 8/10**
I am proud of the hybrid retrieval implementation and the detailed evaluation set that includes adversarial out-of-scope questions.

### E2. The gap between you and a stronger student
A stronger student might have implemented a "Query Expansion" step using the LLM to handle student slang/Hinglish before retrieval, which would make the system much more robust in Tier-2/3 city contexts.

### E3. What would change with two more days
1. **First thing**: Implement a Cross-Encoder reranker to improve precision.
2. **Last thing**: Build a simple Streamlit UI to showcase the prototype to stakeholders.
