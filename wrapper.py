from pypdf import PdfReader
from anthropic import Anthropic

client = Anthropic()  # have to load api_key from env file
MODEL_NAME = "claude-3-opus-20240229"  # can change model to haiku/sonnet


def extract_text_from_pdf(path):
    reader = PdfReader("/Users/sonikaboyapally/Downloads/fw9.pdf")
    number_of_pages = len(reader.pages)
    if number_of_pages > 1:
        pass
    # dont produce a completion, raise exception and produce that message
    text = ''.join(page.extract_text() for page in reader.pages)
    return text


def get_completion(llm_client, prompt):
    return llm_client.messages.create(
        model=MODEL_NAME,
        max_tokens=2048,
        messages=[{
            "role": 'user', "content": prompt
        }]
    ).content[0].text


completion = get_completion(client,
                            f"""Here is an document I am interested in understanding: <paper>{text}</paper>
                            Please do the following:
                            1. Summarize the abstract at a kindergarten reading level. (In <kindergarten_abstract> tags.)"""
                            )

print(completion)
