import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & CONFIGURATION ---
# IMPORTANT: Use st.secrets or an environment variable in production!
API_KEY = "AIzaSyBsoaTDy0_zkPSrBMMMdmsEfDZ3idEgiyI" 
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Gemini Pro Chat", page_icon="⚡")
st.title("⚡ Gemini Chatbot")

# --- 2. MODEL INITIALIZATION ---
# Using 'gemini-1.5-flash-latest' often resolves the 404 error 
# because it routes to the most stable production endpoint.
MODEL_ID = "gemini-2.5-flash" 

if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(MODEL_ID)
    st.session_state.chat_session = model.start_chat(history=[])

# --- 3. DISPLAY CHAT HISTORY ---
# We loop through the history and use streamlit's chat UI
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# --- 4. CHAT INPUT & STREAMING RESPONSE ---
if prompt := st.chat_input("How can I help you today?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response with a "streaming" effect
    with st.chat_message("assistant"):
        message_placeholder = st.empty() # Create an empty container for the stream
        full_response = ""
        
        try:
            # Setting stream=True makes the bot feel much faster
            response = st.session_state.chat_session.send_message(prompt, stream=True)
            
            for chunk in response:
                full_response += chunk.text
                # Update the UI with the text accumulated so far
                message_placeholder.markdown(full_response + "▌")
            
            # Final update to remove the cursor icon
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
            if "404" in str(e):
                st.info("Tip: Try changing the model ID to 'gemini-1.5-flash' or check your Google AI Studio billing/plan.")