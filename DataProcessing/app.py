import os
from dotenv import load_dotenv
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()

# Access API key from .env
openai_api_key = os.getenv('OPENAI_API_KEY')

# Ensure the API key is available
if not openai_api_key:
    raise ValueError("API key not found in environment. Make sure it's in the .env file.")

# Create instance of OpenAI LLM
llm = OpenAI(temperature=0.8, verbose=True, openai_api_key=openai_api_key)
embeddings = OpenAIEmbeddings()

# Path to store the persisted vector database
persist_directory = "chroma_store"

# Check if the vector store already exists
if os.path.exists(persist_directory):
    # Load existing Chroma store
    store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    print("Loaded existing Chroma vector store.")
else:
    # Create and load PDF Loader
    loader = PyPDFLoader('pdfData/annualreport-2023.pdf')
    # Split pages from pdf 
    pages = loader.load_and_split()

    # Create a new Chroma store from documents and save it
    store = Chroma.from_documents(
        pages, embeddings, collection_name='annualreport', persist_directory=persist_directory
    )
    store.persist()
    print("Created and persisted new Chroma vector store.")

# Create a retriever
retriever = store.as_retriever()

# Create the RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # You can try "map_reduce" or "refine" for longer documents
    retriever=retriever,
    verbose=True
)

def run_query():
    prompt = input('Enter your prompt: ')
    if prompt:
        response = qa_chain.run(prompt)
        print("\nResponse:\n", response)



# Run the query function
def api_run_query(prompt):
    
    if prompt:
        # Pass the prompt to the LLM and get a response
        response = qa_chain.run(prompt)
        return response

        # Similarity search with the vectorstore
        # search = store.similarity_search_with_score(prompt)

        # Display the most relevant page's content
        # print("\nMost relevant page content:\n", search[0][0].page_content)