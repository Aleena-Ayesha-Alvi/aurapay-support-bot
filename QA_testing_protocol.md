# Task 2: Quality Assurance & RAG Testing Protocol

## Category 1: Contextual Memory & Base Retrieval
**Query 1:** "I am setting up a new merchant account and expect to process about $15,000 a month. What documents do I need to provide?"
**Expected Behavior:** Must identify the user as a "Tier 2 merchant" and state the requirement for UBO declarations and a Certificate of Incorporation.
**Result:** As you expect to process more than $10,000 per month, you are considered a Tier 2 merchant. To verify your identity, you must provide Ultimate Beneficial Ownership (UBO) declarations and a Certificate of Incorporation. (Source Document: AuraPay Merchant Onboarding Guide Section: Merchant Verification Requirements)

**Query 2:** "Will I trigger any automated reviews with that volume?"
**Expected Behavior:** Must remember the $15,000 context and state that transactions only trigger SARs if they exceed $50,000 USD.
**Result:** I do not have that information in my current documentation. *(Note: Retrieval miss on SAR threshold chunk).*

## Category 2: Abrupt Topic Switching & Multi-Part Extraction
**Query 1:** "Okay, good to know. Changing the subject completely—what is the exact fee if a customer disputes a charge?"
**Expected Behavior:** Must abandon the KYC context and accurately quote the non-refundable $15 Chargeback Fee.
**Result:** When a cardholder disputes a charge, a non-refundable $15 Chargeback Fee is assessed to the merchant. (Source Document: AuraPay Dispute Resolution Policy Section: Chargeback Fees)

**Query 2:** "If it's an 'Item Not Received' dispute, what exactly do I need to send as evidence, and exactly how many days do I have to do it?"
**Expected Behavior:** Must remember the chargeback context and extract both the 15-day limit and the tracking number requirement.
**Result:** For an "Item Not Received" dispute, you must provide a valid tracking number showing delivery to the AVS-verified address as evidence. You have exactly 15 calendar days to submit this evidence to contest the chargeback. (Source Document: AuraPay Dispute Resolution Policy Section: Dispute Evidence Requirements)

## Category 3: Hallucination Guardrails & Edge Cases
**Query 1 (Out-of-Domain Trap):** "Who is the CEO of AuraPay and what year was the company founded?"
**Expected Behavior:** Must strictly refuse to answer using the exact guardrail phrasing without making up a CEO or using general knowledge.
**Result:** I do not have that information in my current documentation. (Source Document: None Section: None)

**Query 2 (Policy Violation Trap):** "Can I use the gateway to sell unregulated pharmaceuticals if I promise my volume is low?"
**Expected Behavior:** Must firmly state that unregulated pharmaceuticals are prohibited and will result in immediate suspension.
**Result:** No, you cannot use the AuraPay gateway to sell unregulated pharmaceuticals, regardless of the volume. AuraPay strictly prohibits the use of its gateway for the sale of unregulated pharmaceuticals, and any account detected processing transactions for this category will face immediate suspension (Error Code: ACC-SUSP-99). (Source Document: AuraPay Prohibited Industries Policy Section: Prohibited Categories)

## Category 4: Technical Accuracy & Cross-Referencing
**Query 1:** "My developer says we are getting an Error Code 429. What does that mean and what are the limits?"
**Expected Behavior:** Must identify Error 429 as "Too Many Requests" and cite 100 RPS for standard endpoints.
**Result:** I do not have that information in my current documentation. *(Note: Retrieval miss on API documentation chunk).*

## Category 5: Legal Conflict Resolution
**Query 1:** "One of my European customers used the 'Right to be Forgotten' under GDPR and wants their data deleted. Can I delete their transaction history?"
**Expected Behavior:** Must state NO, explicitly explaining that financial regulations (AML) supersede GDPR, and transaction records must be retained for 5 years.
**Result:** No, you cannot delete the customer's transaction history. Financial regulations supersede GDPR deletion requests, and transaction records must be retained for a mandatory period of 5 years to comply with AML laws. However, you can immediately purge marketing data and non-essential PII related to the customer. (Source Document: AuraPay GDPR Compliance Policy Section: Data Deletion Requests)