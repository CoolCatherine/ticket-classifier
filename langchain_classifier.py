from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
import os

EMAIL_CATEGORIES = [
    "Technical Support",
    "Customer Support",
    "Product Feedback",
    "Compliance",
    "General Query"
]

def classify_with_langchain(subject, body):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=api_key)

    prompt = PromptTemplate(
        input_variables=["subject", "body", "categories"],
        template=(
            "Analyze the following email and classify it into one of the following categories:\n"
            "{categories}\n\n"
            "Email Subject: {subject}\n"
            "Email Body:\n{body}\n\n"
            "Respond ONLY with the category name from the provided list. "
            "If the content does not clearly fit any category, respond with 'General Query'."
        )
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.run(subject=subject, body=body, categories=", ".join(EMAIL_CATEGORIES))
    result = result.strip()
    if result not in EMAIL_CATEGORIES:
        result = "General Query"
    return result 