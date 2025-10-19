import streamlit as st
import google.generativeai as genai
import config

# Configure the API
genai.configure(api_key=config.GEMINI_API_KEY)

def generate_response(prompt, temperature=0.7):
    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Set generation config
        generation_config = genai.types.GenerationConfig(
            temperature=temperature
        )
        
        # Generate response
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        # Check if response is blocked
        if response.prompt_feedback.block_reason:
            return "I apologize, but I cannot provide an answer to that question."
            
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

def setup_ui():
    st.set_page_config(page_title="AI Teaching Assistant", page_icon="🎓")
    
    st.title("🎓 AI Teaching Assistant")
    st.write("Welcome! Ask any question related to your studies and get instant answers!")
    
    # Add a temperature slider
    temperature = st.slider("Response Creativity", 0.0, 1.0, 0.7, 0.1)
    
    user_input = st.text_area("Enter your question here:", height=100)

    if st.button("Get Answer"):
        if user_input:
            with st.spinner("Thinking..."):
                response = generate_response(user_input, temperature)
                st.write("### Your Question:")
                st.write(user_input)
                st.write("### AI Response:")
                st.markdown(response)
        else:
            st.warning("Please enter a question first.")

def main():
    setup_ui()

if __name__ == "__main__":
    main()
