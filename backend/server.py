from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity

import json
import os
import re
from statistics import mean


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="RazorResolve AI",
    description="AI Investigation Intelligence for Merchant Operations",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# LOAD MERCHANT DATA
# ============================================================

def load_merchants():
    path = os.path.join("data", "merchants.json")

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


# ============================================================
# AI CLASSIFICATION MODEL
# ============================================================

training_texts = [
    # Settlement
    "settlement delayed money not received",
    "settlement on hold payout delayed",
    "merchant settlement issue",
    "payout has not arrived",

    # Refund
    "refund pending customer money",
    "refund not received",
    "customer refund delayed",
    "money back pending",

    # KYC
    "kyc pending verification document",
    "business proof missing kyc",
    "kyc verification problem",
    "merchant verification pending",

    # Payment
    "payment failed transaction declined",
    "payment failure checkout declined",
    "transaction failed repeatedly",
    "customers cannot complete payment",

    # Account
    "account blocked merchant account",
    "account issue access problem",
    "login not working",
    "merchant account access issue",
]


training_labels = [
    "Settlement",
    "Settlement",
    "Settlement",
    "Settlement",

    "Refund",
    "Refund",
    "Refund",
    "Refund",

    "KYC",
    "KYC",
    "KYC",
    "KYC",

    "Payment",
    "Payment",
    "Payment",
    "Payment",

    "Account",
    "Account",
    "Account",
    "Account",
]


vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2)
)

X = vectorizer.fit_transform(training_texts)

classifier = LogisticRegression(
    max_iter=1000,
    random_state=42
)

classifier.fit(X, training_labels)


# ============================================================
# PROBLEM CLASSIFICATION
# ============================================================

def classify_problem(problem: str):

    text = problem.lower().strip()

    keywords = {
        "Settlement": [
            "settlement",
            "payout",
            "money not received",
            "settlement delayed",
            "settlement hold",
            "on hold",
            "payout delayed",
            "payout not arrived",
        ],

        "Refund": [
            "refund",
            "refund pending",
            "refund delayed",
            "money back",
            "customer refund",
        ],

        "KYC": [
            "kyc",
            "verification",
            "verify",
            "document",
            "business proof",
            "merchant verification",
        ],

        "Payment": [
            "payment",
            "failed",
            "failure",
            "declined",
            "transaction",
            "checkout",
            "payment failure",
        ],

        "Account": [
            "account",
            "blocked",
            "access",
            "login",
            "merchant account",
        ],
    }

    scores = {}

    for category, words in keywords.items():
        scores[category] = sum(
            1
            for word in words
            if word in text
        )

    best_category = max(
        scores,
        key=scores.get
    )

    if scores[best_category] > 0:
        return best_category

    prediction = classifier.predict(
        vectorizer.transform([problem])
    )[0]

    return prediction


# ============================================================
# RISK LEVEL
# ============================================================

def risk_level(score: int):

    if score >= 75:
        return "HIGH"

    if score >= 45:
        return "MEDIUM"

    return "LOW"


# ============================================================
# MERCHANT INVESTIGATION
# ============================================================

