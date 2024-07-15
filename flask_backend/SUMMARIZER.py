from transformers import pipeline

summarizer = pipeline("summarization", model="Azma-AI/bart-large-text-summarizer")

text = '''BUSINESS CONTRACT AGREEMENT

This Business Contract Agreement (the "Agreement") is made and entered into as of the [Date] (the "Effective Date") by and between:

Party A:
XYZ Enterprises, Inc.
123 Business Lane
Cityville, State 12345

Party B:
ABC Solutions, LLC
456 Corporate Blvd
Metropolis, State 67890

1. Purpose
This Agreement sets forth the terms and conditions under which XYZ Enterprises, Inc. ("Party A") agrees to provide certain services to ABC Solutions, LLC ("Party B").

2. Services
Party A agrees to provide the following services to Party B:

Development and implementation of a custom software application tailored to Party B's business needs.
Ongoing maintenance and support for the software application for a period of one year from the date of final delivery.
Training sessions for Party B's staff on the use and management of the software application.
3. Payment Terms

Party B agrees to pay Party A a total fee of $150,000 for the services provided.
An initial deposit of $30,000 is due upon signing this Agreement.
The remaining balance of $120,000 shall be paid in equal monthly installments over the next 12 months.
All payments shall be made via bank transfer to the account specified by Party A.
4. Term and Termination

This Agreement shall commence on the Effective Date and shall continue for a period of one year, unless earlier terminated in accordance with this Agreement.
Either party may terminate this Agreement upon 30 days' written notice to the other party.
In the event of termination, Party B shall pay Party A for all services rendered up to the effective date of termination.
5. Confidentiality

Both parties agree to maintain the confidentiality of any proprietary information received from the other party during the term of this Agreement.
This obligation of confidentiality shall survive the termination of this Agreement.
6. Warranties and Representations

Party A warrants that the services provided under this Agreement shall be performed in a professional and workmanlike manner.
Party B represents and warrants that it has the authority to enter into this Agreement and to perform its obligations hereunder.
7. Limitation of Liability

In no event shall either party be liable for any indirect, incidental, special, or consequential damages arising out of or in connection with this Agreement.
The total liability of either party for any claims arising out of this Agreement shall not exceed the total amount paid by Party B to Party A under this Agreement.
8. Governing Law
This Agreement shall be governed by and construed in accordance with the laws of the State of [State], without regard to its conflict of laws principles.

9. Dispute Resolution

Any disputes arising out of or in connection with this Agreement shall be resolved through good faith negotiations between the parties.
If the dispute cannot be resolved through negotiation, the parties agree to submit the dispute to mediation.
If mediation fails, the dispute shall be resolved by binding arbitration in accordance with the rules of the American Arbitration Association.
10. Miscellaneous

This Agreement constitutes the entire agreement between the parties and supersedes all prior agreements and understandings, whether written or oral.
Any amendments or modifications to this Agreement must be in writing and signed by both parties.
Neither party may assign its rights or obligations under this Agreement without the prior written consent of the other party.
IN WITNESS WHEREOF, the parties hereto have executed this Business Contract Agreement as of the Effective Date.

XYZ Enterprises, Inc. ABC Solutions, LLC
By: ________________________ By: ________________________
Name: [Name of Signatory] Name: [Name of Signatory]
Title: [Title of Signatory] Title: [Title of Signatory]
Date: _______________________ Date: _______________________
'''
# print(summarizer(text))

def getSummary(text):
    summary = summarizer(text)
    return summary