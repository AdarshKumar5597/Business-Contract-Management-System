import streamlit as st
from transformers import BertTokenizerFast, AutoModelForTokenClassification, pipeline
import pdfplumber
import matplotlib.pyplot as plt
import pandas as pd

# Function to extract text from PDF using pdfplumber
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Load the pre-trained model and tokenizer
tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
model = AutoModelForTokenClassification.from_pretrained("Contract-Validator-Model")
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer)

# Function to highlight entities in the text
def highlight_entities(text, entities):
    highlighted_text = text
    for entity in sorted(entities, key=lambda x: x['start'], reverse=True):
        start = entity['start']
        end = entity['end']
        label = entity['entity']
        highlighted_text = (
            highlighted_text[:start]
            + f"<mark style='background-color: yellow; color: black;'>{highlighted_text[start:end]}</mark>"
            + highlighted_text[end:]
        )
    return highlighted_text

# Streamlit app layout
st.set_page_config(layout="wide")
st.title("Named Entity Recognition from PDF")
st.write("Upload a PDF file, and the app will extract named entities and their labels.")

# Main layout
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="pdf_uploader")

if uploaded_file is not None:
    # Extract text from the uploaded PDF
    text = extract_text_from_pdf(uploaded_file)
    
    # Apply the NER model
    ner_results = ner_pipeline(text)
    
    # Extract unique entity labels
    entity_labels = list(set([entity['entity'] for entity in ner_results]))
    
    # Sidebar for entity filtering and distribution
    st.sidebar.header("Settings")
    selected_labels = st.sidebar.multiselect("Select entity types to display", options=entity_labels, default=entity_labels)
    
    # Filter results based on selected labels
    filtered_results = [entity for entity in ner_results if entity['entity'] in selected_labels]

    # Prepare data for visualization
    entity_counts = pd.Series([entity['entity'] for entity in filtered_results]).value_counts()

    # Plot the distribution of entities
    st.sidebar.header("Entity Distribution")
    fig, ax = plt.subplots()
    entity_counts.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_xlabel("Entity Label")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of Named Entities")
    st.sidebar.pyplot(fig)
    
    # Display the filtered results in a table
    st.header("Extracted Entities")
    entities_df = pd.DataFrame(filtered_results)
    st.table(entities_df[['word', 'entity']])
    
    # Highlight entities in the text
    highlighted_text = highlight_entities(text, filtered_results)
    
    # Display the highlighted text
    st.header("Highlighted Text with Entities")
    st.markdown(
        f"<div style='white-space: pre-wrap; font-family: Courier; background-color: #f0f0f0; color: black; padding: 1rem; border-radius: 5px; overflow-x: scroll;'>{highlighted_text}</div>",
        unsafe_allow_html=True
    )
else:
    st.info("Please upload a PDF file to get started.")

# Additional CSS to improve layout
st.markdown(
    """
    <style>
    .css-1aumxhk {
        padding-top: 2rem;
    }
    .css-145kmo2 {
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)