def investigate_merchant(merchant):

    signals = []
    findings = []
    explainability = []

    risk_score = int(
        merchant["risk"]["risk_score"]
    )

    settlement = merchant["settlement"]
    payments = merchant["payments"]
    kyc = merchant["kyc"]
    refunds = merchant["refunds"]
    support = merchant["support"]

    # Settlement
    if settlement["status"] == "On Hold":

        signals.append(
            "Settlement is currently on hold"
        )

        findings.append(
            f"₹{settlement['amount']:,} settlement amount is affected"
        )

        explainability.append({
            "signal": "Settlement On Hold",
            "impact": "HIGH",
            "reason": (
                "A settlement hold can directly prevent "
                "merchant funds from being released."
            )
        })

    if settlement["days_delayed"] > 0:

        signals.append(
            f"Settlement delayed by "
            f"{settlement['days_delayed']} days"
        )

        findings.append(
            f"Settlement is delayed by "
            f"{settlement['days_delayed']} days"
        )

        explainability.append({
            "signal": "Settlement Delay",
            "impact": "HIGH",
            "reason": (
                "The expected settlement timeline "
                "has not been met."
            )
        })

    # KYC
    if kyc["status"] == "Pending":

        signals.append(
            "KYC verification is pending"
        )

        findings.append(
            f"Missing document: "
            f"{kyc['missing_document']}"
        )

        explainability.append({
            "signal": "KYC Pending",
            "impact": "HIGH",
            "reason": (
                "Pending verification can affect eligibility "
                "for certain merchant operations."
            )
        })

    # Payments
    failure_rate = float(
        payments["failure_rate"]
    )

    if failure_rate >= 20:

        signals.append(
            f"High payment failure rate: {failure_rate}%"
        )

        findings.append(
            f"Payment failure rate is {failure_rate}%"
        )

        explainability.append({
            "signal": "High Payment Failure Rate",
            "impact": "HIGH",
            "reason": (
                "A high failure rate indicates an abnormal "
                "payment performance pattern."
            )
        })

    elif failure_rate >= 10:

        signals.append(
            f"Elevated payment failure rate: {failure_rate}%"
        )

        findings.append(
            f"Payment failure rate is {failure_rate}%"
        )

        explainability.append({
            "signal": "Elevated Payment Failure Rate",
            "impact": "MEDIUM",
            "reason": (
                "The failure rate is above the normal "
                "low-risk range."
            )
        })

    # Refunds
    pending_refunds = int(
        refunds["pending_count"]
    )

    if pending_refunds > 0:

        signals.append(
            f"{pending_refunds} refunds are pending"
        )

        findings.append(
            f"{pending_refunds} customer refund(s) remain unresolved"
        )

        explainability.append({
            "signal": "Pending Refunds",
            "impact": "MEDIUM",
            "reason": (
                "Pending refunds create unresolved "
                "customer-facing operational work."
            )
        })

    # Unusual activity
    if merchant["risk"]["unusual_activity"]:

        signals.append(
            "Unusual merchant activity detected"
        )

        findings.append(
            "Unusual activity requires additional review"
        )

        explainability.append({
            "signal": "Unusual Activity",
            "impact": "HIGH",
            "reason": (
                "Unusual activity increases the need "
                "for manual investigation."
            )
        })

    # Support
    open_cases = int(
        support["open_cases"]
    )

    if open_cases > 0:

        signals.append(
            f"{open_cases} support cases are open"
        )

        explainability.append({
            "signal": "Open Support Cases",
            "impact": "MEDIUM",
            "reason": (
                "Multiple unresolved cases indicate "
                "an ongoing merchant support burden."
            )
        })

    return {
        "signals": signals,
        "findings": findings,
        "risk_score": risk_score,
        "risk_level": risk_level(risk_score),
        "explainability": explainability,
    }


# ============================================================
# AI REASONING
# ============================================================

def create_ai_reasoning(category, investigation):

    signals = investigation["explainability"]

    high_signals = [
        item["signal"]
        for item in signals
        if item["impact"] == "HIGH"
    ]

    if category == "Settlement":

        if high_signals:
            return (
                "The AI classified this as a Settlement issue "
                "because settlement-related operational signals "
                "were detected. The strongest indicators are "
                + ", ".join(high_signals)
                + "."
            )

        return (
            "The complaint contains settlement-related language, "
            "so the AI classified it as a Settlement issue."
        )

    if category == "Payment":

        if high_signals:
            return (
                "The AI detected a Payment issue because "
                "payment performance signals indicate possible "
                "transaction instability. The strongest indicators "
                "are "
                + ", ".join(high_signals)
                + "."
            )

        return (
            "The complaint contains payment-related language, "
            "so the AI classified it as a Payment issue."
        )

    if category == "KYC":

        return (
            "The AI identified a KYC issue because the merchant "
            "verification state contains evidence of incomplete "
            "or pending verification."
        )

    if category == "Refund":

        return (
            "The AI identified a Refund issue because pending "
            "refund activity indicates unresolved refund processing."
        )

    if category == "Account":

        return (
            "The AI identified an Account issue based on "
            "merchant account access or status signals."
        )

    return (
        "The AI identified the issue using the merchant complaint "
        "and available operational signals."
    )


