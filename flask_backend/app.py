# app.py
from flask import Flask, jsonify, request, send_file
from fpdf import FPDF
from NER import getNerHighlightedTexts
from COMPARE import compare
from SUMMARIZER import getSummary
import fitz
from flask_cors import CORS, cross_origin
import pymupdf
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import pickle
import re

app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})



def highlight_entities_in_pdf(pdf_path, output_path, ner_results, labels):
    # Create a label-to-color mapping
    label_colors = {label: pymupdf.pdfcolor[color] for label, color in labels}

    # Open the input PDF
    doc = fitz.open(pdf_path)

    # Iterate through each page in the PDF
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Iterate through each NER result
        for result in ner_results:
            entities = result['entities']
            line = result['line']
            for entity in entities:
                word = line[entity['start']:entity['end']]
                tag = entity['tag']
                if tag in label_colors:
                    color = label_colors[tag]
                    
                    # Search for the word in the page text
                    rects = page.search_for(word)
                    
                    # Highlight all occurrences of the word
                    for rect in rects:
                        highlight = page.add_highlight_annot(rect)
                        highlight.set_colors(stroke=color)  # Set the highlight color
                        highlight.update()
    
    # Save the output PDF with highlights
    doc.save(output_path)



def create_pdf_from_ner_results(result):
        labels = [('DOC_NAME', "red"), ('AGMT_DATE', "yellow"), ('PARTY', "cyan"), ('AMOUNT', "blue")]
        pdf = FPDF()
        pdf.add_page()  # Start with the first page
        pdf.set_font('Arial', 'B', 8.0)
        for line in result:
            text = line['line']
            print(text)
            # Check if the current Y position exceeds the limit
            if pdf.get_y() + 10 > 297 - pdf.b_margin:  # A4 page height is 297mm
                pdf.add_page()
            pdf.cell(ln=0, h=5.0, align='L', w=0, txt=text, border=0)
            pdf.ln(5)  # Move to the next line
        pdf.output('test.pdf', 'F')
        highlight_entities_in_pdf('test.pdf', 'output.pdf', result, labels)
        
        


def create_pdf_from_compare_results(original_contract_cluster, template_cluster, filtered_sentences, colors):
    pdf = FPDF()
    
    # Helper function to add text with color
    def add_colored_text(text, color):
        if isinstance(color, tuple) and len(color) == 3:
            r, g, b = color
        else:
            r, g, b = (0, 0, 0)  # Default to black if color is not valid
        pdf.set_text_color(r, g, b)
        pdf.cell(ln=0, h=5.0, align='L', w=0, txt=text, border=0)
        pdf.ln(5)
        pdf.set_text_color(0, 0, 0)  # Reset to black for any subsequent text

    # Highlighted Contract Template
    pdf.add_page()
    pdf.set_font('Arial', 'B', 24.0)
    pdf.cell(0, 10, "HIGHLIGHTED CONTRACT TEMPLATE", 0, 1, 'C')
    
    pdf.set_font('Arial', '', 8.0)
    for key, sentences in template_cluster.items():
        color = colors[key] 
        for sentence in sentences:
            if pdf.get_y() + 10 > 297 - pdf.b_margin: 
                pdf.add_page()
            add_colored_text(sentence, color)
    
    # Highlighted Original Contract
    pdf.add_page()
    pdf.set_font('Arial', 'B', 24.0)
    pdf.cell(0, 10, "HIGHLIGHTED ORIGINAL CONTRACT", 0, 1, 'C')

    pdf.set_font('Arial', '', 8.0)
    sentence_is_present = False
    for sentence in filtered_sentences:
        sentence_is_present = False
        for cluster in original_contract_cluster:
            if sentence in original_contract_cluster[cluster]:
                sentence_is_present = True
                color = colors[cluster]
                if pdf.get_y() + 10 > 297 - pdf.b_margin: 
                    pdf.add_page()
                add_colored_text(sentence, color)
        if not sentence_is_present:
            if pdf.get_y() + 10 > 297 - pdf.b_margin: 
                pdf.add_page()
            add_colored_text(sentence, (0, 0, 0))
    
    pdf.output('compare.pdf', 'F')
    
    
