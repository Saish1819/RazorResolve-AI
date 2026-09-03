# RazorResolve AI — System Architecture

## 1. Overview

RazorResolve AI is a merchant operations intelligence prototype that combines merchant signals, AI-based issue classification, risk analysis, explainability, incident intelligence, and human-in-the-loop controls into a single investigation workflow.

The core principle is:

> AI investigates, evidence explains, humans decide.

---

## 2. High-Level Architecture

```text
                    ┌──────────────────────┐
                    │  Merchant / Operator │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Frontend Dashboard │
                    │     HTML/CSS/JS      │
                    └──────────┬───────────┘
                               │ HTTP
                               ▼
                    ┌──────────────────────┐
                    │    FastAPI Backend   │
                    │    backend/server.py │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
      │    Issue    │   │  Merchant   │   │    Risk     │
      │ Classifier  │   │   Signals   │   │   Analysis  │
      └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │    Explainability    │
                    │       Engine         │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │      Guardrails      │
                    │    Human Review      │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │  AI Recommendation   │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │    Human Decision    │
                    └──────────────────────┘
                    
Frontend
   ↓
API Layer
   ↓
Investigation Engine
   ↓
AI Classification
   ↓
Signal Analysis
   ↓
Risk Engine
   ↓
Explainability
   ↓
Guardrails
   ↓
Human Decision

frontend/index.html
backend/server.py
data/merchants.json

                Merchant Problem
                       │
                       ▼
              Text Normalization
                       │
                       ▼
              Keyword Detection
                       │
              ┌────────┴────────┐
              │                 │
        Strong Match?          No
              │                 │
             Yes                ▼
              │             TF-IDF
              │                │
              │                ▼
              │       Logistic Regression
              │                │
              └────────┬───────┘
                       ▼
                 Issue Category

                 Settlement Status
KYC Status
Payment Failure Rate
Pending Refunds
Unusual Activity
Risk Score
Support Cases

Issue
Root Cause
Findings
Evidence
Confidence
Risk Score
Risk Level
AI Reasoning
Contributing Signals
Signal Summary
Decision Reason
Human Review Reason
Guardrail Reason

             AI Investigation
                    │
                    ▼
              Risk Analysis
                    │
                    ▼
            Guardrail Check
                    │
           ┌────────┴────────┐
           │                 │
        High Risk          Lower Risk
           │                 │
           ▼                 ▼
    Human Review        AI Recommendation
           │
           ▼
    Human Decision

    AI Recommendation
       │
       ▼
Human Review
       │
   ┌───┴────┐
   │        │
Approve   Reject
   │        │
   ▼        ▼
Action   Reconsider

KYC Status
Payment Failure Rate
Risk Score
Settlement Status
Pending Refunds
Unusual Activity

Hypothetical Inputs
        ↓
Signal Processing
        ↓
Risk Calculation
        ↓
Predicted Risk Score
        ↓
Risk Level

Frontend
   │
   ├── GET  /health
   │
   ├── POST /analyze
   │
   ├── POST /simulate
   │
   ├── POST /incidents
   │
   └── GET  /evaluate
   │
   ▼
FastAPI Backend

1. Merchant Problem
        ↓
2. Issue Classification
        ↓
3. Merchant Signal Collection
        ↓
4. Evidence Analysis
        ↓
5. Risk Scoring
        ↓
6. AI Reasoning
        ↓
7. Guardrail Check
        ↓
8. Recommendation
        ↓
9. Human Review
        ↓
10. Resolution

Merchant Issue
      ↓
Investigation
      ↓
Evidence + Findings
      ↓
Resolution Context
      ↓
Customer-Service Copilot
      ↓
Support Response

                    ┌─────────────────┐
                    │ Merchant Issue  │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │   Classifier    │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Merchant Signals│
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │  Risk Analysis  │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Explainability  │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │   Guardrails    │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ AI Recommendation│
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Human Decision  │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │    Resolution   │
                    └─────────────────┘

                    Browser
   ↓
Frontend Server :5500
   ↓
FastAPI Server :8000
   ↓
Local JSON Data

AI investigates
       ↓
Evidence explains
       ↓
Risk informs
       ↓
Human decides
       ↓
Operations resolve