# ============================================================
# RESOLUTION PLAN
# ============================================================

def create_resolution_plan(category):

    plans = {

        "Settlement": [
            "Verify settlement hold reason",
            "Check KYC and compliance status",
            "Validate settlement account details",
            "Escalate if delay exceeds expected timeline",
        ],

        "Payment": [
            "Identify dominant payment failure pattern",
            "Check transaction decline signals",
            "Review payment configuration",
            "Monitor failure rate after corrective action",
        ],

        "KYC": [
            "Identify missing verification document",
            "Request valid business documentation",
            "Re-run verification",
            "Escalate if verification remains blocked",
        ],

        "Refund": [
            "Identify pending refund transactions",
            "Verify refund processing status",
            "Check customer payment destination",
            "Escalate unusually delayed refunds",
        ],

        "Account": [
            "Verify account status",
            "Check recent security signals",
            "Validate merchant access",
            "Escalate suspicious account activity",
        ],
    }

    return plans.get(
        category,
        [
            "Investigate merchant signals",
            "Validate supporting evidence",
            "Apply appropriate resolution",
        ]
    )


# ============================================================
# GUARDRAILS
# ============================================================

def create_guardrail(category, investigation):

    score = investigation["risk_score"]

    if score >= 75:

        return {
            "action": "Human Review Required",
            "reason": (
                "High-risk cases should not be automatically "
                "resolved because sensitive merchant operations "
                "may be affected."
            )
        }

    if category == "KYC":

        return {
            "action": "Document Verification Required",
            "reason": (
                "Do not approve verification without "
                "valid supporting evidence."
            )
        }

    if category == "Settlement":

        return {
            "action": "Manual Settlement Review",
            "reason": (
                "Financial holds require verification "
                "before release."
            )
        }

    if category == "Payment":

        return {
            "action": "Monitor Before Intervention",
            "reason": (
                "Payment changes should be validated "
                "against observed failure signals."
            )
        }

    return {
        "action": "Controlled Resolution",
        "reason": (
            "Apply only evidence-supported actions."
        )
    }


# ============================================================
# DECISION
# ============================================================

def create_decision(category, investigation):

    score = investigation["risk_score"]

    if score >= 75:

        return {
            "decision": "Escalate",
            "decision_type": "Human Review",
        }

    if category == "Payment" and score >= 60:

        return {
            "decision": "Investigate",
            "decision_type": "AI Investigation",
        }

    return {
        "decision": "Recommend Resolution",
        "decision_type": "AI Recommendation",
    }


# ============================================================
# CONFIDENCE
# ============================================================

def get_confidence(category):

    confidence = {
        "Payment": 0.91,
        "Settlement": 0.94,
        "KYC": 0.92,
        "Refund": 0.89,
        "Account": 0.86,
    }

    return confidence.get(category, 0.86)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "RazorResolve AI is running",
        "status": "online",
        "version": "1.0.0"
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================================
# ANALYZE
# ============================================================

class AnalyzeRequest(BaseModel):
    problem: str


