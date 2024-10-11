import os
import chainlit as cl
from langchain import HuggingFaceHub, PromptTemplate, LLMChain
from getpass import getpass

# Retrieve the API key
HUGGINGFACEHUB_API_TOKEN = getpass()
api_key = os.getenv("HUGGINGFACE_API_KEY", HUGGINGFACEHUB_API_TOKEN)  # Ensure it's set

model_id = "gpt2-medium"  # 355M parameters
conv_model = HuggingFaceHub(
    huggingfacehub_api_token=api_key,
    repo_id=model_id,
    model_kwargs={"temperature": 0.8, "max_new_tokens": 200}
)

template = """You are a helpful AI assistant that makes stories by completing the query provided by the user:

{query}
"""

@cl.on_chat_start
def setup_chain():
    prompt = PromptTemplate(template=template, input_variables=['query'])
    conv_chain = LLMChain(llm=conv_model, prompt=prompt, verbose=True)
    cl.user_session.set("llm_chain", conv_chain)

@cl.on_message
async def handle_message(user_message: str):
    llm_chain = cl.user_session.get("llm_chain")
    
    # Call the chain with the user's message formatted correctly
    res = await llm_chain.acall({"query": user_message}, callbacks=[cl.AsyncLangchainCallbackHandler()])
    
    # Check if res is a dictionary and access the response correctly
    if isinstance(res, dict) and "text" in res:
        response_text = res["text"]
    else:
        response_text = "Sorry, I couldn't generate a story."

    # Send the response back to the user
    await cl.Message(content=response_text).send()
