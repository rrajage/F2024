import streamlit as st
import asyncio
from engine.langchain_agent import create_agent,run_agent
from dotenv import load_dotenv
#from openai import OpenAI

load_dotenv()
import os
# print(os.environ["OPENAI_API_KEY"])
# Client = OpenAI()

st.title("Langchain Agent")
if "memory" not in st.session_state:
    st.session_state["memory"] = [{"role":"system","content":""}]

if "agent" not in st.session_state:
    model_name = "gpt-3.5-turbo"
    st.session_state['agent'] = create_agent(model_name)

# updading the chat page with messages
for message in st.session_state["memory"]:
    if message["role"] == "assistant":
        with st.chat_message(message["role"]):
            msg = message["content"]["output"]
            if "/bot/images/dall-e" in msg:
                address = msg.split("(")[1][:-1]
                print("address:",address)
                st.image(address)
            else:
                st.markdown(msg)
    elif message["role"] == "system":
        pass
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# entering new message event handle
if prompt := st.chat_input("Your message ..."):
    st.session_state['memory'].append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    response = asyncio.run(run_agent(st.session_state["agent"],prompt))
    st.session_state['memory'].append({"role":"assistant","content":response})
    with st.chat_message("assistant"):
        if "/bot/images/dall-e" in response["output"]:
            address = response["output"].split("(")[1][:-1]
            st.image(address)
        else:
            st.markdown(response["output"])