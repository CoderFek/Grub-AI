import os
from langchain_openai import ChatOpenAI

OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL")

if not OPENAI_API_KEY:
    raise NotImplementedError("`OPENAI_API_KEY` is not set")

def get_openai_llm():
    openai_params = {
        "model": OPENAI_MODEL,
        "api_key": OPENAI_API_KEY,
    }
    if OPENAI_BASE_URL:
        openai_params["base_url"] = OPENAI_BASE_URL
    return ChatOpenAI(**openai_params)
