
# Import necessary libraries
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import FAISS

# url list to be scraped
urls = [
    "https://theworldtravelguy.com/",
    "https://blog.ricksteves.com/",
    "https://www.theblondeabroad.com/",
    "https://www.reddit.com/r/solotravel/",
]


# Initialize text storage
all_texts = []

# Step 1: Fetch and process content from multiple URLs
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract text from <p> tags
    text = ' '.join([para.get_text() for para in soup.find_all('p')])
    
    if text:  # Store only if text is found
        all_texts.append(text)


# Split all content into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
all_chunks = []
for text in all_texts:
    all_chunks.extend(text_splitter.split_text(text))

# Initialize Ollama embeddings and FAISS vector store
embeddings = OllamaEmbeddings(model="snowflake-arctic-embed:335m")
vector_store = FAISS.from_texts(all_chunks, embeddings)

# Initialize Ollama LLM
llm = OllamaLLM(model="gemma3:12b", temperature=0.3)

# Question-answering function with fallback
def ask_question_with_fallback(query):
    docs = vector_store.similarity_search(query, k=3)

    if not docs:
        return use_general_knowledge(query)

    context = "\n\n".join([doc.page_content for doc in docs])

    rag_prompt = f"""
    Use the following context to answer the question, but in case that the context does not help, answer 'i don't know':
    
    Context:
    {context}

    Question: {query}
    """

    rag_answer = llm.invoke(rag_prompt)

    if "NO_ANSWER_FOUND" in rag_answer or "don't know" in rag_answer.lower():
        return use_general_knowledge(query)

    return {"answer": rag_answer}

# General knowledge fallback
def use_general_knowledge(query):
    general_prompt = f"Please mention that you are answering with general knowledge at the begining of your answer for this question: {query}"
    general_answer = llm.invoke(general_prompt)
    return {"answer": general_answer}

# Continuous interaction loop
print("    Deep Knowledge Chat-Bot    ")
print("Ask about destinations, tips, solo travel, budgeting, and more.")
print("Type 'exit' to quit.\n")


while True:
    query = input("Your question: ").strip()
    if query.lower() == "exit":
        print("Goodbye! ")
        break

    result = ask_question_with_fallback(query)
    print("\nAnswer:", result["answer"], "\n")
