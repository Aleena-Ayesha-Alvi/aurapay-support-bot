# Task 2: Quality Assurance & RAG Testing Protocol

## Category 1: Contextual Memory & Base Retrieval
**Query 1:** "I am setting up a new merchant account and expect to process about $15,000 a month. What documents do I need to provide?"
**Expected Behavior:** Must identify the user as a "Tier 2 merchant" and state the requirement for UBO declarations and a Certificate of Incorporation.
**Result:** As you expect to process more than $10,000 per month, you are considered a Tier 2 merchant. To verify your identity, you will need to provide Ultimate Beneficial Ownership (UBO) declarations and a Certificate of Incorporation. (Source: AuraPay Merchant Onboarding Guidelines)

**Query 2:** "Wait, going back to my processing volume from earlier. Will that volume alone trigger a Suspicious Activity Report (SAR) under AML laws?"
**Expected Behavior:** Must search back through the chat history to remember the $15,000 figure, compare it to the AML policy, and explicitly state the $50,000 threshold. 
**Result:** No, your processing volume of 15,000 per month will not trigger a Suspicious Activity Report (SAR) solely based on the volume. According to AuraPay's policies, transactions exceeding 50,000 USD equivalent trigger an automated SAR review. *(Success - MMR Search Upgrade Fixed Previous Miss).*

## Category 2: Technical Accuracy & Follow-Ups
**Query 1:** "My developer is asking about rate limits. We are getting Error Code 429 on the standard endpoints. What is the limit?"
**Expected Behavior:** Must identify Error 429 as "Too Many Requests" and cite 100 RPS.
**Result:** The standard endpoints for AuraPay have a rate limit of 100 requests per second (RPS) per IP address. If you exceed this limit, you will receive an HTTP 429 "Too Many Requests" status code. *(Success - MMR Search Upgrade Fixed Previous Miss).*

**Query 2:** "What if we are hitting the /v1/charges endpoint instead? Is the limit the same?"
**Expected Behavior:** Must realize we are still talking about rate limits and pull the specific exception.
**Result:** No, the rate limit for the /v1/charges endpoint is different. It is considered a high-volume endpoint and has a rate limit of 50 requests per second (RPS) per IP address.

## Category 3: Abrupt Topic Switching & Multi-Part Extraction
**Query 1:** "I just got an 'Item Not Received' chargeback dispute. What fee do I have to pay?"
**Expected Behavior:** Must abandon API context and accurately quote the non-refundable $15 Chargeback Fee.
**Result:** When a cardholder disputes a charge, a non-refundable $15 Chargeback Fee is assessed to the merchant.

**Query 2:** "What evidence do I need to submit to fight that specific dispute, and how many days do I have?"
**Expected Behavior:** Must remember the chargeback context and extract both the 15-day limit and the tracking number requirement.
**Result:** For an "Item Not Received" dispute, you must provide a valid tracking number showing delivery to the AVS-verified address. You have exactly 15 calendar days to submit this compelling evidence.

## Category 4: Long-Term Session Memory
**Query 1 (Turn 5):** "my name is priyanshu agarwal"
**Query 2 (Turn 12):** "you remember my name"
**Expected Behavior:** The agent must retain exact string data across a deeply technical 12-turn conversation without dropping the entity.
**Result:** Your name is Priyanshu Agarwal. *(Success - Proves total historical retention is active).*

## Category 5: Guardrails & Context Dilution Limitations
**Query 1 (Out-of-Domain Trap):** "Who is the CEO of AuraPay and what year was the company founded?"
**Expected Behavior:** Must strictly refuse to answer using the exact guardrail phrasing without making up a CEO.
**Result:** I do not have that information in my current documentation. *(Success).*

**Query 2 (Policy Violation/Escalation):** "I'm going to message Tier 3 directly on Slack to complain. Is that allowed?"
**Expected Behavior:** Must warn the user that Tier 1/2 cannot contact Tier 3 on Slack.
**Result:** No, that is not allowed. Tier 1 and Tier 2 agents, as well as merchants, must never contact Tier 3 directly via Slack. All escalations must go through Jira. *(Success).*

**Query 3 (Context Dilution / Legal Conflict):** "One of my European customers used the 'Right to be Forgotten' under GDPR. Can I delete their transaction history?"
**Result:** I do not have that information in my current documentation.
**Engineering Note:** *Retrieval Miss due to Context Dilution.* Because the system is mandated to keep the full chat history active, by Turn 9 the historical payload was so massive that the LLM generated a noisy vector search query, missing the GDPR document. In a production environment, implementing a "Sliding Window" memory (keeping only the last 3 turns active) would immediately resolve this.