from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
import os
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

os.environ["OPENAI_API_KEY"] = "random"
documents = SimpleDirectoryReader("docs").load_data()
index = GPTVectorStoreIndex.from_documents(documents)

index.as_query_engine().query("test")

# query_engine = index.as_query_engine()
# response = query_engine.query("What did the author do growing up?")
# print(response)