@app.post("/analyze")
def analyze(request: AnalyzeRequest):

    problem = request.problem.strip()

    if not problem:

        return {
            "success": False,
            "error": "Please enter a problem"
        }

    category = classify_problem(problem)

    merchants = load_merchants()

    if not merchants:

        return {
            "success": False,
            "error": "No merchant data available"
        }

    merchant = merchants[0]

    investigation = investigate_merchant(
        merchant
    )

    resolution_plan = create_resolution_plan(
        category
    )

    guardrail = create_guardrail(
        category,
        investigation
    )

    decision = create_decision(
        category,
        investigation
    )

    confidence = get_confidence(
        category
    )

    root_causes = {

        "Settlement":
            "Settlement hold or delayed payout",

        "Payment":
            "Elevated transaction failure or decline pattern",

        "KYC":
            "Incomplete merchant verification",

        "Refund":
            "Pending refund processing",

        "Account":
            "Merchant account access or status issue",
    }

    ai_reasoning = create_ai_reasoning(
        category,
        investigation
    )

    if investigation["risk_score"] >= 75:

        human_review_reason = (
            f"Risk score is {investigation['risk_score']}/100, "
            "which crosses the high-risk threshold. "
            "The AI therefore recommends human review instead "
            "of autonomous resolution."
        )

    else:

        human_review_reason = (
            f"Risk score is {investigation['risk_score']}/100, "
            "which does not cross the high-risk escalation threshold."
        )

    high_signals = [
        item["signal"]
        for item in investigation["explainability"]
        if item["impact"] == "HIGH"
    ]

    medium_signals = [
        item["signal"]
        for item in investigation["explainability"]
        if item["impact"] == "MEDIUM"
    ]

    return {

        "success": True,

        "problem": problem,

        "issue": category,

        "root_cause":
            root_causes.get(
                category,
                "Merchant issue requires investigation"
            ),

        "resolution_plan":
            resolution_plan,

        "guardrail":
            guardrail,

        "decision":
            decision["decision"],

        "decision_type":
            decision["decision_type"],

        "findings":
            investigation["findings"],

        "evidence":
            investigation["signals"],

        "confidence":
            confidence,

        "risk_score":
            investigation["risk_score"],

        "risk_level":
            investigation["risk_level"],

        "human_review":
            investigation["risk_score"] >= 75,

        "ai_reasoning":
            ai_reasoning,

        "contributing_signals":
            investigation["explainability"],

        "signal_summary": {

            "high_impact":
                high_signals,

            "medium_impact":
                medium_signals,

            "total_signals":
                len(investigation["signals"]),
        },

        "human_review_reason":
            human_review_reason,

        "guardrail_reason":
            guardrail["reason"],

        "decision_reason":
            (
                "High-risk case requires human review."
                if investigation["risk_score"] >= 75
                else
                "AI recommends the next operational step "
                "based on the observed merchant signals."
            ),

        "audit": {

            "model":
                "Hybrid Keyword Signals + TF-IDF + Logistic Regression",

            "classification_method":
                "Keyword signals + supervised text classification",

            "signals_used":
                len(investigation["signals"]),

            "explainability_enabled":
                True,

            "human_in_control":
                True,

            "financial_action_allowed":
                False,

            "prototype":
                True,
        }
    }


# ============================================================
# WHAT-IF SIMULATOR
# ============================================================

class SimulationRequest(BaseModel):

    kyc_status: str = "Pending"

    payment_failure_rate: float = 6.7

    risk_score: int = 78

    settlement_status: str = "On Hold"

    pending_refunds: int = 2

    unusual_activity: bool = False


