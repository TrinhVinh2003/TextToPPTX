# Updated to use `ChatOpenAI` for OpenAI models
from langchain_community.chat_message_histories import RedisChatMessageHistory

from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory


template = """
    {chat_history}
    You are an expert assistant tasked with creating a structured outline for a PowerPoint presentation.
    Use the extracted content from the document and focus on the given topic to create an outline.
    
    Guidelines:
    1. Use markdown headings indicated by hash symbols (#):
       - # for the main title of the presentation.
       - ## for chapters or main sections.
       - ### for key points within a chapter.
    
    2. For each heading, add detailed content wrapped in <p></p> tags.
    3. Ensure the outline starts with an introduction and ends with a conclusion.
    4. Adhere strictly to the provided topic..
    5. Provide concise, relevant, and well-structured content.

    Example structure:
    # Main Title
    ## Chapter 1: Introduction
    <p>Introduction content goes here.</p>
    ### Key Point 1
    <p>Details about key point 1.</p>
    ### Key Point 2
    <p>Details about key point 2.</p>
    ## Chapter 2: Main Section
    <p>Main section overview.</p>
    ### Subtopic 1
    <p>Details about subtopic 1.</p>
    ### Subtopic 2
    <p>Details about subtopic 2.</p>
    ## Chapter N: Conclusion
    <p>Conclusion content goes here.</p>
    
    
   {human_input}
    """



class GptChain:
    template: str = template
    openai_api_key: str = None
    session_id: str = None
    redis_url: str = None
    chain: LLMChain = None  # Updated to match the `chain` naming convention
    message_history: RedisChatMessageHistory = None

    def __init__(self, openai_api_key, session_id, redis_url, openai_base_url):
        self.openai_api_key = openai_api_key
        self.session_id = session_id
        self.redis_url = redis_url
        self.openai_base_url = openai_base_url
        self.create_chain()  # Updated method name to `create_chain`

    def create_chain(self):
        # Set up Redis-based message history
        message_history = RedisChatMessageHistory(
            url=self.redis_url, ttl=600, session_id=self.session_id
        )
        self.message_history = message_history

        # Create memory for chat history
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        prompt = PromptTemplate(
            input_variables=[ "human_input"],
            template=self.template,
        )
        llm = ChatOpenAI(
            model="gpt-4",
            openai_api_key=self.openai_api_key,
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()],
        )
        self.chain = LLMChain(
            llm=llm,
            prompt=prompt,
            verbose=True,
            memory=self.memory,
        )

        # Build the chain
     
    def predict(self, human_input: str) -> str:

    
        # Run the prediction with chat history, human input, and topic
        return self.chain.run(human_input=human_input)

    def clear_redis(self):
        """Clear the Redis message history."""
        self.message_history.clear()
