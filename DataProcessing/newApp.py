import os
from dotenv import load_dotenv
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv()

# Access API key from .env
openai_api_key = os.getenv('OPENAI_API_KEY')

# Ensure the API key is available
if not openai_api_key:
    raise ValueError("API key not found in environment. Make sure it's in the .env file.")

# Create instance of OpenAI LLM
llm = OpenAI(
    temperature=0.0,  # Lower temperature for more deterministic output
    max_tokens=1500,
    verbose=True,
    openai_api_key=openai_api_key
)

embeddings = OpenAIEmbeddings()

# Path to store the persisted vector database
persist_directory = "chroma_store"

# Check if the vector store already exists
if os.path.exists(persist_directory):
    # Load existing Chroma store
    store = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    print("Loaded existing Chroma vector store.")
else:
    # Create and load PDF Loader
    loader = PyPDFLoader('pdfData/annualreport-2023.pdf')
    documents = loader.load()

    # Verify that documents are loaded
    if not documents:
        raise ValueError("No documents found in the PDF file.")

    # Define a text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    # Split documents into chunks
    pages = text_splitter.split_documents(documents)

    # Verify that pages are split
    if not pages:
        raise ValueError("No text chunks created from the documents.")

    # Create a new Chroma store from documents and save it
    store = Chroma.from_documents(
        pages,
        embeddings,
        collection_name='annualreport',
        persist_directory=persist_directory
    )
    store.persist()
    print("Created and persisted new Chroma vector store.")

# Verify the number of documents in the vector store
collection = store._collection
num_documents = collection.count()
print(f"Number of documents in vector store: {num_documents}")

if num_documents == 0:
    raise ValueError("Vector store is empty. Ensure that documents are properly added.")

# Create a retriever
retriever = store.as_retriever()

# Create the RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    verbose=True
)

def run_query():
    prompt = input('Enter your prompt: ')
    if prompt:
        # Pass the prompt to the LLM and get a response
        response = qa_chain.run(prompt)
        print("\nResponse:\n", response)

        # Perform similarity search with the vector store
        try:
            search_results = store.similarity_search_with_relevance_scores(prompt, k=3)
            if not search_results:
                print("No relevant documents found.")
            else:
                # Display the most relevant documents
                print("\nRelevant Documents:")
                for doc, score in search_results:
                    print(f"\nScore: {score}\nContent:\n{doc.page_content}")
        except AttributeError as e:
            print(f"Method not found: {e}")
        except Exception as e:
            print(f"An error occurred during similarity search: {e}")

run_query()