@app.post("/simulate")
def simulate(request: SimulationRequest):

    score = int(request.risk_score)

    signals = []
    reasoning = []

    if request.kyc_status.lower() == "pending":

        score += 10

        signals.append(
            "KYC still pending"
        )

        reasoning.append(
            "Pending KYC increases operational risk."
        )

    else:

        score -= 5

        reasoning.append(
            "Verified KYC reduces verification-related risk."
        )

    if request.payment_failure_rate >= 30:

        score += 15

        signals.append(
            f"High payment failure rate: "
            f"{request.payment_failure_rate}%"
        )

        reasoning.append(
            "Very high payment failures increase transaction risk."
        )

    elif request.payment_failure_rate >= 15:

        score += 8

        signals.append(
            f"Elevated payment failure rate: "
            f"{request.payment_failure_rate}%"
        )

        reasoning.append(
            "Elevated payment failures increase operational risk."
        )

    elif request.payment_failure_rate < 10:

        score -= 5

        reasoning.append(
            "Low payment failure rate reduces payment-related risk."
        )

    if request.settlement_status.lower() == "on hold":

        score += 10

        signals.append(
            "Settlement remains on hold"
        )

        reasoning.append(
            "Settlement hold increases financial-operation risk."
        )

    elif request.settlement_status.lower() == "completed":

        score -= 5

        reasoning.append(
            "Completed settlement reduces settlement risk."
        )

    if request.pending_refunds >= 5:

        score += 8

        signals.append(
            f"{request.pending_refunds} pending refunds"
        )

        reasoning.append(
            "A high number of pending refunds increases "
            "unresolved workload."
        )

    elif request.pending_refunds == 0:

        score -= 4

        reasoning.append(
            "No pending refunds reduces unresolved refund risk."
        )

    if request.unusual_activity:

        score += 15

        signals.append(
            "Unusual activity detected"
        )

        reasoning.append(
            "Unusual activity significantly increases "
            "review requirements."
        )

    score = max(
        0,
        min(100, score)
    )

    level = risk_level(score)

    if score >= 75:

        decision = "Escalate to Human Review"

        recommendation = (
            "High-risk scenario. Avoid automatic "
            "financial or account changes."
        )

    elif score >= 45:

        decision = "Investigate Further"

        recommendation = (
            "Review supporting signals before taking action."
        )

    else:

        decision = "Low Risk"

        recommendation = (
            "Scenario appears stable based on available signals."
        )

    return {

        "success": True,

        "simulation": True,

        "risk_score":
            score,

        "risk_level":
            level,

        "decision":
            decision,

        "recommendation":
            recommendation,

        "root_cause":
            "Combined merchant operational risk",

        "signals":
            signals,

        "reasoning":
            reasoning,

        "guardrail":
            {
                "action": "Simulation Only",
                "reason": (
                    "No real merchant, payment, settlement, "
                    "refund, or account changes are performed."
                )
            },

        "scenario": {

            "kyc_status":
                request.kyc_status,

            "payment_failure_rate":
                request.payment_failure_rate,

            "risk_score_input":
                request.risk_score,

            "settlement_status":
                request.settlement_status,

            "pending_refunds":
                request.pending_refunds,

            "unusual_activity":
                request.unusual_activity,
        }
    }


# ============================================================
# INCIDENT INTELLIGENCE
# ============================================================

class IncidentRequest(BaseModel):

    cases: list[dict]


def normalize_text(text):

    if text is None:
        return ""

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def get_case_text(case):

    parts = [

        case.get("problem", ""),

        case.get("issue", ""),

        case.get("rootCause", ""),

        case.get("root_cause", ""),

        case.get("summary", ""),

        case.get("decision", ""),
    ]

    return normalize_text(
        " ".join(
            str(part)
            for part in parts
            if part
        )
    )


def get_case_risk(case):

    risk = case.get("risk")

    if risk:
        return str(risk).upper()

    risk_level_value = case.get("risk_level")

    if risk_level_value:
        return str(risk_level_value).upper()

    score = case.get("risk_score")

    if score is not None:

        try:
            return risk_level(
                int(score)
            )
        except Exception:
            pass

    return "LOW"


def get_case_confidence(case):

    value = case.get(
        "confidence",
        0
    )

    try:

        value = float(value)

        if value > 1:
            value = value / 100

        return value

    except Exception:

        return 0


