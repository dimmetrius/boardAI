from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from boarddocs import BoardDocsReader
from langchain.vectorstores import Chroma
from langchain.schema import Document
import json
import os

load_dotenv()

langchain_docs = []
docs_files = os.listdir("docs")

for name in docs_files:
    f = open("./docs/" + name)
    json_doc = json.loads(json.load(f))
    langchain_docs.append(
        Document(page_content=json_doc["text"], metadata=json_doc["extra_info"])
    )
    f.close()

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
vectorstore = Chroma.from_documents(
    langchain_docs, embedding=embeddings, persist_directory="chroma"
)
vectorstore.persist()
