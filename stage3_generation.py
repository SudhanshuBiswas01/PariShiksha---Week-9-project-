import google.generativeai as genai
import os

class StudyAssistant:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_answer(self, question, retrieved_chunks):
        context = "\n---\n".join([c['text'] for c in retrieved_chunks])
        
        prompt = f"""
You are PariShiksha, a grounded study assistant for NCERT Science.
Your goal is to answer student questions based ONLY on the provided context.

RULES:
1. Use ONLY the provided context to answer.
2. If the answer is not in the context, say: "I am sorry, but I cannot find the answer to this question in the textbook content provided."
3. Stay strictly grounded in the facts from the textbook.
4. Do not use outside knowledge.
5. If the question is out of scope for the provided context, refuse politely.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""
        response = self.model.generate_content(prompt, generation_config={"temperature": 0})
        return response.text
