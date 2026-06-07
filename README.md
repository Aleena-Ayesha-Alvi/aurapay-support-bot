# 💳 AuraPay Enterprise Support Agent

A Retrieval-Augmented Generation (RAG) based customer support assistant built for the DesiCrew Data Science Assessment.

The system answers enterprise payment gateway support questions using an internal knowledge base covering:

- KYC & AML Compliance
- Chargebacks & Disputes
- API Integration
- GDPR & Data Privacy
- Service Level Agreements (SLA)
- Support Escalation Policies

Unlike a generic chatbot, the assistant is grounded exclusively on company documentation and refuses to hallucinate answers outside the provided knowledge base.

## 🚀 Live Demo

https://desicrew-ds-assessment-776zueaju5dsv9hgfq93ph.streamlit.app/

---

## Problem Statement

Build an enterprise support chatbot capable of:

- Answering support questions using company documentation
- Maintaining multi-turn conversational context
- Providing source-backed responses
- Handling policy, compliance, legal, and technical questions
- Refusing to answer when information is unavailable

---

## Features

### Retrieval-Augmented Generation (RAG)

The assistant combines:

- Semantic Search
- Vector Embeddings
- Large Language Models

to generate grounded answers from internal documentation.

---

### Multi-Turn Conversation Memory

The assistant retains complete conversation history and can answer follow-up questions that depend on earlier context.

Example:

**User**

```text
I process about $15,000 per month. What documents do I need?
```

**Assistant**

```text
You are classified as a Tier 2 merchant and must provide:
- UBO Declaration
- Certificate of Incorporation
```

**User**

```text
Will that processing volume trigger a Suspicious Activity Report?
```

The assistant correctly remembers the previously mentioned $15,000 amount and answers using AML policy documentation. 

---

### Source-Grounded Responses

Every answer includes document provenance:

```text
Source Document:
3_api_integration_guidelines.md

Section:
Rate Limiting
```

This improves transparency and auditability. 
---

### Context Inspection

Users can inspect the exact retrieved chunks used to generate an answer through the UI.

This enables:

- Retrieval debugging
- Transparency
- Hallucination detection



---

### Session Management

The application provides:

- Persistent chat history
- Context retention
- One-click conversation reset

to support evaluation of long-running support sessions. 

---

## Architecture

```text
User Question
      │
      ▼
Conversation History
      │
      ▼
History-Aware Query Reformulation
      │
      ▼
FAISS Vector Search
      │
      ▼
Relevant Document Chunks
      │
      ▼
Llama 3.3 70B
      │
      ▼
Grounded Response
      │
      ▼
Source Citation
```

---

## Project Structure

```text
task2_support_bot/
│
├── app.py
├── prompts.py
├── vector_store.py
├── setup_docs.py
│
├── knowledge_base/
│   ├── 1_kyc_aml_compliance.md
│   ├── 2_chargeback_dispute_resolution.md
│   ├── 3_api_integration_guidelines.md
│   ├── 4_gdpr_data_privacy.md
│   ├── 5_merchant_sla.md
│   └── 6_support_escalation_matrix.md
│
├── faiss_index/
│
└── README.md
```

---

## Knowledge Base

The assistant is grounded on six enterprise documentation domains:

### KYC & AML Compliance

Includes:

- Customer Identification Program (CIP)
- Merchant Verification
- Suspicious Activity Reporting
- Prohibited Businesses

### Chargebacks & Disputes

Includes:

- Chargeback Lifecycle
- Compelling Evidence
- Arbitration Procedures
- Dispute Resolution Timelines

### API Integration

Includes:

- OAuth Authentication
- API Rate Limits
- Webhooks
- Security Verification

### GDPR & Privacy

Includes:

- Data Subject Access Requests
- Right to be Forgotten
- Data Breach Notification Rules

### Service Level Agreement (SLA)

Includes:

- Uptime Guarantees
- Maintenance Windows
- Service Credits

### Support Escalation Matrix

Includes:

- Tier 1 Responsibilities
- Tier 2 Responsibilities
- Tier 3 Restrictions
- Escalation Workflows



---

## Retrieval Pipeline

### Document Loading

Markdown files are loaded automatically from:

```text
knowledge_base/
```

### Hierarchical Chunking

The system uses:

1. Markdown Header Splitting
2. Recursive Character Splitting

This preserves document structure while maintaining retrieval quality. 

---

### Embeddings

Model:

```text
all-MiniLM-L6-v2
```

Used to convert document chunks into vector representations.

---

### Vector Database

Vector Store:

```text
FAISS
```

The generated index is cached locally to avoid rebuilding embeddings on every application startup. 

---

### Retrieval Strategy

Search Type:

```text
MMR (Max Marginal Relevance)
```

Configuration:

```python
k = 7
fetch_k = 20
```

This improves diversity and relevance of retrieved chunks. 
---

## Prompt Engineering

### Query Contextualization

A history-aware retriever reformulates follow-up questions into standalone queries before retrieval.

Example:

```text
What about that limit?
```

becomes:

```text
What is the API rate limit for /v1/charges?
```

based on prior conversation context. 

---

### Grounded Answer Generation

The assistant is instructed to:

- Use retrieved documentation only
- Never invent policies
- Never guess answers
- Return explicit refusal when information is unavailable

Fallback response:

```text
I do not have that information in my current documentation.
```


---

## Quality Assurance Testing

### Contextual Memory Testing

Scenario:

Merchant onboarding requirements followed by AML follow-up questions.

Result:

Assistant correctly retained prior merchant processing volume and applied AML thresholds. 

---

### Technical Accuracy Testing

Query:

```text
What is the rate limit for standard endpoints?
```

Result:

```text
100 RPS
```

Follow-Up:

```text
What about /v1/charges?
```

Result:

```text
50 RPS
```

Correctly retrieved endpoint-specific documentation. 

---

### Chargeback Workflow Testing

Query:

```text
What evidence is required for Item Not Received disputes?
```

Result:

- Tracking Number
- AVS Verified Address
- 15-Day Submission Window

Correctly extracted from dispute resolution policy. 

---

### Long-Term Memory Testing

A user's name was introduced early in the conversation and correctly recalled several turns later, demonstrating full historical context retention. 
---

### Out-of-Domain Testing

Query:

```text
Who is AuraPay's CEO?
```

Result:

```text
I do not have that information in my current documentation.
```

The assistant correctly refused to hallucinate information. 

---

## Limitations Observed

### Context Dilution

During very long conversations, retrieval quality may degrade because the reformulated query includes excessive historical context.

Observed Example:

A GDPR-related question failed retrieval after several unrelated conversation turns.

Potential Production Solution:

- Sliding Window Memory
- Conversation Summarization
- Hybrid Memory Architectures


---

## Technologies Used

### Frontend

- Streamlit

### LLM

- Groq
- Llama 3.3 70B Versatile

### Framework

- LangChain

### Embeddings

- HuggingFace Embeddings
- all-MiniLM-L6-v2

### Vector Database

- FAISS

### Retrieval

- History-Aware Retrieval
- MMR Search

### Knowledge Base

- Markdown Documentation

---

## Key Achievements

✅ Retrieval-Augmented Generation (RAG)

✅ Multi-turn conversational memory

✅ Source-grounded responses

✅ Document chunk transparency

✅ FAISS vector search

✅ History-aware retrieval

✅ Hallucination prevention

✅ Enterprise support knowledge base

✅ Compliance and policy assistance

---

## Author

**Priyanshu Agarwal**

IIT Madras BS in Data Science and Applications

DesiCrew Data Science Assessment Submission