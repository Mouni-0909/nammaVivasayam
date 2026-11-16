
import hashlib
import json
import time

import config

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI


class FarmerRAG:

    def __init__(self):

        # Create folders if missing
        config.PDF_FOLDER.mkdir(parents=True, exist_ok=True)
        config.FAISS_FOLDER.mkdir(parents=True, exist_ok=True)

        # Load embedding model
        self.embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL
        )

        # Load OpenAI model
        self.llm = ChatOpenAI(
            model=config.LLM_MODEL,
            temperature=0,
            api_key=config.OPENAI_API_KEY
        )

        # Split PDF content
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150
        )

        self.hash_file = config.FAISS_FOLDER / "files.json"

        # Load saved PDF details
        if self.hash_file.exists():
            self.files = json.loads(
                self.hash_file.read_text(encoding="utf-8")
            )
        else:
            self.files = {}

        # Load existing FAISS index
        self.vectorstore = None

        index_path = config.FAISS_FOLDER / "index.faiss"

        if index_path.exists():
            self.vectorstore = FAISS.load_local(
                str(config.FAISS_FOLDER),
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            self.files = {}

    # Add new PDF
    def add_pdf(self, file_name, data):

        start = time.time()

        # Check PDF format
        if not data.startswith(b"%PDF"):
            return "Invalid PDF file"

        # Avoid duplicate PDFs
        file_hash = hashlib.sha256(data).hexdigest()

        if file_hash in self.files:
            return "Already added"

        # Save PDF if it does not exist
        file_path = config.PDF_FOLDER / (
            file_hash[:10] + "_" + file_name
        )

        if not file_path.exists():
            file_path.write_bytes(data)

        # Read PDF content
        documents = PyPDFLoader(str(file_path)).load()

        for doc in documents:
            doc.metadata["source"] = file_name
            doc.metadata["page"] += 1

        # Split into chunks
        chunks = self.splitter.split_documents(documents)

        if not chunks:
            return "No readable text found"

        # Add chunks to FAISS
        if self.vectorstore is None:
            self.vectorstore = FAISS.from_documents(
                chunks, self.embeddings
            )
        else:
            self.vectorstore.add_documents(chunks)

        # Save FAISS index
        self.vectorstore.save_local(
            str(config.FAISS_FOLDER)
        )

        # Save PDF details
        self.files[file_hash] = file_name

        self.hash_file.write_text(
            json.dumps(self.files, indent=4),
            encoding="utf-8"
        )

        elapsed = round(time.time() - start, 1)

        return f"Added successfully in {elapsed} seconds"

    # Process PDFs already saved in folder
    def process_existing_pdfs(self):

        for pdf in config.PDF_FOLDER.glob("*.pdf"):

            file_hash = hashlib.sha256(
                pdf.read_bytes()
            ).hexdigest()

            if file_hash not in self.files:
                self.add_pdf(pdf.name, pdf.read_bytes())

    # Ask questions
    def ask_question(self, question, language, history):

        if self.vectorstore is None:
            return "Please upload PDF files first.", []

        start = time.time()

        # Search relevant PDF chunks
        results = self.vectorstore.similarity_search(
            question,
            k=config.TOP_K
        )

        context = "\n".join(
            doc.page_content for doc in results
        )

        # Collect unique sources
        sources = []

        for doc in results:
            source = {
                "file": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", 1)
            }

            if source not in sources:
                sources.append(source)

        # Previous chat messages
        chat_history = "\n".join(
            msg["role"] + ": " + msg["content"]
            for msg in history[-6:]
        )

        # Generate response
        prompt = f"""
You are Namma Vivasayam, a Tamil Nadu farmer assistant.

Answer in {language} using simple words.

Use only the provided PDF information.
Never invent scheme names, amounts or eligibility.

If the information is unavailable, say so clearly.

Previous conversation:
{chat_history}

PDF information:
{context}

Question:
{question}
"""

        answer = self.llm.invoke(prompt)

        print(
            f"Question answered in "
            f"{time.time() - start:.1f} seconds"
        )

        return answer.content, sources
