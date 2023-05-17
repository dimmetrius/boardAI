from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.schema import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.chains.question_answering import load_qa_chain
import os
import json

load_dotenv()

llm = OpenAI(temperature=0)
document_content_description = "Board meeting description"
metadata_field_info = [
    AttributeInfo(
        name="committee",
        description="committee ID",
        type="string",
    ),
    AttributeInfo(
        name="title",
        description="Meeting title",
        type="string",
    ),
    AttributeInfo(
        name="date",
        description="Meeting date",
        type="string",
    ),
    AttributeInfo(
        name="url",
        description="Meeting url",
        type="string",
    ),
]
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
vectorstore = Chroma(embedding_function=embeddings, persist_directory="chroma")
# Retriever that wraps around a vector store and uses an LLM to generate the vector store queries.
retriever = SelfQueryRetriever.from_llm(
    llm, vectorstore, document_content_description, metadata_field_info, verbose=True
)

print("=======================")
print("# print EXIT for exit #")
print("=======================")
while True:
    txt = input("Enter your question: ")
    if txt == "EXIT":
        break
    try:
        docs = retriever.get_relevant_documents(txt)
        print("docs:")
        for doc in docs:
            print("Title: " + doc.metadata["title"])
            print("Url: " + doc.metadata["url"])
            print("Date: " + doc.metadata["date"])

        # chain = load_qa_chain(llm, chain_type="stuff")
        # query = "What did the David Weekly say in meetings"
        # resp = chain.run(input_documents=docs, question=query)
        # print(resp)

    except Exception as err:
        print("Exception:", err)
