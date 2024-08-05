from pypdf import PdfReader
from anthropic import Anthropic

client = Anthropic()  # have to load api_key from env file
MODEL_NAME = "claude-3-opus-20240229"  # can change model to haiku/sonnet


def check_number_of_pages(pdf_reader):
    # checks number of pages
    number_of_pages = len(pdf_reader.pages)
    return number_of_pages


def extract_text_from_pdf(path):
    reader = PdfReader(path)
    number_of_pages = check_number_of_pages(reader)
    if number_of_pages == 1:
        return ''.join(page.extract_text() for page in reader.pages)
    else:
        page_1 = reader.pages[0]
        return page_1.extract_text()


def get_completion(llm_client, prompt):
    return llm_client.messages.create(
        model=MODEL_NAME,
        max_tokens=100,
        messages=[{
            "role": 'user', "content": prompt
        }]
    ).content[0].text


def build_summarize_prompt(text):
    summarize_prompt = f"""

    User_Query: Here is an document I am interested in understanding: <paper>{text}</paper>
    please do the following:
    Summarize the abstract at a kindergarten reading level in less than 100 words. (In <kindergarten_abstract> tags.)
    """
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


def build_general_prompt(text, actual_query):
    general_prompt = f"""

    User_Query: In the given document: <paper>{text}</paper>
    please answer the following in less than 10 words:
    {actual_query}. 
    """
    return general_prompt



if __name__ == "__main__":
    # path = "/Users/sonikaboyapally/Downloads/fw9.pdf"
    # given_text = extract_text_from_pdf(path)
    # user_question = " "
    # general_prompt = build_summarize_prompt(given_text, user_question)
    # completion = get_completion(client, general_prompt)
    # print(completion)
    pass




