import streamlit as st
import requests
import smtplib
import re
from email.message import EmailMessage

# Hugging Face API details
HF_API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
HF_API_KEY = "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"

# Email sender details
EMAIL_SENDER = "mailmatic55@gmail.com"
EMAIL_PASSWORD = "rrfuxfoccveuperi"

EMAIL_TYPES = ["Job Application", "Business Inquiry", "Follow-up", "Apology", "Thank You", "Custom", "Invitation", "Others"]
SALUTATIONS = ["Dear", "Hello", "Respected", "Hi"]

# Function to validate email format
def is_valid_email(email):
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email) is not None

# Function to validate required fields
def validate_inputs(inputs):
    missing_fields = [field for field, value in inputs.items() if not value or not str(value).strip()]
    return f"⚠ Please fill in: {', '.join(missing_fields)}" if missing_fields else None

# Function to generate email content
def generate_email(email_type, salutation, recipient_name, your_name, description):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    prompt = (f"{salutation} {recipient_name},\n\n")

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True,
            "repetition_penalty": 1.2
        }
    }

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response_data = response.json()

        # Extract generated text properly
        if isinstance(response_data, list) and response_data:
            email_text = response_data[0].get('generated_text', '')
        elif isinstance(response_data, dict) and 'generated_text' in response_data:
            email_text = response_data['generated_text']
        else:
            return "⚠ Unexpected API response format. Try again."

        # **Remove unnecessary text**
        unwanted_phrases = [
            "Generated Email:", "Instructions:", "Here is", "Sure,", "Of course,", 
            "Here’s a sample email:", "Certainly,", "Hope this helps!", "Write a formal",
            "Do not include any instructions", "Ensure the email is"
        ]
        
        email_lines = email_text.split("\n")
        clean_email = "\n".join([line for line in email_lines if not any(phrase in line for phrase in unwanted_phrases)])

        return clean_email.strip() if clean_email else "⚠ Error: No valid email generated."

    except Exception as e:
        return f"❌ Error generating email: {str(e)}"

# Function to send email
def send_email(recipient_email, subject, body):
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = recipient_email
        msg.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        return "✅ Email sent successfully!"
    except Exception as e:
        return f"❌ Email sending failed: {str(e)}"

# Theme Customization
st.title("🎨 Customize Theme")
theme_color = st.color_picker("Pick a Theme Color", "#007BFF")
bg_color = st.color_picker("Pick a Background Color", "#ffffff")
text_color = st.color_picker("Pick a Text Color", "#000000")

# Apply Custom CSS for Styling
custom_css = f"""
    <style>
        body {{
            background-color: {bg_color};
            color: {text_color};
        }}
        .stTextInput, .stTextArea, .stSelectbox {{
            border-radius: 10px;
            border: 1px solid #ccc;
        }}
        .block-container {{
            padding: 2rem;
            border-radius: 15px;
            background-color: white;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
        }}
        .stButton>button {{
            border-radius: 10px;
            background-color: {theme_color};
            color: white;
            font-size: 16px;
        }}
        .stButton>button:hover {{
            background-color: #0056b3;
        }}
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.title("📧 MailMatic")
st.write("From thoughts to inbox!")

with st.expander("✍️ Enter Email Details"):
    email_type = st.selectbox("Select Email Type", EMAIL_TYPES)
    your_name = st.text_input("Your Name", placeholder="John Doe")
    salutation = st.selectbox("Select Salutation", SALUTATIONS)
    recipient_name = st.text_input("Recipient's Name", placeholder="Jane Smith")
    recipient_email = st.text_input("Recipient's Email Address", placeholder="jane@example.com")
    subject = st.text_input("Email Subject", placeholder="Subject of your email")
    description = st.text_area("Email Description (Reason for writing this email)", placeholder="Enter details here...")

# Generate Email Button
if "email_generated" not in st.session_state:
    if st.button("📝 Generate Email", use_container_width=True):
        inputs = {
            "Your Name": your_name,
            "Recipient's Name": recipient_name,
            "Recipient's Email": recipient_email,
            "Email Subject": subject,
            "Email Description": description,
        }

        validation_result = validate_inputs(inputs)

        if validation_result:
            st.error(validation_result)
        elif not is_valid_email(recipient_email):
            st.error("⚠ Invalid email format! Please enter a valid email.")
        else:
            st.session_state.email_content = generate_email(email_type, salutation, recipient_name, your_name, description)
            st.session_state.email_generated = True
            st.rerun()

# Display Generated Email
if "email_generated" in st.session_state and st.session_state.email_generated:
    st.text_area("📨 Generated Email:", st.session_state.email_content, height=250)
    if st.button("📩 Accept & Send Email", use_container_width=True):
        result = send_email(recipient_email, subject, st.session_state.email_content)
        st.success(result)

