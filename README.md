MailMatic - AI-Powered Email Generator

Overview

MailMatic is an AI-powered email generator built using Streamlit and the Falcon-7B model from Hugging Face. It allows users to generate professional emails based on different categories and send them directly via Gmail.

Features

AI-generated emails using the Falcon-7B model

Multiple email categories (Job Application, Business Inquiry, Follow-up, etc.)

Customizable salutation and recipient details

Email validation and required field checks

Gmail integration for sending emails

Theme customization (color, background, text color)

Installation

Prerequisites

Ensure you have Python installed (Python 3.8+ recommended). You also need to install the required dependencies.

Install Dependencies

Run the following command:

pip install -r requirements.txt

Usage

Running the App

Start the Streamlit app with the command:

streamlit run app.py

How to Use

Open the app in your browser.

Select an email type from the dropdown.

Enter your name, recipient’s name, email address, subject, and a description.

Click "Generate Email" to get an AI-generated email.

Review the generated email and click "Accept & Send Email" to send it.

API Information

This application uses the Hugging Face Falcon-7B model for AI-generated email content. Ensure you replace HF_API_KEY with your own API key for authentication.

Gmail Integration

The application uses Gmail’s SMTP service to send emails.

Ensure you replace EMAIL_SENDER and EMAIL_PASSWORD with valid credentials.

If using Gmail, enable "Less Secure Apps" or create an App Password for security.

Security Warning

DO NOT expose API keys or email credentials in public repositories. Store them securely in environment variables or a secrets manager.

Contributing

Feel free to fork this repository and improve the project! Pull requests are welcome.

License

This project is licensed under the MIT License.

