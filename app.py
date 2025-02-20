import streamlit as st
import openai

# Set OpenAI API Key (Manually add yours)
openai.api_key = "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"

# Title & Description
st.title("📧 AI Email Generator")
st.write("Generate professional emails using AI.")

# User Input
prompt = st.text_input("Enter a short description of the email:")
start = st.text_input("Start writing the first few words (optional):")
submit_button = st.button("Generate Email")

# Email Generation
if submit_button:
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{prompt}\n\n{start}",
        temperature=0.7,
        max_tokens=200
    )
    email_text = response.choices[0].text.strip()
    st.text_area("Generated Email:", value=email_text, height=300)

    # Option to copy email
    st.download_button(label="📋 Copy Email", data=email_text, file_name="email.txt")
