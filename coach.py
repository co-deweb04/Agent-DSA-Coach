from google import genai
from config import GEMINI_API_KEY
from rag import retrieve_context

client = genai.Client(api_key=GEMINI_API_KEY)


def get_response(question, mode):

    context = retrieve_context(question)

    prompt = f"""
You are a DSA Coach Agent.

Help the student learn Data Structures and Algorithms.

Mode: {mode}

Relevant knowledge:
{context}

Student question:
{question}

Instructions:
- Explain concepts in simple language.
- Give hints instead of the complete answer in Hint mode.
- Explain solutions step by step in Solution mode.
- Review code and suggest improvements in Code Review mode.
- Use the provided context when answering.
- Do not invent information that conflicts with the provided context.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text