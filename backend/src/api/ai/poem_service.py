from api.ai.llm import get_openai_llm
from api.ai.schemas import EmailMessageSchema

def generate_email_message(query: str) -> EmailMessageSchema:
    llm_base = get_openai_llm()
    llm = llm_base.with_structured_output(EmailMessageSchema)

    messages = [
        (
            "system",
            "You are a helpful assistant for writing high-quality plaintext poems in the form of email messages. "
            "Your responses should be well-structured, human-readable, and informative. "
            "Do not use markdown or formatting like *, #, or backticks. "
            "Structure your output exactly as: {\"subject\": \"...\", \"content\": \"...\", \"invalid_request\": false}. "
            "Do not explain anything outside the JSON. Reply with pure JSON only."
        ),
        (
            "human",
            f"{query}. Do not use markdown in your response only plaintext."
        )
    ]

    return llm.invoke(messages)
