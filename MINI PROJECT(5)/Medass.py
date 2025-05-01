import streamlit as st 
from api_key import api_key
import model 

# Set the page configuration
st.set_page_config(page_title="MEDIAI MEDICAL SUPPORT") 
st.header("MEDIAI MEDICAL SUPPORT")

# Initialize chat history specific to this page
if "messages_chatbot_1" not in st.session_state or not isinstance(st.session_state.messages_chatbot_1, list): 
    st.session_state.messages_chatbot_1 = [] 

# Display chat messages from history on app rerun
print(f"Debug: Chat history on rerun: {st.session_state.messages_chatbot_1}")  # Debugging
for message in st.session_state.messages_chatbot_1: 
    if isinstance(message, dict) and "role" in message and "content" in message:
        with st.chat_message(message["role"]): 
            st.markdown(message["content"])
  
# Accept user input
if prompt := st.chat_input("Text a medical question here...."):
    # Debugging: Print the user input
    print(f"Debug: User input: {prompt}")

    # Validate user input before adding to chat history
    st.session_state.messages_chatbot_1.append({"role": "user", "content": prompt})

    # Debugging: Print the chat history after user input
    print(f"Debug: Chat history after user input: {st.session_state.messages_chatbot_1}")

    # Generate assistant response
    model_response = model.model(prompt)

    # Debugging: Print the model response
    print(f"Debug: Model response: {model_response}")

    # Validate model response before adding to chat history
    st.session_state.messages_chatbot_1.append({"role": "assistant", "content": model_response})

    # Debugging: Print the chat history after assistant response
    print(f"Debug: Chat history after assistant response: {st.session_state.messages_chatbot_1}")

    # Display user message in chat message container
    with st.chat_message("user"): 
        st.markdown(prompt) 

    # Display assistant response
    with st.chat_message("assistant"): 
        st.markdown(model_response)

# filepath: d:\MINI PROJECT(5)\model.py
def model(prompt):
    # Debugging: Print the input prompt
    print(f"Debug: Input to model: {prompt}")

    # Simulate processing (replace this with actual logic)
    response_data = [{"role": "user", "content": prompt}, {"role": "assistant", "content": "Sample response"}]

    # Validate each item in response_data
    for item in response_data:
        if not isinstance(item, dict) or "role" not in item or "content" not in item:
            raise ValueError(f"Invalid item format: {item}")

    # Generate a response (example logic)
    return response_data[-1]["content"]