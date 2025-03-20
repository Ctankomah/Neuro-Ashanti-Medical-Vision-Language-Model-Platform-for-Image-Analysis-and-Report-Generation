import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"), 
    model_name="llama-3.3-70b-versatile"
)

# Streamlit UI
st.title("AI Chat App with ChatGroq")
st.markdown("Talk to an advanced AI model powered by Groq!")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Type your message:", "")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get response from ChatGroq
    with st.spinner("Thinking..."):
        try:
            response = llm.invoke(user_input)  # Get response from the model
            ai_response = response.content  # Extract only the message content
        except Exception as e:
            ai_response = f"Error: {str(e)}"
        st.session_state.messages.append({"role": "ai", "content": ai_response})

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"**You:** {message['content']}")
    elif message["role"] == "ai":
        st.write(f"**AI:** {message['content']}")
