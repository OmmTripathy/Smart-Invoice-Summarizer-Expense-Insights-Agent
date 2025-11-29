# Smart Invoice Summarizer & Expense Insights Agent

## An AI-powered multi-agent system that extracts invoice data, summarizes key details, and generates real-time spending insights for small businesses adn startups

**Category:** **Enterprise Agents**  

## Team Members :
1. Omm Kishor Tripathy
2. Adarsha Sahoo
3. OMM PRASAD SAHOO


## 1. Project Overview
Small business owners and startup teams generate dozens of receipts and invoices every month.  
They often spend hours manually reading invoices, extracting amounts, typing data into Excel, and tracking expenses. This workflow is repetitive, error-prone, and wastes valuable time.

This project solves that problem by building an **AI‑powered multi‑agent system** that automatically:

- Reads receipts, bills, invoices, and payment statements **in pdf format**
- Extracts structured data using vision-enabled AI
- Validates fields (totals, taxes, dates, vendor names)
- Stores the extracted results
- Displays them inside a clean UI (frontend)
- Allows users to manage and track expenses instantly

The system uses **OpenAI models**, a **FastAPI backend**, a **Gradio/HTML/JS UI frontend**, and a **multi-agent architecture**.

---

## 2. Problem Statement
Small businesses and startup teams face issues regarding Time-consuming manual reading, Error-prone & slow entry typing into Excel, No insights into spending patterns, and mentally exhausting.

---

## 3. Solution Pitch
We built the **Smart Invoice Summarizer & Expense Insights Agent**,an AI-powered multi-agent system that accepts PDFs of receipts/invoices, extracts invoice data and text, summarizes key details, and generates real-time spending insights for small businesses.
This reduces the manual work of logging expenses from hours per week to minutes—or zero if automated.

---

## 4. Values Created
Users avoid manual entry
AI ensures consistent parsing
Expenses are logged instantly
Can support 100s of documents
This project demonstrates practical use of agents for enterprise productivity and finance automation.

---


## 5. Architecture

### Multi-Agent Workflow

1. **Extraction Agent**
Uses OpenAI Vision models
Extracts raw text + structured fields
Handles multiple formats: JPG, PNG, PDF
Outputs a JSON payload

2. **Validation Agent**
Normalizes numeric fields
Converts dates to ISO
Performs consistency checks

3. **Analytics Agent**  
Aggregates validated results  
Generates spending summaries and insights  
Categorizes expenses (e.g., food, travel, utilities)  
Provides charts and statistics for users  

4. **Frontend UI**
Built with Gradio
Users upload receipts
Receives structured results from backend

5. **Backend**
FastAPI server
Two endpoints: `/extract`, `/validate`
Communicates with agents
Supports deployment on Cloud Run or local

---

### Architecture Diagram
                   ┌──────────────────┐
                   │     Frontend      │
                   │ (UI / File Upload)│
                   └─────────┬────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │       Backend        │
                  │     (FastAPI)        │
                  └─────────┬───────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌─────────────┐     ┌────────────────┐     ┌────────────────┐
│ Extraction  │     │ Validation     │     │   Analytics    │
│    Agent    │     │    Agent       │     │     Agent      │
└─────────────┘     └────────────────┘     └────────────────┘
        │                    │                    │
        └──────────┬────────┴──────────┬─────────┘
                   ▼                   ▼
             Extracted JSON     Validated JSON


---

## 6. Features
Multi-agent architecture
Tools integration
Structured data extraction  
API endpoint integration  
Vision-based model usage  
Invoice summarization  
Analytics & insights generation  
Cloud Run deployment  
Memory for storing past expenses

---

## 7. Setup Instructions

### Prerequisites
Python 3.9+  
FastAPI  
Gradio / HTML / JS frontend  
OpenAI API access

### Installation
```bash
# Clone repository from github
git clone https://github.com/yourusername/expense-tracker-agent.git

# Install dependencies
pip install -r requirements.txt

# Execute frontend & backend together
runall.bat


#Lunch backend and frontend in separate terminals
# Run only backend
uvicorn app.main:app --reload --port 8080
# Launch only frontend
uvicorn ui.app:app --reload --port 8000
```

## 8. Future Enhancements
Auto email invoice collector,Integration with accounting software,Multi-currency support,Alert agent for unusual spending & more.

## 9. Conclusion
The project shows how AI agents can automate business workflows using multi-agent design,memory, tools, and Gemi
