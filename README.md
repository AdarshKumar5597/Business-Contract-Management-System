
# ClauseCheck

Business contracts are complex legal documents with structured
content. The Business Contract Validator Website enhances the contract
review and validation process by utilizing Natural Language Processing
(NLP) to extract key entities from uploaded PDFs, such as parties'
names, agreement date, amount, and document type. It compares this
extracted data against a predefined template to identify discrepancies
and missing elements, generating a summary that highlights key points
and potential issues. This approach streamlines the contract analysis
process, improving efficiency, accuracy, and consistency with a user-friendly interface and robust backend technologies.

So, we created an application which is designed for contract analysis and Named Entity Recognition (NER). The application classifies content within contract clauses, detects deviations from a template, and highlights them. Additionally, we developed a text classifier to enhance the accuracy of content classification.

## Technologies used
- Frontend: React, Next.js, HTML5, CSS3, Javascript
- Backend: FastAPI, Flask
- Model: PyTorch, HuggingFace


## Features

- Text Extraction from PDFs
- PDF-Parser
- Named Entity Recognition (NER)
- Text Classification
- Entity Highlighting
- Text Comparison
- Text Summarization
- User-Friendly Interface


## Authors

- [@AdarshKumar5597](https://github.com/AdarshKumar5597)
- [@RedWolfCodes](https://github.com/RedWolfCodes)
- [@anishakshyp](https://github.com/anishakshyp)
- [@HUMAN1-2](https://github.com/HUMAN1-2)


## Process Flow

![ProcessFlow](https://i.ibb.co/xFs14Bk/diagram-export-7-14-2024-9-47-13-PM.png)

## Screenshots

![Front](https://i.ibb.co/WVp5Cww/Screenshot-2024-07-15-195855.png)

![Features1](https://i.postimg.cc/sD1NJ7vV/Screenshot-2024-07-15-195913.png)

![Features3](https://i.postimg.cc/FsqnCzL0/Screenshot-2024-07-15-195938.png)

![Features2](https://i.postimg.cc/ZqP7qLDL/Screenshot-2024-07-15-195959.png)

![Process2](https://i.postimg.cc/vTT33w8P/Screenshot-2024-07-15-200016.png)

![Process3](https://i.postimg.cc/prSkScpP/Screenshot-2024-07-15-200029.png)

![Process1](https://i.postimg.cc/ZYsf0njX/Screenshot-2024-07-15-200041.png)


## Run the program

To deploy this project run, go through this following steps:

- Step 1: Clone the repository
```bash
  git clone https://github.com/AdarshKumar5597/Business-Contract-Management-System.git
```

- Step 2: To run the frontend
```bash
    cd bcv-frontend
    npm i
    npm run dev
```

- Step 3: To run the backend, download the model from this google drive link: https://drive.google.com/drive/folders/1S-jcKlC3o5AaHwIamT_JkfltrxqogntM?usp=drive_link and download the folders.


- Step 4: After downloading the folders, paste them in [flask-backend] folder.

- Step 5: Run this command to install all python packages.
```bash
    pip install -r requirements.txt
```

- Step 6: Then initiate the backend code.
```bash
    python app.py
```




## Instruction

- Our program needs two contract pdfs (must be in text or pdf format) - Standard Template and Target contract to compare, classify and summarize.

