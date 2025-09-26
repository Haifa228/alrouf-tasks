import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings  # Mock if no key
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from googletrans import Translator  # For AR/EN

# Mock embeddings if no OpenAI key
class MockEmbeddings:
    def embed_documents(self, texts):
        return [[0.1] * 1536 for _ in texts]  # Fake vector
    def embed_query(self, text):
        return [0.1] * 1536

# Load documents
documents_dir = "documents/"
docs = []
for file in os.listdir(documents_dir):
    if file.endswith(".txt"):
        loader = TextLoader(os.path.join(documents_dir, file))
        docs.extend(loader.load())

# Chunk
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(docs)

# Embed and index
embeddings = MockEmbeddings() if not os.getenv("OPENAI_API_KEY") else OpenAIEmbeddings()
vectorstore = FAISS.from_documents(texts, embeddings)

# LLM (mock if no key)
llm = OpenAI(temperature=0) if os.getenv("OPENAI_API_KEY") else lambda q: f"Mock answer for {q}"

# Retrieval QA
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever(), return_source_documents=True)

# Translator for AR/EN
translator = Translator()

def query_rag(query, lang="en"):
    result = qa({"query": query})
    answer = result["result"]
    sources = [doc.metadata["source"] for doc in result["source_documents"]]

    # Translate if needed
    if lang == "ar":
        answer = translator.translate(answer, dest="ar").text

    return {"answer": answer, "sources": sources}

if __name__ == "__main__":
    print("RAG CLI: Enter query (or 'exit'). Lang: en/ar")
    while True:
        query = input("Query: ")
        if query == "exit": break
        lang = input("Lang (en/ar): ")
        result = query_rag(query, lang)
        print(f"Answer: {result['answer']}")
        print(f"Citations: {result['sources']}")
