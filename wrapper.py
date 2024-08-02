import os
import anthropic
from langchain_core.prompts import ChatPromptTemplate

my_api_key = "" # add later from an env file
def chat(prompt):
    client = anthropic.Anthropic(
        api_key=my_api_key,
    )
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content