def create_pdf_from_summary_results(summary_list):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 24.0)
    pdf.cell(0, 10, "SUMMARY", 0, 1, 'C')
    
    pdf.set_auto_page_break(auto=True, margin=15)
    for summary in summary_list:
        # Original Text
        pdf.set_font('Arial', '', 8.0)
        pdf.set_text_color(0, 0, 255)
        pdf.multi_cell(0, 5.0, txt=summary['original_text'], border=0)
        
        pdf.set_font('Arial', 'B', 6.0)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, "Summary of the Above highlighted Part - ", 0, 1, 'C')
        
        # Summary Text
        pdf.set_font('Arial', '', 8.0)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 5.0, txt=summary['summary'], border=0)
        
        # Add space between summaries
        pdf.ln(10)
    
    pdf.output('summary.pdf', 'F')

    
    

@app.route('/')
@cross_origin()
def home():
    return 'Hello, Flask!'

@app.route('/ner', methods=['GET', 'POST'])
@cross_origin()
def ner():
    pdf_file = request.files['pdfFile']
    print(pdf_file)
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")

    all_text = chr(12).join([page.get_text() for page in doc])
        
    # print(all_text)
     
    ner_results = getNerHighlightedTexts(all_text)
    
    print(ner_results)
    
    create_pdf_from_ner_results(ner_results)
    
    
    ner_results = {
        'success': 'true',
        'pdfUrl': 'http://127.0.0.1:5000/getnerpdf'
    }
    
    return jsonify(ner_results)


@app.route('/getnerpdf', methods=['GET', 'POST'])
@cross_origin()
def getNEROutputPdf():
    return send_file('output.pdf', as_attachment=True)


@app.route('/getcomparepdf', methods=['GET', 'POST'])
@cross_origin()
def getCOMPAREOutputPdf():
    return send_file('compare.pdf', as_attachment=True)

@app.route('/getsummarypdf', methods=['GET', 'POST'])
@cross_origin()
def getSUMMARYOutputPdf():
    return send_file('summary.pdf', as_attachment=True)

@app.route('/getclassificationpdf', methods=['GET'])
@cross_origin()
def get_classification_pdf():
    return send_file('classification_results.pdf', as_attachment=True)


@app.route('/compare', methods=['GET', 'POST'])
@cross_origin()
def compareboth():
    
    original_pdf_file = request.files['originalPdfFile']
    template_pdf_file = request.files['templatePdfFile']

    originalDoc = fitz.open(stream=original_pdf_file.read(), filetype="pdf")
    templateDoc = fitz.open(stream=template_pdf_file.read(), filetype="pdf")

    original_all_text = chr(12).join([page.get_text() for page in originalDoc])
    template_all_text = chr(12).join([page.get_text() for page in templateDoc])
    
    
    original_contract_cluster, template_cluster, filtered_sentences = compare(template_all_text, original_all_text)
    colors = [
        (255, 0, 0),    # red
        (0, 255, 0),    # green
        (0, 0, 255),    # blue
        (255, 255, 0),  # yellow
        (255, 0, 255),  # magenta
        (0, 255, 255),  # cyan
        (255, 255, 255),# white
        (128, 128, 128),# grey
        (0, 0, 0),      # black
        (128, 0, 128)   # purple
    ]
    
    
    create_pdf_from_compare_results(original_contract_cluster, template_cluster, filtered_sentences, colors)
    
    result = {
        'success': 'true',
        'pdfUrl': 'http://127.0.0.1:5000/getcomparepdf'
    }
    
    return jsonify(result)