def cluster_cases(cases):

    if not cases:
        return []

    texts = [
        get_case_text(case)
        for case in cases
    ]

    if len(cases) == 1:

        category = cases[0].get(
            "issue",
            "Unknown"
        )

        risk = get_case_risk(
            cases[0]
        )

        confidence = get_case_confidence(
            cases[0]
        )

        return [{

            "cluster_id":
                "INC-001",

            "title":
                f"{category} Incident",

            "category":
                category,

            "case_count":
                1,

            "risk_level":
                risk,

            "average_confidence":
                round(
                    confidence,
                    2
                ),

            "priority":
                risk,

            "summary":
                "One historical incident is available for comparison.",

            "cases":
                cases,
        }]

    vectorizer_local = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2)
    )

    try:

        matrix = vectorizer_local.fit_transform(
            texts
        )

        similarity = cosine_similarity(
            matrix
        )

    except ValueError:

        similarity = None

    clusters = []

    assigned = set()

    threshold = 0.25

    for i in range(len(cases)):

        if i in assigned:
            continue

        current_cluster = [i]

        assigned.add(i)

        for j in range(
            i + 1,
            len(cases)
        ):

            if j in assigned:
                continue

            issue_i = cases[i].get(
                "issue"
            )

            issue_j = cases[j].get(
                "issue"
            )

            same_issue = (
                issue_i
                and issue_j
                and str(issue_i).lower()
                == str(issue_j).lower()
            )

            similar = False

            if similarity is not None:

                similar = (
                    similarity[i][j]
                    >= threshold
                )

            if same_issue or similar:

                current_cluster.append(j)

                assigned.add(j)

        cluster_data = [
            cases[index]
            for index in current_cluster
        ]

        categories = [
            case.get(
                "issue",
                "Unknown"
            )
            for case in cluster_data
        ]

        category = max(
            set(categories),
            key=categories.count
        )

        risk_order = {
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1
        }

        highest_risk = max(
            cluster_data,
            key=lambda case:
                risk_order.get(
                    get_case_risk(case),
                    1
                )
        )

        highest_risk_level = get_case_risk(
            highest_risk
        )

        confidences = [
            get_case_confidence(case)
            for case in cluster_data
            if get_case_confidence(case) > 0
        ]

        avg_confidence = (
            mean(confidences)
            if confidences
            else 0
        )

        titles = {

            "Payment":
                "Payment Incident",

            "Settlement":
                "Settlement Incident",

            "KYC":
                "KYC Incident",

            "Refund":
                "Refund Incident",

            "Account":
                "Account Incident",
        }

        title = titles.get(
            category,
            "Merchant Incident"
        )

        summary = (
            f"{len(cluster_data)} related "
            f"{str(category).lower()} case(s) detected. "
            f"Highest observed risk is "
            f"{highest_risk_level}."
        )

        clusters.append({

            "cluster_id":
                f"INC-{len(clusters) + 1:03d}",

            "title":
                title,

            "category":
                category,

            "case_count":
                len(cluster_data),

            "risk_level":
                highest_risk_level,

            "average_confidence":
                round(
                    avg_confidence,
                    2
                ),

            "priority":
                highest_risk_level,

            "summary":
                summary,

            "cases":
                cluster_data,
        })

    clusters.sort(

        key=lambda cluster:
            {
                "HIGH": 3,
                "MEDIUM": 2,
                "LOW": 1,
            }.get(
                cluster["priority"],
                1
            ),

        reverse=True,
    )

    return clusters


# ============================================================
# INCIDENT ENDPOINT
# ============================================================

@app.post("/incidents")
def incidents(request: IncidentRequest):

    cases = request.cases

    # ========================================================
    # PROTOTYPE HISTORICAL MEMORY
    # ========================================================

    if not cases:

        cases = [

            {
                "case_id": "HIST-001",
                "problem":
                    "Merchant settlement was delayed",
                "issue":
                    "Settlement",
                "root_cause":
                    "Settlement hold due to verification review",
                "risk":
                    "HIGH",
                "risk_score":
                    81,
                "confidence":
                    0.93,
                "summary":
                    "Settlement delayed while merchant "
                    "verification was reviewed."
            },

            {
                "case_id": "HIST-002",
                "problem":
                    "Payout has not arrived for merchant",
                "issue":
                    "Settlement",
                "root_cause":
                    "Delayed payout processing",
                "risk":
                    "MEDIUM",
                "risk_score":
                    62,
                "confidence":
                    0.91,
                "summary":
                    "Merchant payout exceeded the expected "
                    "settlement timeline."
            },

            {
                "case_id": "HIST-003",
                "problem":
                    "Merchant settlement is on hold",
                "issue":
                    "Settlement",
                "root_cause":
                    "Settlement compliance review",
                "risk":
                    "HIGH",
                "risk_score":
                    78,
                "confidence":
                    0.92,
                "summary":
                    "Settlement was held pending operational review."
            },

            {
                "case_id": "HIST-004",
                "problem":
                    "Customer payments are failing",
                "issue":
                    "Payment",
                "root_cause":
                    "High transaction failure rate",
                "risk":
                    "HIGH",
                "risk_score":
                    76,
                "confidence":
                    0.90,
                "summary":
                    "Repeated payment failures were detected."
            },

            {
                "case_id": "HIST-005",
                "problem":
                    "Merchant KYC verification is pending",
                "issue":
                    "KYC",
                "root_cause":
                    "Missing business verification document",
                "risk":
                    "MEDIUM",
                "risk_score":
                    58,
                "confidence":
                    0.92,
                "summary":
                    "Merchant verification remained incomplete."
            },

            {
                "case_id": "HIST-006",
                "problem":
                    "Customer refund is still pending",
                "issue":
                    "Refund",
                "root_cause":
                    "Refund processing delay",
                "risk":
                    "MEDIUM",
                "risk_score":
                    55,
                "confidence":
                    0.89,
                "summary":
                    "Customer refund remained unresolved."
            }
        ]

        demo_mode = True

    else:

        demo_mode = False

    clusters = cluster_cases(
        cases
    )

    return {

        "success":
            True,

        "total_cases":
            len(cases),

        "cluster_count":
            len(clusters),

        "clusters":
            clusters,

        "demo_mode":
            demo_mode,

        "engine":
            (
                "TF-IDF similarity + "
                "issue category matching"
            ),

        "message":
            (
                "Prototype historical incidents used "
                "for comparison."
                if demo_mode
                else
                "Historical merchant cases analyzed successfully."
            )
    }


