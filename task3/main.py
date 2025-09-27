import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms.base import LLM
from deep_translator import GoogleTranslator

# Mock LLM class for compatibility with langchain==0.1.20
class MockLLM(LLM):
    def _call(self, prompt, stop=None):
        return f"Mock answer for {prompt}"
    
    @property
    def _llm_type(self):
        return "mock"

    def predict(self, text):
        return self._call(text)

# Mock embeddings with callable interface
class MockEmbeddings:
    def embed_documents(self, texts):
        return [[0.1] * 1536 for _ in texts]  # Fake vector
    
    def embed_query(self, text):
        return [0.1] * 1536
    
    def __call__(self, text):
        return self.embed_query(text)  # Make it callable

# Load documents with encoding handling
documents_dir = "documents/"
docs = []
if os.path.exists(documents_dir) and os.path.isdir(documents_dir):
    for file in os.listdir(documents_dir):
        if file.endswith(".txt"):
            try:
                loader = TextLoader(os.path.join(documents_dir, file), encoding="utf-8")
                docs.extend(loader.load())
            except UnicodeDecodeError:
                try:
                    loader = TextLoader(os.path.join(documents_dir, file), encoding="cp1252")
                    docs.extend(loader.load())
                except Exception as e:
                    print(f"Failed to load {file}: {e}")
else:
    print("Warning: 'documents/' directory not found or empty. Using empty document set.")

# Chunk
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(docs) if docs else []

# Embed and index
embeddings = MockEmbeddings() if not os.getenv("OPENAI_API_KEY") else OpenAIEmbeddings()
vectorstore = FAISS.from_documents(texts, embeddings)

# LLM (mock if no key)
llm = MockLLM() if not os.getenv("OPENAI_API_KEY") else OpenAI(temperature=0)

# Retrieval QA
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever(), return_source_documents=True)

# Translator for AR/EN
translator = GoogleTranslator()

def query_rag(query, lang="en"):
    result = qa({"query": query})
    answer = result["result"]
    sources = [doc.metadata.get("source", "No source") for doc in result["source_documents"]]

    # Translate if needed
    if lang == "ar":
        answer = translator.translate(answer, target_lang="ar")

    return {"answer": answer, "sources": sources}

if __name__ == "__main__":
    print("RAG CLI: Enter query (or 'exit'). Lang: en/ar")
    while True:
        query = input("Query: ")
        if query == "exit":
            break
        lang = input("Lang (en/ar): ").lower() or "en"
        result = query_rag(query, lang)
        print(f"Answer: {result['answer']}")
        print(f"Citations: {result['sources']}")