@app.route('/summarize', methods=['GET', 'POST'])
@cross_origin()
def summarize():
    pdf_file = request.files['pdfFile']
    print(pdf_file)
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")

    all_text = chr(12).join([page.get_text() for page in doc])
    
    start = 0
    max_word_limit = 1000
    
    # Split the text into chunks of 1000 words
    chunks = []
    while start < len(all_text):
        chunks.append(all_text[start:start + max_word_limit])
        start += max_word_limit
    
    all_text = chunks
    
    overall_summary_list = []
    for text in all_text:
        summary = getSummary(text)
        print(summary)
        overall_summary_list.append({'original_text': text, 'summary': summary[0]['summary_text']})
        
    create_pdf_from_summary_results(overall_summary_list)
    
    summary_results = {
        'success': 'true',
        'pdfUrl': 'http://127.0.0.1:5000/getsummarypdf'
    }
    
    return jsonify(summary_results)


def extract_text_from_pdf(pdf_file):
    document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

# Function to clean text
def clean_text(text):
    text = text.lower()
    text = text.replace('\n', ' ')
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Load the tokenizer
tokenizer = BertTokenizer.from_pretrained('contract_classifier_tokenizer')

# Load the model
model = BertForSequenceClassification.from_pretrained('contract_classifier_model')
model.eval()

# Load the label encoder
with open('clause_type_encoder.pkl', 'rb') as f:
    clause_type_encoder = pickle.load(f)

def classify_contract_clauses(contract_text):
    # Clean text
    text = clean_text(contract_text)

    # Split text into clauses
    clauses = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

    # Clean each clause
    cleaned_clauses = [clean_text(clause) for clause in clauses]

    # Tokenize and encode each clause
    encoded_clauses = [tokenizer(clause, return_tensors='pt', padding=True, truncation=True, max_length=512) for clause in cleaned_clauses]

    # Move the model to GPU if available
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    predicted_clause_types = []

    # Predict clause type for each clause
    for inputs in encoded_clauses:
        inputs = {key: val.to(device) for key, val in inputs.items()}
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            predicted_class_indices = torch.argmax(logits, dim=1)
            predicted_clause_types.extend(clause_type_encoder.inverse_transform(predicted_class_indices.cpu().numpy()))

    return predicted_clause_types

def create_pdf_from_classifications(original_predictions, template_predictions):
    pdf = FPDF()
    pdf.add_page()
    
    # Original Contract Predictions
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, "Original Contract Predictions", 0, 1, 'C')
    
    pdf.set_font('Arial', '', 12)
    for idx, clause_type in enumerate(original_predictions):
        pdf.cell(0, 10, f"Clause {idx+1}: {clause_type}", 0, 1)
    
    # Template Contract Predictions
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, "Template Contract Predictions", 0, 1, 'C')
    
    pdf.set_font('Arial', '', 12)
    for idx, clause_type in enumerate(template_predictions):
        pdf.cell(0, 10, f"Clause {idx+1}: {clause_type}", 0, 1)
    
    pdf.output('classification_results.pdf', 'F')\


@app.route('/classify', methods=['POST'])
@cross_origin()
def classify():
    if 'originalPdfFile' not in request.files or 'templatePdfFile' not in request.files:
        return jsonify({'error': 'Both original and template PDF files are required'}), 400
    
    original_pdf_file = request.files['originalPdfFile']
    template_pdf_file = request.files['templatePdfFile']
    
    original_text = extract_text_from_pdf(original_pdf_file)
    template_text = extract_text_from_pdf(template_pdf_file)
    
    if not original_text or not template_text:
        return jsonify({'error': 'Failed to extract text from one or both PDFs'}), 500
    
    original_predictions = classify_contract_clauses(original_text)
    template_predictions = classify_contract_clauses(template_text)
    
    create_pdf_from_classifications(original_predictions, template_predictions)
    
    response = {
        'success': 'true',
        'pdfUrl': 'http://127.0.0.1:5000/getclassificationpdf'
    }
    
    return jsonify(response)
    


if __name__ == '__main__':
    app.run(debug=True)
