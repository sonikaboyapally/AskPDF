from pypdf import PdfReader
from anthropic import Anthropic

client = Anthropic()  # have to load api_key from env file
MODEL_NAME = "claude-3-opus-20240229"  # can change model to haiku/sonnet


def extract_text_from_pdf(path):
    reader = PdfReader(path)
    number_of_pages = len(reader.pages)
    if number_of_pages > 1:
        pass
    # dont produce a completion, raise exception and produce that message
    text = ''.join(page.extract_text() for page in reader.pages)
    return text


def get_completion(llm_client, prompt):
    return llm_client.messages.create(
        model=MODEL_NAME,
        max_tokens=100,
        messages=[{
            "role": 'user', "content": prompt
        }]
    ).content[0].text

def build_summarize_prompt(text):
    summarize_prompt = f"""Here is an document I am interested in understanding: <paper>{text}</paper>
    Please do the following:
    Summarize the abstract at a kindergarten reading level in less than 100 words. (In <kindergarten_abstract> tags.)"""
    return summarize_prompt


def build_records_extraction_prompt(text):
    records_prompt = f'''
    @dataclass
    class Record:
        name : str
        role : str
    
    Function:
    def identities(names : List[Record]):
    """
    given the name and role of the people 
    """
    
    User_Query : given {text}, identify all the records of people in the document and their role<human_end>
    
    '''
    return records_prompt

if __name__ == "__main__":
    # path = "/Users/sonikaboyapally/Downloads/fw9.pdf"
    # summarize_prompt = build_summarize_prompt(extract_text_from_pdf(path))
    # completion = get_completion(client, summarize_prompt)
    # print(completion)
    pass




