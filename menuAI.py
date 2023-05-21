from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain.tools import AIPluginTool
from langchain.memory import SimpleMemory
from datetime import date
from dotenv import load_dotenv

load_dotenv()


tool = AIPluginTool.from_plugin_url("http://0.0.0.0:5003/.well-known/ai-plugin.json")

llm = ChatOpenAI(temperature=0.7)
tools = load_tools(["requests_all"])
tools += [tool]

agent_chain = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)


question = "What's for lunch tomorrow at Orion?"
transformed_question = (
    "Today is: " + date.today().strftime("%Y-%m-%d") + "\n" + question
)

resp = agent_chain.run(transformed_question)
print("RESP", resp)
