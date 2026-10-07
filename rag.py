import os
from google import genai
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from a .env file
load_dotenv()

# Initialize the Gemini client using the API key from environment variables
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
)

# Streamlit App UI
st.title("Professional Sentence Improver")
st.write("Enter a casual sentence below, select a professional variation, and let Gemini generate a final refined output.")

# User input text box
user_input = st.text_input("Your sentence:", placeholder="e.g., i want job")

# Button to trigger the initial options generation
if st.button("Generate Options"):
    if user_input.strip():
        with st.spinner("Generating professional variations..."):
            try:
                prompt = (
                    f"Provide 4 distinct, highly professional variations of this sentence: '{user_input}'. "
                    "Return ONLY the sentences, one per line, with no extra conversational filler, introduction, or numbering."
                )
                
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt
                )
                
                raw_text = response.text.strip()
                options = [line.strip("- *1234567890.").strip() for line in raw_text.split("\n") if line.strip()]
                
                if options:
                    st.session_state["options"] = options
                    # Clear any previous final output when new options are generated
                    if "final_response" in st.session_state:
                        del st.session_state["final_response"]
                else:
                    st.warning("No options were generated. Please try again.")
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a sentence first.")

# If options exist in session state, let the user select one and process it
if "options" in st.session_state and st.session_state["options"]:
    st.subheader("Select your preferred version:")
    selected_option = st.selectbox("Choose from the generated list:", st.session_state["options"])
    
    # Button to send the selected option back to Gemini for a final response
    if st.button("Generate Final Response with Selected Prompt"):
        with st.spinner("Generating final response..."):
            try:
                # Send the selected option back to Gemini with a new/extended instruction
                final_prompt = f"Elaborate or write a formal message/context utilizing this professional sentence: '{selected_option}'"
                
                final_api_response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=final_prompt
                )
                
                # Store the final response in session state
                st.session_state["final_response"] = final_api_response.text
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

    # Display the final generated response if available
    if "final_response" in st.session_state:
        st.markdown("### Final Generated Response:")
        st.success(st.session_state["final_response"])