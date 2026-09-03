# RazorResolve AI

## AI Investigation Intelligence for Merchant Operations

RazorResolve AI is an AI-powered merchant operations intelligence prototype designed to help support and operations teams investigate merchant issues faster.

Instead of looking at settlement status, KYC status, payment failures, refunds, support cases, and risk signals separately, RazorResolve AI combines these fragmented signals into one investigation workflow.

### Core Idea

> AI investigates, human decides.

The system identifies the likely issue, explains the contributing signals, estimates operational risk, recommends a resolution path, and applies human-review guardrails for high-risk situations.

---

## 🚀 Key Features

### 1. AI Merchant Investigation

The system accepts a merchant problem and automatically:

- Classifies the issue
- Identifies the likely root cause
- Collects supporting evidence
- Calculates an operational risk score
- Provides an explainable AI reasoning summary
- Recommends a resolution plan
- Determines whether human review is required

Supported issue categories:

- Settlement
- Payment
- KYC
- Refund
- Account

---

### 2. Hybrid AI Classification

RazorResolve AI uses a hybrid classification engine:

**Domain keyword signals + TF-IDF + Logistic Regression**

Keyword signals help detect strong domain-specific patterns, while the supervised machine-learning model provides a fallback classification mechanism.

This approach is designed for a lightweight prototype without requiring a large external AI model.

---

### 3. Explainable Investigation

The system does not only provide a decision.

It also provides:

- Findings
- Evidence
- Contributing signals
- AI reasoning
- Confidence
- Risk level
- Human-review reason
- Guardrail reason
- Decision reason

This makes the investigation easier for an operations or support team to understand.

---

### 4. Operational Risk Scoring

The prototype calculates an operational risk score from 0 to 100.

Risk levels:

| Score | Level |
|---|---|
| 0–39 | LOW |
| 40–69 | MEDIUM |
| 70–100 | HIGH |

This is a prototype operational risk indicator and is not intended to represent financial, regulatory, or credit risk.

---

### 5. What-If Risk Simulator

The simulator allows an operator to change merchant signals such as:

- KYC status
- Payment failure rate
- Risk score
- Settlement status
- Pending refunds
- Unusual activity

The system then estimates the resulting operational risk level.

This helps teams explore hypothetical situations before taking action.

---

### 6. Incident Intelligence

Historical incidents can be analyzed using text similarity and issue-category matching.

The system groups similar incidents into clusters and provides information such as:

- Cluster size
- Common issue category
- Average confidence
- Risk level
- Similar historical cases

This helps operations teams use previous cases as investigation context.

---

### 7. Model Evaluation

The prototype contains a small labeled test set covering five issue categories.

Current prototype evaluation:

- Total test cases: 20
- Correct predictions: 20
- Prototype accuracy: 100%

Important:

> This is a small built-in prototype evaluation set and should not be treated as production model performance.

---

### 8. Customer-Service Copilot

The dashboard includes a customer-service copilot that uses investigation context to generate a response suitable for merchant communication.

The goal is to reduce repetitive investigation and response-writing work for support teams.

---

## 🏗️ System Architecture

```text
Merchant Problem
       ↓
Frontend Dashboard
       ↓
FastAPI Backend
       ↓
Issue Classification
       ↓
Merchant Signal Analysis
       ↓
Risk Scoring
       ↓
Explainability Engine
       ↓
Guardrails
       ↓
AI Recommendation
       ↓
Human Decision
       ↓
Resolution / Support Response

Historical Cases
       ↓
Text Vectorization
       ↓
Similarity Analysis
       ↓
Issue Category Matching
       ↓
Incident Clusters
       ↓
Operational Context

RazorResolve-AI/
│
├── backend/
│   └── server.py
│
├── frontend/
│   └── index.html
│
├── data/
│   └── merchants.json
│
├── main.py
│
├── README.md
├── ARCHITECTURE.md
├── API_DOCUMENTATION.md
├── AI_DOCUMENTATION.md
├── DEMO_GUIDE.md
│
└── .gitignore