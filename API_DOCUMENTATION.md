# RazorResolve AI — API Documentation

## Overview

RazorResolve AI provides APIs for merchant operations investigation, risk simulation, incident intelligence, and model evaluation.

Base URL (Local):

http://127.0.0.1:8000

Base URL (Production):

https://razorresolve-ai.onrender.com

---

## 1. Health Check

### Endpoint

GET `/health`

### Purpose

Checks whether the API service is running.

### Example

```http
GET /health


{
  "status": "healthy"
}

{
  "problem": "Settlement delayed for merchant"
}

{
  "success": true,
  "issue": "Settlement",
  "root_cause": "Settlement hold or delayed payout",
  "decision": "Escalate",
  "decision_type": "Human Review",
  "confidence": 0.94,
  "risk_score": 78,
  "risk_level": "HIGH",
  "human_review": true
}

{
  "kyc_status": "Pending",
  "payment_failure_rate": 6.7,
  "risk_score": 78,
  "settlement_status": "On Hold",
  "pending_refunds": 2,
  "unusual_activity": false
}


{
  "success": true,
  "predicted_risk_score": 93,
  "risk_level": "HIGH",
  "message": "Changing the merchant signals results in a predicted risk of 93/100."
}

{
  "cases": []
}

{
  "success": true,
  "total_cases": 6,
  "cluster_count": 4,
  "demo_mode": true,
  "engine": "TF-IDF similarity + issue category matching"
}

High-risk cases should not be automatically resolved because
sensitive merchant operations may be affected.