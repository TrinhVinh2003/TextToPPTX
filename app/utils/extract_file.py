import requests
from langchain_community.document_loaders import PyPDFLoader

from langchain.text_splitter import CharacterTextSplitter


def load_pdf(filename, max_chunks=5):
    """Load and split PDF content into chunks, limit to max_chunks."""
    loader = PyPDFLoader(filename)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30)
    chunks = text_splitter.split_documents(documents)
    return chunks[:max_chunks]


def download_file_from_google_drive(file_id, destination):
    URL = "https://drive.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  
                f.write(chunk)
                