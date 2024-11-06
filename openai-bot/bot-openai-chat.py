import streamlit as st
from dotenv import load_dotenv
from openai_engine import OpenAIEngine

load_dotenv()
engine = OpenAIEngine()

st.title("OpenAI API")

# Define options for the dropdown lists
chat_model_list = ["gpt-3.5-turbo","gpt-4-turbo-preview","gpt-4-vision-preview"]
image_model_list = ["dall-e-3","dall-e-2"]
chat_prompt_dictionary = {
"Code Assistant":
"""You are a code assistant. 
Answer questions in code with minimal to no explanation.
Put brief one line comments on the code for explanation\
    """,
"General Assistant": 
"""You are a general AI assistant. 
Answer questions with minimal and to the point explanation.
Don't put safety and cultural warnings. Only warn about security."""
    }

# Create the first dropdown in the sidebar and update session state: generation type
st.session_state["app_type_option"] = st.sidebar.selectbox("Generation Type:",["Chatting","Image Generation"])
st.sidebar.write(f'You are in {st.session_state.app_type_option} mode.')

# list of models is changed  based on the type of generation
model_list  = chat_model_list if st.session_state.app_type_option == "Chatting" else image_model_list
# second dropdown: list of models dropdown
st.session_state["selected_option_1"] = st.sidebar.selectbox('Models:', model_list )

# third dropdown in the sidebar and update session state: assistant type
if st.session_state.app_type_option == "Chatting":
    st.session_state.selected_option_2 = st.sidebar.selectbox('Prompts:', chat_prompt_dictionary.keys()) 
    # Display the selected options
    st.sidebar.write(f'You are using "{st.session_state.selected_option_1}\
            " together with "{st.session_state.selected_option_2}" prompt.')
else:
    st.sidebar.write(f'You are using "{st.session_state.selected_option_1}".')

# defining openai engine
engine.change(st.session_state.app_type_option,
              st.session_state.selected_option_1,
              chat_prompt_dictionary[st.session_state.selected_option_2])

# updading the chat page with messages
for message in st.session_state["memory"]:
    if message["role"] == "image assistant":
        with st.chat_message("assistant"):
            st.image(message["content"])
    elif message["role"] == "system":
        pass
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# entering new message event handle
if prompt := st.chat_input("Start chat ..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if st.session_state.app_type_option == "Chatting":
            engine.generate_answer(prompt)
        else:
            engine.generate_image(prompt)

# Load image history on app start
history_file = os.path.join(st.session_state["image_folder"], "image_history.json")
if os.path.exists(history_file):
    with open(history_file, "r") as f:
        history_data = json.load(f)
        for item in history_data:
            st.session_state["memory"].append({"role": "image assistant", "content": item["path"]})

    
