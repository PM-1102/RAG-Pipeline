import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


class GroqLLM:
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant",
            temperature=0.1
        )

    def generate(self, query, context):
        prompt = f"""
        You are a strict AI assistant.

        Answer the question ONLY using the provided context.

        Rules:
        - If the answer is not in the context, say: "I don't know based on the provided document."
        - Do NOT use outside knowledge
        - Do NOT guess or infer
        - Keep answers concise and factual

        Context:
        {context}

        Question: {query}

        Answer:
        """
        response = self.llm.invoke(prompt)
        return response.content