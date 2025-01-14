import uuid
from app.core.configs import settings
from app.mdtree.tree2ppt import Tree2PPT
from langchain_community.document_loaders import PyPDFLoader

from langchain.text_splitter import CharacterTextSplitter
from app.chain.gpt_memory import GptChain

class Gen:
    chain: GptChain = None

    def __init__(self, session_id):
      
      self.chain = GptChain(
            openai_api_key=settings.OPENAI_API_KEY,
            session_id=session_id,
            redis_url=settings.REDIS_URL,
            openai_base_url=settings.OPENAI_BASE_URL,
        )

# ----------------------------------------------------------------
class GenOutline(Gen):
    def __init__(self, session_id):
        super().__init__(session_id)

    def generate_outline_from_pdf(self,pdf_chunks:str, topic:str)->str:
        # """Generate an outline and detailed content for the given topic using content from the PDF."""
        full_text = " ".join(chunk.page_content for chunk in pdf_chunks)
        input = f"""
        Create a structured outline with detailed content for a PowerPoint presentation based on the following content:
        {full_text}
        
        Topic: {topic}
        
        Ensure:
        1. The outline adheres to markdown format.
        2. Each heading includes content wrapped in <p></p> tags.
        """
        return self.chain.predict(human_input=input)

    def generate_outline_from_topic(self,topic):
        input = f"""
        Create a structured outline with detailed content  for a PowerPoint presentation:
        Topic: {topic}
        
        Ensure:
        1. The outline adheres to markdown format.
        2. Each heading includes content wrapped in <p></p> tags.
        """
        
        return self.chain.predict(human_input=input)





