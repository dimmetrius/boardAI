from llama_index.readers.schema.base import Document
from llama_index import GPTListIndex
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index import LangchainEmbedding, ServiceContext
import json
import os
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
os.environ["OPENAI_API_KEY"] = "random"

docs = []
docs_files = os.listdir("docs")

for name in docs_files:
    f = open("./docs/" + name)
    json_doc = json.loads(json.load(f))
    docs.append(Document(text=json_doc["text"]))
    f.close()

# load in HF embedding model from langchain
embed_model = LangchainEmbedding(HuggingFaceEmbeddings())
service_context = ServiceContext.from_defaults(embed_model=embed_model)

new_index = GPTListIndex.from_documents(docs)

# query with embed_model specified
query_engine = new_index.as_query_engine(
    retriever_mode="embedding", verbose=True, service_context=service_context
)
response = query_engine.query("David")
print(response)
