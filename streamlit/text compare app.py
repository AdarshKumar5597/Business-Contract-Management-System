import streamlit as st
import fitz  # PyMuPDF
import re
from sentence_transformers import SentenceTransformer, util

# Load pre-trained models
model = SentenceTransformer("all-MiniLM-L6-v2")

# Helper function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

# Function to split text into sentences
def split_into_sentences(text):
    text = text.replace('\n', ' ').replace('\r', '')
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(r"(Mr|St|Mrs|Ms|Dr)[.]",r"\1<prd>",text)
    text = re.sub(r"[.](com|net|org|io|gov|edu|me)",r"<prd>\1",text)
    text = re.sub(r"([0-9])[.]([0-9])",r"\1<prd>\2",text)
    text = re.sub(r'\.{2,}', lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub(r"\s([A-Za-z])[.] "," \\1<prd> ",text)
    text = re.sub(r"([A-Z][.][A-Z][.](?:[A-Z][.])?) "+r"(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)",r"\1<stop> \2",text)
    text = re.sub(r"([A-Za-z])[.]([A-Za-z])[.]([A-Za-z])[.]",r"\1<prd>\2<prd>\3<prd>",text)
    text = re.sub(r"([A-Za-z])[.]([A-Za-z])[.]",r"\1<prd>\2<prd>",text)
    text = re.sub(r" (Inc|Ltd|Jr|Sr|Co)[.] "+r"(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)",r" \1<stop> \2",text)
    text = re.sub(r" (Inc|Ltd|Jr|Sr|Co)[.]",r" \1<prd>",text)
    text = re.sub(r" ([A-Za-z])[.]",r" \1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    text = text.replace("**", "")
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

# Function to generate filtered sentences
def generate_filtered_sentences(para):
    para = split_into_sentences(para)
    sentences = para
    pattern = re.compile(r'^\d+\.$')
    filtered_sentences = [sentence for sentence in sentences if not pattern.match(sentence.strip())]
    return filtered_sentences

# Streamlit app
def main():
    st.title("PDF Text Comparison Tool")

    st.header("Upload Files")
    template_file = st.file_uploader("Upload Template PDF", type="pdf")
    new_file = st.file_uploader("Upload New PDF", type="pdf")

    if template_file is not None and new_file is not None:
        # Extract text from the uploaded PDF files
        template_text = extract_text_from_pdf(template_file)
        new_text = extract_text_from_pdf(new_file)

        # Generate filtered sentences
        template_sentences = generate_filtered_sentences(template_text)
        new_sentences = generate_filtered_sentences(new_text)

        # Encode sentences
        template_embeddings = model.encode(template_sentences, convert_to_tensor=True)
        new_embeddings = model.encode(new_sentences, convert_to_tensor=True)

        # Calculate cosine similarity
        cos_sim = util.pytorch_cos_sim(template_embeddings, new_embeddings)

        # Find the most similar sentences
        most_similar_sentences = []
        for i in range(len(template_sentences)):
            max_sim = 0
            for j in range(len(new_sentences)):
                if cos_sim[i][j] > max_sim:
                    max_sim = cos_sim[i][j]
                    most_similar_sentences.append((max_sim.item(), template_sentences[i], new_sentences[j]))

        # Display results in two side-by-side columns
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Template Text with Differences Highlighted")
            template_highlighted = []
            for sim, template_sentence, new_sentence in most_similar_sentences:
                color = 'red' if sim < 0.5 else ('#A89812' if sim < 0.8 else 'green')
                template_highlighted.append(f"<span style='color:{color}'>{template_sentence}</span>")
            st.markdown("<div style='background-color:white; padding:10px;'>" + "<br>".join(template_highlighted) + "</div>", unsafe_allow_html=True)

        with col2:
            st.subheader("New Text with Differences Highlighted")
            new_highlighted = []
            for sim, template_sentence, new_sentence in most_similar_sentences:
                color = 'red' if sim < 0.5 else ('#A89812' if sim < 0.8 else 'green')
                new_highlighted.append(f"<span style='color:{color}'>{new_sentence}</span>")
            st.markdown("<div style='background-color:white; padding:10px;'>" + "<br>".join(new_highlighted) + "</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
