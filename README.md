# Deep-Knowledge-Chatbot

An external retrieval-augmented generation (RAG) assistant that answers your questions using a local Embedding model and LLM model via [Ollama](https://ollama.com), powered by LangChain and FAISS.

This version is set to obtain its knowledge from travel sites/blogs for better traveling related advices, but you can customize it to your own content easily.

## Features

- Fully local RAG setup (no need for cloud api)
- Performs Deep Research to enrich its knowledge base before answering the user
- Uses Ollama-compatible models for both embedding and generation
- Built with Python, using LangChain and FAISS library
- Interactive terminal interface
- Fallback to general knowledge if answer isn’t found in knowledge base

## Requirements

- Python 3.11+
- [Ollama](https://ollama.com) installed and running
- pull LLM model and Embedding model from Ollama to local (after pulling, change line 18 and 22 of the code accordingly)

Install Python library dependencies:
```bash
pip install requests beautifulsoup4 langchain langchain-community langchain-ollama faiss-cpu
```

## Sources of Information

The chat-bot is set to fetch data from specific website URLs to enrich it's knowledge base. You can change line ??? of the code to change the URLs, and it will switch the knowledge that the chat-bot is focusing on. 

## How It Works

This project uses Retrieval-Augmented Generation (RAG), which combines a embedding vector database created from your content, along with a language model to answer questions more accurately and contextually.

### Embedding the Content

- As the preperation for Deep Research, texts will be extracted from external websites to act as our knowledge base.

- The contents will be converted by projecting the **high-dimensional space of initial data vectors** into a **lower-dimensional space** using a local embedding model (in the code provided, we used 'snowflake-arctic-embed:335m' from Ollama).

- These vectors capture the semantic meaning of the text — two similar tips will have similar embeddings. 

### Storing in a Vector Database

- The vectors are stored in FAISS, a fast, in-memory vector store that supports efficient similarity search.

- This lets the system quickly find the most relevant chunks of text when a new question is asked.

### Retrieving and Generating Answers

- When you ask a question, it is also embedded into a vector on the spot for the LLM model to actully understand your question.

- FAISS compares this vector to the ones in the vector database and returns the top matching text chunks, and the specific phrase we use is **"top-k"**.

- **top-k** is the number of top matching entries we retrieve from the embedding. If the number is too small, we might miss out on some relevant information; if it's too large, we're likely getting too much unrelated content. In the code provided we are using **"top-k 3"**, which is a recommended good default option.

- These relevant texts are passed to the LLM (in the provided code we used 'gemma3:12b') along with our question.

- The LLM uses this context to generate a more accurate, grounded, and helpful response.

## Usage

Run the following command in the directory of the python file. 
```bash
python deep-knowledge-chatbot.py
```

Type in what you want to ask when the prompt "Your question: " shows up. 

Example use of the code:
```bash
<some-user-directory>:~$ python deep-knowledge-chatbot.py
    Internal RAG Q&A Bot    
Ask questions about cooking hacks and kitchen tips.
This assistant is powered by a local language model and a custom knowledge base built from community-sourced cooking advice.
Type 'exit' to quit.

Your question:
```

Here we enter our question:
```bash
Your question: where would you recommend for hiking?
```

The answer responded is:
```bash
Answer: Based on the text, I would recommend hiking around Mont Blanc. The author describes it as doable for reasonably fit hikers and highlights the positive experience they had.


Your question: 
```

Ask the chat-bot a follow-up question:
```bash
Your question: can you share more on the author's experience?
```

The second answer responded is:
```bash
Answer: The author has traveled extensively with his wife, Intan (who is from Bali). Together they've done bucket list hikes, climbed active volcanoes, seen exotic wildlife, and visited castles, temples, and monuments worldwide. He's been featured by BBC Travel, NBC News, Time, and other companies, indicating a recognized travel blog. 


Your question:
```

now we can type "exit" to close this chatbot: 

```bash
Your question: exit
Goodbye!
```







