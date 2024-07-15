from transformers import AutoModelForTokenClassification, pipeline, BertTokenizerFast
import streamlit as st
from typing import List, Tuple, Any, Optional, Dict


tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
model_fine_tuned = AutoModelForTokenClassification.from_pretrained("contract-validator-model")
cvnlp = pipeline("ner", model=model_fine_tuned, tokenizer=tokenizer)

def combine_entities(ner_results):
    combined_entities = []
    current_entity = None

    for entity in ner_results:
        if entity['entity'].startswith('B-'):
            if current_entity:
                combined_entities.append(current_entity)
            current_entity = {
                'word': entity['word'].replace('#', ''),
                'start': entity['start'],
                'end': entity['end'],
                'tag': entity['entity'][2:]
            }
        elif entity['entity'].startswith('I-') and current_entity:
            if entity['entity'][2:] == current_entity['tag']:
                if entity['entity'] == 'I-AMOUNT' or entity['entity'] == 'I-AGMT_DATE':
                    current_entity['word'] += entity['word'].replace('#', '')
                else:
                    current_entity['word'] += ' ' + entity['word'].replace('#', '')
                current_entity['end'] = entity['end']
    if current_entity:
        combined_entities.append(current_entity)

    return combined_entities


# business_contract = '''
# $10,000
# Business Contract Agreement

# This Business Contract Agreement (the "Agreement") is made and entered into as of July 15, 2024, by and between:

# Party A:
# Name: SolarTech Solutions Inc.
# Address: 123 Solar Park Drive, San Diego, CA 92101
# Contact Information: (555) 678-9101, contact@solartech.com

# Party B:
# Name: GreenWave Marketing Group
# Address: 456 Eco Street, Portland, OR 97204
# Contact Information: (555) 234-5678, info@greenwavemarketing.com

# Recitals

# WHEREAS, SolarTech Solutions Inc. is engaged in the business of providing solar energy solutions and related services;

# WHEREAS, GreenWave Marketing Group is engaged in the business of providing marketing and advertising services;

# WHEREAS, SolarTech Solutions Inc. desires to engage GreenWave Marketing Group to provide certain marketing services, and GreenWave Marketing Group agrees to provide such services under the terms and conditions set forth in this Agreement;

# NOW, THEREFORE, in consideration of the mutual covenants and promises herein contained, the parties hereto agree as follows:

# 1. Services Provided

# GreenWave Marketing Group agrees $10,000 to provide the following services to SolarTech Solutions Inc.:

# Development and implementation of a comprehensive marketing strategy for solar energy products.
# Social media management and content creation for platforms including Facebook, Twitter, Instagram, and LinkedIn.
# Design and distribution of promotional materials, including brochures, flyers, and digital advertisements.
# Conducting market research and analysis to identify new opportunities for business growth.
# 2. Compensation

# SolarTech Solutions Inc. agrees to pay GreenWave Marketing Group a total fee of $60,000 for the services described in Section 1.
# Payment will be made in six equal installments of $10,000 each, payable at the beginning of each month.


# 3. Term and Termination
# This Agreement shall commence on August 1, 2024, and continue until January 31, 2025, unless terminated earlier in accordance with this Section.
# Either party may terminate this Agreement with 30 days' written notice to the other party.
# Upon termination, GreenWave Marketing Group shall be entitled to payment for services rendered up to the termination date.


# 4. Confidentiality
# Both parties agree to maintain the confidentiality of any proprietary or confidential information disclosed during the term of this Agreement.
# This obligation shall survive the termination of this Agreement.


# 5. Intellectual Property
# Any materials created by GreenWave Marketing Group in the course of providing services to SolarTech Solutions Inc. shall be the property of SolarTech Solutions Inc.
# GreenWave Marketing Group agrees to transfer all rights, title, and interest in such materials to SolarTech Solutions Inc. upon receipt of final payment.


# 6. Indemnification
# Each party agrees to indemnify, defend, and hold harmless the other party from any claims, damages, or liabilities arising out of the performance of this Agreement.

# 7. Governing Law
# This Agreement shall be governed by and construed in accordance with the laws of the State of California, without regard to its conflict of law principles.
# 8. Entire Agreement

# This Agreement constitutes the entire agreement between the parties and supersedes all prior understandings, agreements, or representations, whether written or oral, regarding the subject matter herein.
# 9. Amendments

# Any amendments or modifications to this Agreement must be made in writing and signed by both parties.
# 10. Notices

# Any notice required or permitted to be given under this Agreement shall be in writing and sent to the addresses provided above.
# IN WITNESS WHEREOF, the parties hereto have executed this Business Contract Agreement as of the day and year first above written.

# SolarTech Solutions Inc.:
# By: _________________________
# Name: Michael Johnson
# Title: CEO
# Date: July 15, 2024

# GreenWave Marketing Group:
# By: _________________________
# Name: Emily Thompson
# Title: Managing Director
# Date: July 15, 2024
# '''

# print(int(len(business_contract)/512) + 1)
# lines = business_contract.splitlines()


def text_highlighter(
    text: str,
    labels: List[Tuple[Any, Any]],
    selected_label: Optional[str] = None,
    annotations: Optional[List[Dict[Any, Any]]] = None,
    key: Optional[str] = None,
    show_label_selector: bool = True,
    text_height: Optional[int] = None,
) -> str:
    annotations = [] if annotations is None else annotations
    label_names = [item[0] for item in labels]
    colors = [item[1] for item in labels]
    annotations = [
        {**annotation, "color": colors[label_names.index(annotation["tag"])]}
        for annotation in annotations if annotation["tag"] in label_names
    ]
    print("ANNOTATIONS:", annotations)
    selected_label = label_names[0] if selected_label is None else selected_label

    # Process annotations and generate highlighted text
    def get_highlighted_text(annotations, text):
        highlighted_text = ""
        last_index = 0
        for annotation in sorted(annotations, key=lambda x: x["start"]):
            start, end, color, tag = annotation["start"], annotation["end"], annotation["color"], annotation["tag"]
            word = text[start:end]

            highlighted_text += f'<span style="background-color: {color}; display: inline-block; margin-bottom: 2px; border: 2px solid white; border-radius: 5px; padding: 5px; margin: 5px;">{word} - {tag}</span>'
            
            last_index = end
        highlighted_text += text[last_index:]
        return highlighted_text

    return get_highlighted_text(annotations, text)



# for index, line in enumerate(lines):
#     ner_results = cvnlp(line)
#     comnined_entities = combine_entities(ner_results)
#     highlighted_result = text_highlighter(line, labels=labels, annotations=comnined_entities, key=index)
#     st.markdown(highlighted_result, unsafe_allow_html=True)
    
    
def getNerHighlightedTexts(text):
    comnined_entities = []
    lines_with_ner_resuts = []
    text = text.splitlines()
    for line in text:
        result = dict()
        if len(line) == 0 or line.isspace():
            continue
        ner_results = cvnlp(line)
        comnined_entities = combine_entities(ner_results)
        result['line'] = line
        result['entities'] = comnined_entities
        lines_with_ner_resuts.append(result)
    return lines_with_ner_resuts