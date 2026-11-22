# BusinessDoc AI
### AI-Powered Invoice and Purchase Order Reconciliation

BusinessDoc AI is a Python-based application that automates the comparison of invoices and purchase orders using document processing, rule-based validation, and Amazon Bedrock generative AI.

It identifies discrepancies between business documents and generates clear, AI-powered explanations to help users understand issues that may require attention.

## Problem Statement

Businesses regularly process invoices against purchase orders. Manually checking every field and product entry can be time-consuming and may lead to overlooked discrepancies.

BusinessDoc AI helps simplify this process by automatically extracting information, comparing important fields, identifying mismatches, and generating explanations.

## Key Features

- Upload invoice and purchase order PDFs.
- Extract document information using PyMuPDF.
- Compare supplier, buyer, dates, totals, and product details.
- Identify missing products and mismatched values.
- Generate plain-language discrepancy explanations using Amazon Bedrock.
- Generate a downloadable PDF reconciliation report.
- Run the application locally or using Docker.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Web application interface |
| PyMuPDF | PDF text extraction |
| Pandas | Data handling |
| Amazon Bedrock | AI-powered explanations |
| Amazon Nova 2 Lite | Generative AI model |
| Boto3 | AWS service integration |
| ReportLab | PDF report generation |
| Pytest | Unit testing |
| Docker | Application containerization |
| Git & GitHub | Version control and source code hosting |

## How It Works

1. **Document Upload:** User uploads an invoice PDF and a purchase order PDF.
2. **Text Extraction:** PyMuPDF extracts text from both documents.
3. **Data Processing:** Extracted information is organized into structured fields.
4. **Reconciliation:** Python validation logic compares the extracted information.
5. **Discrepancy Detection:** Mismatches are identified and displayed.
6. **AI Explanation:** Amazon Bedrock generates a business-friendly explanation of the detected discrepancies.
7. **Report Generation:** A downloadable PDF report summarizes the reconciliation results.

### Important Design Principle

Python-based validation rules determine whether information matches or differs. Amazon Bedrock is used to explain the detected discrepancies, not to make payment approval decisions.

## Project Structure

```text
BusinessDoc-AI/
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
├── app.py
├── requirements.txt
│
├── sample_documents/
│   ├── sample_invoice.pdf
│   └── sample_purchase_order.pdf
│
├── src/
│   ├── __init__.py
│   ├── bedrock_explainer.py
│   ├── pdf_extractor.py
│   ├── reconciler.py
│   └── report_generator.py
│
└── tests/
    └── test_reconciler.py
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/AshishVittal/BusinessDoc-AI.git
cd BusinessDoc-AI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure AWS

Configure AWS CLI credentials and ensure the AWS identity has permission to invoke the selected Amazon Bedrock model.

Create a `.env` file in the project root:

```env
AWS_REGION=ap-south-1
BEDROCK_MODEL_ID=global.amazon.nova-2-lite-v1:0
```

AWS credentials should be configured separately through the AWS CLI. Do not put access keys or secret keys in the `.env` file or commit credentials to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local Streamlit URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## Running Tests

Run the test suite using:

```bash
python -m pytest -v
```

The reconciliation test suite has successfully passed all three tests:

- `test_all_fields_match`
- `test_delivery_date_mismatch`
- `test_missing_product_is_detected`

## Docker Setup

Build the Docker image:

```bash
docker build -t businessdoc-ai .
```

Run the container on Windows PowerShell:

```powershell
docker run -d --name businessdoc-ai-container -p 8501:8501 --env-file .env -v "$env:USERPROFILE\.aws:/root/.aws:ro" -e AWS_PROFILE=default businessdoc-ai
```

The AWS credentials folder is mounted read-only so the container can use the configured AWS profile without copying credentials into the Docker image.

Open:

```text
http://localhost:8501
```

## Sample Reconciliation Scenario

The included fictional sample documents represent a purchase order and its corresponding invoice.

| Field | Purchase Order | Invoice |
|---|---|---|
| PO Number | PO-2026-1042 | PO-2026-1042 |
| Invoice Number | — | INV-2026-0881 |
| Supplier | Northstar Office Supplies | Northstar Office Supplies |
| Subtotal | INR 8,600 | INR 8,600 |
| GST | INR 1,548 | INR 1,548 |
| Total | INR 10,148 | INR 10,148 |
| Expected Delivery Date | 20 November 2026 | 27 November 2026 |

**Detected discrepancy:** The invoice lists a delivery date seven days later than the purchase order.

The application identifies this mismatch and uses Amazon Bedrock to explain why it may require business review.

## Limitations

- Text extraction depends on the PDF containing readable text. Scanned documents requiring OCR are not currently supported.
- The application uses predefined validation rules and extracted document fields.
- AI-generated explanations should be reviewed by a human.
- The application does not approve or reject payments.
- AWS Bedrock usage may incur charges depending on usage and applicable pricing.

## Future Improvements

- Add OCR support for scanned documents.
- Introduce persistent database storage for reconciliation history.
- Add support for additional document formats.
- Improve validation and error handling.
- Deploy the application on AWS.
- Add user authentication and access control.

## Disclaimer

This project is an educational portfolio project. The included sample documents contain fictional business information. Reconciliation results and AI-generated explanations are intended to assist human review and should not be treated as automatic financial approval decisions.
