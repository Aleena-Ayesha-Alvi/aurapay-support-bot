# Task 2: Quality Assurance & RAG Testing Protocol

All queries below were run in order as a single 13-turn conversation against the current pipeline (GPT-4o mini via AI Pipe, temperature 0, FAISS MMR retrieval with k=7). Results are copied verbatim, citations included.

## Category 1: Contextual Memory & Base Retrieval
**Query 1 (Turn 1):** "I am setting up a new merchant account and expect to process about $15,000 a month. What documents do I need to provide?"
**Expected Behavior:** Must identify the user as a "Tier 2 merchant" and state the requirement for UBO declarations and a Certificate of Incorporation.
**Result:** As a Tier 2 merchant processing over $10,000 a month, you will need to provide the following documents: 1. Ultimate Beneficial Ownership (UBO) declarations. 2. Certificate of Incorporation. These documents are required to verify your identity under the Bank Secrecy Act and global Anti-Money Laundering (AML) laws.
**Source Document:** 1_kyc_aml_compliance.md | **Section:** Customer Identification Program (CIP) *(Pass)*

**Query 2 (Turn 2):** "Wait, going back to my processing volume from earlier. Will that volume alone trigger a Suspicious Activity Report (SAR) under AML laws?"
**Expected Behavior:** Must remember the $15,000 figure from the chat history, compare it to the AML policy, and state the $50,000 threshold.
**Result:** No, your processing volume of $15,000 a month will not trigger an automated Suspicious Activity Report (SAR) review. SAR reviews are triggered for transactions exceeding $50,000 USD equivalent.
**Source Document:** 1_kyc_aml_compliance.md | **Section:** Transaction Monitoring *(Pass)*

## Category 2: Technical Accuracy & Follow-Ups
**Query 1 (Turn 3):** "My developer is asking about rate limits. We are getting Error Code 429 on the standard endpoints. What is the limit?"
**Expected Behavior:** Must identify Error 429 as "Too Many Requests" and cite 100 RPS.
**Result:** The standard endpoints allow for 100 requests per second (RPS) per IP address. If you exceed this limit, you will receive an HTTP 429 "Too Many Requests" status code.
**Source Document:** 3_api_integration_guidelines.md | **Section:** Rate Limiting *(Pass)*

**Query 2 (Turn 4):** "What if we are hitting the /v1/charges endpoint instead? Is the limit the same?"
**Expected Behavior:** Must realize we are still talking about rate limits and pull the specific exception.
**Result:** No, the limit for the `/v1/charges` endpoint is different. It allows for 50 requests per second (RPS). Exceeding this limit will also return an HTTP 429 "Too Many Requests" status code.
**Source Document:** 3_api_integration_guidelines.md | **Section:** Rate Limiting *(Pass)*

## Category 3: Abrupt Topic Switching & Multi-Part Extraction
**Query 1 (Turn 6):** "I just got an 'Item Not Received' chargeback dispute. What fee do I have to pay?"
**Expected Behavior:** Must abandon API context and accurately quote the non-refundable $15 Chargeback Fee.
**Result:** For an 'Item Not Received' chargeback dispute, you will be assessed a non-refundable $15 Chargeback Fee. Additionally, you have 15 calendar days to submit compelling evidence to contest the chargeback. If you do not submit evidence, the dispute will be resolved in favor of the cardholder.
**Source Document:** 2_chargeback_dispute_resolution.md | **Section:** The Chargeback Lifecycle *(Pass)*

**Query 2 (Turn 7):** "What evidence do I need to submit to fight that specific dispute, and how many days do I have?"
**Expected Behavior:** Must remember the chargeback context and extract both the 15-day limit and the tracking number requirement.
**Result:** To contest an 'Item Not Received' chargeback dispute, you must provide a valid tracking number showing delivery to the AVS-verified address. You have exactly 15 calendar days to submit this compelling evidence.
**Source Document:** 2_chargeback_dispute_resolution.md | **Section:** Compelling Evidence Requirements *(Pass)*

## Category 4: Long-Term Session Memory
**Query 1 (Turn 5):** "my name is priyanshu agarwal"
**Result:** Nice to meet you, Priyanshu! How can I assist you today?

**Query 2 (Turn 12):** "you remember my name"
**Expected Behavior:** The agent must retain exact string data across a deeply technical 12-turn conversation without dropping the entity.
**Result:** Yes, your name is Priyanshu Agarwal. How can I assist you further today? *(Pass)*
**Engineering Note:** After migrating to GPT-4o mini, the strict "answer only from context" rule caused the model to reply "I do not have that information in my current documentation." both to the introduction and to the recall question, even though the name was in the chat history. The QA prompt now distinguishes policy questions (context only, with citations) from facts the user shared in the conversation (answered from chat history, no citation).

## Category 5: Guardrails & Context Dilution
**Query 1 (Turn 8, Out-of-Domain Trap):** "Who is the CEO of AuraPay and what year was the company founded?"
**Expected Behavior:** Must strictly refuse to answer using the exact guardrail phrasing without making up a CEO.
**Result:** I do not have that information in my current documentation. *(Pass)*

**Query 2 (Turn 9, Context Dilution / Legal Conflict):** "One of my European customers used the 'Right to be Forgotten' under GDPR. Can I delete their transaction history?"
**Expected Behavior:** Must explain that financial regulations supersede GDPR and records must be retained.
**Result:** No, you cannot delete their transaction history. While customers may request data deletion under the 'Right to be Forgotten,' financial regulations supersede GDPR deletion requests. Transaction records, KYC documents, and chargeback history must be retained for a mandatory period of 5 years to comply with AML laws. Only marketing data and non-essential PII can be immediately purged.
**Source Document:** 4_gdpr_data_privacy.md | **Section:** Right to be Forgotten *(Pass)*
**Engineering Note:** With the previous Llama 3.3 setup this turn was a retrieval miss caused by context dilution: the long history produced a noisy reformulated search query. With GPT-4o mini the history-aware reformulation stays focused and the GDPR chunk is retrieved. A sliding-window memory remains a sensible safeguard for much longer sessions.

**Query 3 (Turn 10, Policy Violation/Escalation):** "I'm going to message Tier 3 directly on Slack to complain. Is that allowed?"
**Expected Behavior:** Must warn the user that Tier 3 cannot be contacted on Slack.
**Result:** No, you are not allowed to contact Tier 3 directly via Slack. All escalations to Tier 3 must go through the Jira ticketing system.
**Source Document:** 6_support_escalation_matrix.md | **Section:** Tier 3: Legal & Security *(Pass)*

**Query 4 (Turn 13, Off-Topic):** "What's the weather in Chennai today?"
**Result:** I do not have that information in my current documentation. *(Pass)*

## Category 6: Citation Accuracy
**Turn 11:** "When do API access tokens expire?"
**Result:** API access tokens expire every 3600 seconds (1 hour).
**Source Document:** 3_api_integration_guidelines.md | **Section:** Authentication *(Pass)*
**Engineering Note:** Originally, citations were emitted as literal placeholders (`[Insert source_file metadata here]`) because `create_stuff_documents_chain` only passes `page_content` to the LLM. A `DOCUMENT_PROMPT` now prefixes each chunk with its `source_file` and `Section` metadata, so every citation names a real file and section.

## Summary
13 / 13 turns passed.
