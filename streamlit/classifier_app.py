import fitz  # PyMuPDF
import re
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import pickle

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
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

# Extract and preprocess text from PDF
# pdf_path = './contract.pdf'
# contract_text = extract_text_from_pdf(pdf_path)
contract_text = """Parties:
This Contract Agreement (Agreement) is made and entered into as of July 1, 2024, by and between AlphaTech Solutions, with a principal place of business at 123 Innovation Drive, Techville, CA 94000, ("First Party"), and Beta Innovations Inc., with a principal place of business at 456 Progress Avenue, Innovatown, NY 10001, ("Second Party").

WHEREAS:
The First Party and the Second Party wish to establish a business relationship whereby AlphaTech Solutions will provide certain services to Beta Innovations Inc. under the terms and conditions set forth in this Agreement.

1. Definitions:
For the purposes of this Agreement, the following terms shall have the meanings ascribed to them herein:

"Services" means the tasks and deliverables specified in the Scope of Work.
"Shares" refers to the stock options granted under this Agreement.
2. Scope of Work:
AlphaTech Solutions agrees to provide Beta Innovations Inc. with the following services: Development and implementation of a custom software solution for data analytics.

3. Compensation:
Beta Innovations Inc. agrees to pay AlphaTech Solutions the amount of $50,000 for the services rendered, according to the payment terms outlined in this Agreement.

4. Payment Terms:
Payments will be made according to the following schedule: $25,000 upon signing of this Agreement and $25,000 upon completion of the project. Any additional expenses must be pre-approved in writing by Beta Innovations Inc.

5. Vesting:
Any stock options granted to AlphaTech Solutions will vest over a period of 4 years with a 1-year cliff.

6. Termination:
Either party may terminate this Agreement at any time by providing 30 days written notice to the other party. Upon termination, AlphaTech Solutions will be compensated for all services performed up to the date of termination.

7. Taxes:
Each party shall be responsible for its own taxes arising from the transactions contemplated by this Agreement.

8. Stock Option:
Beta Innovations Inc. agrees to grant AlphaTech Solutions stock options as part of the compensation package.

9. Shares:
Details regarding the number of shares and the vesting schedule will be documented in a separate Stock Option Agreement.

10. Severability:
If any provision of this Agreement is found to be invalid or unenforceable, the remaining provisions will continue to be valid and enforceable.

11. Seed:
Any seed funding or investment in the project will be subject to a separate investment agreement.

12. Representations:
Each party represents and warrants that it has the authority to enter into this Agreement and perform its obligations hereunder.

13. Private Equity:
Any private equity investment will be governed by a separate agreement.

14. Ownership of Shares:
AlphaTech Solutions shall have no ownership interest in the shares until they are vested.

15. Notices:
All notices required or permitted under this Agreement shall be in writing and shall be deemed delivered when delivered in person, via email, or by certified mail, return receipt requested, to the addresses specified above.

16. Miscellaneous:
This Agreement contains the entire understanding of the parties with respect to the subject matter hereof and supersedes all prior agreements and understandings.

17. Loans:
Any loans between the parties will be documented in a separate loan agreement.

18. Investments:
Investments made under this Agreement will be subject to applicable laws and regulations.

19. Investment Company:
If either party becomes an investment company, this Agreement will be amended to comply with the Investment Company Act.

20. Interest:
Any overdue payments shall accrue interest at a rate of 5% per annum.

21. Insurance:
Each party shall maintain adequate insurance coverage to protect its interests under this Agreement.

22. Indemnification:
Each party agrees to indemnify and hold harmless the other party from any claims, damages, or liabilities arising out of its performance under this Agreement.

23. Headings:
The headings in this Agreement are for convenience only and shall not affect its interpretation.

24. Grant of Option:
Beta Innovations Inc. hereby grants AlphaTech Solutions the option to purchase shares of its common stock, subject to the terms of the Stock Option Agreement.

25. Governing Law:
This Agreement will be governed by and construed in accordance with the laws of the State of California, without regard to its conflict of law principles.

26. Foreign Investors:
Any foreign investments will comply with all applicable laws and regulations.

27. Financing:
Any financing arrangements will be documented in a separate financing agreement.

28. ESOP:
Employee stock ownership plans (ESOP) will be governed by the terms of the company's ESOP plan.

29. Entire Agreement:
This Agreement constitutes the entire agreement between the parties and supersedes all prior or contemporaneous understandings, agreements, representations, and warranties, whether written or oral, with respect to the subject matter of this Agreement.

30. Employee Benefits:
AlphaTech Solutions employees assigned to this project will receive benefits as per the company’s policy.

31. Dividends:
Any dividends declared on shares will be paid in accordance with the company’s dividend policy.

32. Counterparts:
This Agreement may be executed in counterparts, each of which shall be deemed an original, but all of which together shall constitute one and the same instrument.

33. Conversion of Shares:
Shares granted under this Agreement may be converted into common stock as per the terms of the Stock Option Agreement.

34. Confidentiality:
Both parties agree to keep confidential any and all information that is disclosed during the course of this Agreement. This confidentiality obligation will survive the termination of this Agreement.

35. Compensation:
Compensation for services rendered will be as outlined in the Compensation section of this Agreement.

36. Clause Type:
This Agreement includes various clause types, such as confidentiality, indemnification, and severability, to ensure comprehensive coverage of the parties' rights and obligations.

37. Capitalization:
The capitalization table of Beta Innovations Inc. will be updated to reflect any changes in ownership resulting from the grant of shares.

38. Board:
Any decisions regarding the grant of options or shares will be subject to approval by the Beta Innovations Inc. board of directors.

39. Base Salary:
The base salary for any AlphaTech Solutions employees assigned to this project will be determined in accordance with the company’s salary structure.

40. Assignment:
Neither party may assign its rights or obligations under this Agreement without the prior written consent of the other party."""


# Split text into clauses
clauses = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', contract_text)
print(clauses)
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

# Output the predictions
# for clause, clause_type in zip(clauses, predicted_clause_types):
#     print(f"Clause: {clause}\nPredicted Clause Type: {clause_type}\n")

# Print all predictions in a structured way
print("Predicted Clause Types for the given contract:")
for idx, clause_type in enumerate(predicted_clause_types):
    print(f"Clause {idx+1}: {clause_type}")
