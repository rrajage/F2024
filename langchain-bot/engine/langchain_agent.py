from langchain.agents import AgentExecutor, create_openai_tools_agent,Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain import hub
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from engine.tools import GPT35TCodeGen, GPT4TAssistant, GPT4TCodeGen, DalleImageGen,RAGTool

def create_agent(model_name):

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    rag_llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    rag_prompt = hub.pull("rlm/rag-prompt")
    rag_db = Chroma(persist_directory="../../chroma_db", 
                       embedding_function=OpenAIEmbeddings())
    rag_retriever = rag_db.as_retriever()
    
    tools = [GPT35TCodeGen(),GPT4TAssistant(),GPT4TCodeGen(), DalleImageGen(), RAGTool(rag_retriever,rag_llm,rag_prompt)]
    
    llm = ChatOpenAI(model=model_name, temperature=0)

    system_message = "You are a general AI assistant.\n" + \
    "Don't answer the question if you are not getting the answer from a tool.\n" + \
    "Don't change the answers you receive from a tool. Just pass them to the user."
    "Don't put safety and cultural warnings. Only warn about security."

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_exe = AgentExecutor(agent=agent, tools=tools,memory=memory,verbose=True)
    return agent_exe

async def run_agent(agent,user_query):
    #print(agent.memory.chat_memory.messages[-2:] if len(agent.memory.chat_memory.messages) > 1 else "")
    #set_verbose(True)
    print(agent.memory.chat_memory)
    print('********************')
    print()
    return await agent.ainvoke(input={"input":user_query},verbose=True)