# ============================================================
# MODEL EVALUATION
# ============================================================

evaluation_examples = [

    ("My settlement is delayed", "Settlement"),
    ("My payout has not arrived", "Settlement"),
    ("Settlement amount is on hold", "Settlement"),
    ("Why is my settlement pending?", "Settlement"),

    ("My payment failed", "Payment"),
    ("Customers cannot complete checkout", "Payment"),
    ("Transactions are being declined", "Payment"),
    ("Payment failure rate is increasing", "Payment"),

    ("My KYC is pending", "KYC"),
    ("Business verification is incomplete", "KYC"),
    ("I need to submit a verification document", "KYC"),
    ("Why is my merchant verification pending?", "KYC"),

    ("Customer refund is pending", "Refund"),
    ("Refund has not reached the customer", "Refund"),
    ("My refund is delayed", "Refund"),
    ("Customer has not received money back", "Refund"),

    ("My merchant account is blocked", "Account"),
    ("I cannot access my account", "Account"),
    ("My account login is not working", "Account"),
    ("There is an issue with my merchant account", "Account"),
]


def evaluate_model():

    texts = [
        item[0]
        for item in evaluation_examples
    ]

    actual_labels = [
        item[1]
        for item in evaluation_examples
    ]

    predictions = []

    for text in texts:

        predictions.append(
            classify_problem(text)
        )

    correct = sum(
        1
        for actual, predicted
        in zip(
            actual_labels,
            predictions
        )
        if actual == predicted
    )

    total = len(
        actual_labels
    )

    accuracy = (
        correct / total
        if total > 0
        else 0
    )

    categories = [
        "Settlement",
        "Payment",
        "KYC",
        "Refund",
        "Account"
    ]

    category_results = {}

    for category in categories:

        category_total = 0
        category_correct = 0

        for actual, predicted in zip(
            actual_labels,
            predictions
        ):

            if actual == category:

                category_total += 1

                if predicted == actual:
                    category_correct += 1

        category_accuracy = (
            category_correct / category_total
            if category_total > 0
            else 0
        )

        category_results[category] = {

            "total":
                category_total,

            "correct":
                category_correct,

            "accuracy":
                round(
                    category_accuracy * 100,
                    2
                )
        }

    return {

        "model":
            "Hybrid Keyword Signals + TF-IDF + Logistic Regression",

        "classification_method":
            "Keyword signals + supervised text classification",

        "total_test_cases":
            total,

        "correct_predictions":
            correct,

        "incorrect_predictions":
            total - correct,

        "accuracy":
            round(
                accuracy * 100,
                2
            ),

        "category_performance":
            category_results,

        "evaluation_type":
            "Labeled merchant issue test set",

        "note":
            (
                "This evaluation uses a small built-in "
                "prototype dataset and should not be treated "
                "as production model performance."
            )
    }


# ============================================================
# EVALUATION ENDPOINT
# ============================================================

@app.get("/evaluate")
def evaluate():

    return {

        "success":
            True,

        **evaluate_model()
    }