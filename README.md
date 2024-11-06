# Streamlit Webapp 
## Installation
Note: You need Python 3.10 or above. 
1. Create a venv: 
```python -m venv path-to-venv```  
venv stands for Virtual Environment.
2. Activate the venv:
```source path-to-venv/bin/activate```
3. Install requirements.txt:
```pip install -r requirements.txt```
## Running
* **OpenAI Bot:**  
1. Go to ```bot/openai-bot```   
2. run ```streamlit run bot-openai-chat.py```
* **LangChain Bot:**
1. Go to ```bot/langchain-bot```   
2. run ```streamlit run bot-langchain-chat.py```
* **Indexing:**
1. Go to ```bot/rag_indexing```
2. run ```python indexing.py [url]```. For our example, url by ```https://lilianweng.github.io/posts/2023-06-23-agent/```

## OpenAI Bot
Pure OpenAI bots with a Streamlit webapp as UI.
* **OpenAI Chatbot**
    * **Models:** gpt-3.5-turbo, gpt-4-turbo-preview, gpt-4-vision-preview
* **OpenAI Image Bot**
    * **Models:** dall-e-3, dall-e-2

## Langchain Agent Bot
A Langchain agent uses an LLM to make a decision to use which tools. The current app has to 4 tools and uses GPT3.5-Turbo for decision making as well as answering some questions that can answer directly. The model is not good at following the descriptions. It is supposed to pass through the answers, but it changes some words in the final answer.
* **List of Tools**
1. GPT4-Turbo_General_Assistant
2. GPT4-Turbo_Code_Assistant
3. GPT35-Turbo_Code_Assistant
4. Dalle3_Image_Generator
