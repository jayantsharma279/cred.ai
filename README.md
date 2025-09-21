# CRED.ai: Automated Loan Underwriting from Bank Statements using NLP

This project automates the **loan underwriting process** by parsing applicant **bank statements** from PDF, transforming them into structured data, and running creditworthiness analysis using **NLP models**. 
A finBERT model was finetuned on passbook data from HuggingFace, which runs text classification on each transaction to classify across spend categories (Income, Debt, Expenditure etc.) which is then used for underwriting.

-  **PDF Parsing**: Extracts transaction tables using [LlamaParse API](https://www.llamaparse.com/).  
-  **Data Processing**: Converts parsed JSON into a clean **pandas DataFrame**.  
-  **Underwriting Models**:  
   A **fine-tuned FinBERT model**  
   **OpenAI GPT-3.0** model for comparison
   
-  Outputs underwriting decisions based on model predictions.

---

## ⚙ Tech Stack
- **Python 3.9+**
- **pandas** – for financial data processing    
- **LlamaParse API** – for PDF-to-JSON parsing  
- **Transformers** – for FinBERT model  
- **OpenAI API** – for alternative underwriting model  

---
