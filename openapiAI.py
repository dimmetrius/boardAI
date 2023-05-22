import yaml
import requests
import tiktoken
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from dotenv import load_dotenv

load_dotenv()
from langchain.agents.agent_toolkits.openapi.spec import reduce_openapi_spec  # type: ignore
from io import StringIO

from langchain.requests import RequestsWrapper
from langchain.agents.agent_toolkits.openapi import planner

from langchain.chat_models import ChatOpenAI


enc = tiktoken.encoding_for_model("text-davinci-003")


def count_tokens(s: str):
    return len(enc.encode(s))


yaml_url = "https://raw.githubusercontent.com/APIs-guru/openapi-directory/main/APIs/spotify.com/1.0.0/openapi.yaml"
yaml_url = "https://www.klarna.com/us/shopping/public/openai/v0/api-docs"
yaml_url = "http://0.0.0.0:5003/openapi.yaml"

req = requests.get(
    yaml_url,
)
yaml_text = req.text

raw_openai_api_spec = yaml.load(StringIO(yaml_text), Loader=yaml.Loader)
openapi_api_spec = reduce_openapi_spec(raw_openai_api_spec)

llm = ChatOpenAI(model_name="gpt-4", temperature=0.7, client=None)

headers = {}
openapi_requests_wrapper = RequestsWrapper(headers=headers)

openapi_agent = planner.create_openapi_agent(
    openapi_api_spec, openapi_requests_wrapper, llm
)
user_query = "What's for lunch tomorrow at Orion?"
openapi_agent.run(user_query)
