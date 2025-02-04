import streamlit as st
import openai
from fpdf import FPDF
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# App Title
st.title("AI-Driven Proposal Automation")

# Sidebar Inputs
st.sidebar.header("Lead Information")

# Collecting Lead Information
lead_name = st.sidebar.text_input("Lead Name", "")
company_name = st.sidebar.text_input("Company Name", "")
industry = st.sidebar.selectbox(
    "Industry",
    ["Travel", "Business Payments", "Lending & Wages", "Merchant Payments", "Investments", "Other Markets"]
)
use_case = st.sidebar.multiselect(
    "Use Cases",
    ["Pay Out", "Pay In", "Cross-Currency Transactions", "Fraud Detection", "Compliance", "Automation"]
)
currency_support = st.sidebar.multiselect(
    "Required Currencies",
    ["USD", "EUR", "GBP", "AUD", "INR", "Other"]
)

additional_requirements = st.sidebar.text_area(
    "Additional Requirements",
    "e.g., custom APIs, multi-language support, detailed reporting"
)

# Generate Proposal Button
if st.sidebar.button("Generate Proposal"):
    # Validate Inputs
    if not lead_name or not company_name or not use_case or not currency_support:
        st.error("Please fill in all required fields in the sidebar.")
    else:
        with st.spinner("Generating your personalized proposal..."):
            # Prompt for GPT-3.5 Turbo
            prompt = f"""
            Generate a personalized business proposal for an embedded payment platform. 
            The proposal should be tailored to the following lead details:

            Lead Name: {lead_name}
            Company Name: {company_name}
            Industry: {industry}
            Use Cases: {', '.join(use_case)}
            Required Currencies: {', '.join(currency_support)}
            Additional Requirements: {additional_requirements}

            The proposal should highlight:
            - Benefits of the platform for their specific use cases
            - Scalability and flexibility
            - Security and compliance features
            - Cross-currency capabilities
            - Cost-effectiveness
            - Support and onboarding processes

            Write this proposal in a professional and persuasive tone.
            """

            try:
                # Call OpenAI ChatCompletion API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that generates professional business proposals."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )

                # Extract the proposal content
                proposal = response["choices"][0]["message"]["content"].strip()

                # Display the Proposal
                st.success("Proposal Generated Successfully!")
                st.markdown("### Personalized Proposal")
                st.write(proposal)

                # Generate PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, proposal)

                pdf_output = f"{lead_name}_proposal.pdf"
                pdf.output(pdf_output)

                # Option to Download Proposal as PDF
                with open(pdf_output, "rb") as pdf_file:
                    st.download_button(
                        label="Download Proposal as PDF",
                        data=pdf_file.read(),
                        file_name=pdf_output,
                        mime="application/pdf"
                    )

            except Exception as e:
                # Handle unexpected errors
                st.error(f"An error occurred while generating the proposal: {e}")

# Footer
st.markdown("---")
st.markdown("*AI-powered proposal generation. Please review and refine the content before sharing with the lead to ensure accuracy and alignment with business objectives.*")
