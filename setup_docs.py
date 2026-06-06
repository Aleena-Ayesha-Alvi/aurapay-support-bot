import os

docs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge_base")
os.makedirs(docs_dir, exist_ok=True)

docs = {
    "1_kyc_aml_compliance.md": """# AuraPay KYC & AML Compliance Policy

## Customer Identification Program (CIP)
Under the Bank Secrecy Act and global Anti-Money Laundering (AML) laws, AuraPay must verify the identity of every merchant. Tier 1 merchants (processing <$10,000/month) require a government-issued ID and Proof of Address. Tier 2 merchants (processing >$10,000/month) must provide Ultimate Beneficial Ownership (UBO) declarations and a Certificate of Incorporation. 

## Prohibited Business Categories
AuraPay strictly prohibits the use of its gateway for the following industries: adult entertainment, unregulated pharmaceuticals, cryptocurrency tumbling services, and unregulated gambling. Any account detected processing transactions for these categories will face immediate suspension (Error Code: ACC-SUSP-99).

## Transaction Monitoring
All transactions exceeding $50,000 USD equivalent trigger an automated Suspicious Activity Report (SAR) review. Support agents must not disclose the existence of a SAR investigation to the merchant under any circumstances, as this constitutes "tipping off," which is a federal offense.
""",

    "2_chargeback_dispute_resolution.md": """# AuraPay Chargeback and Dispute Resolution

## The Chargeback Lifecycle
When a cardholder disputes a charge, the funds are immediately held, and a non-refundable $15 Chargeback Fee is assessed to the merchant. The merchant has exactly 15 calendar days to submit compelling evidence to contest the chargeback. If no evidence is submitted, the dispute is automatically resolved in favor of the cardholder.

## Compelling Evidence Requirements
For "Item Not Received" disputes, the merchant must provide a valid tracking number showing delivery to the AVS-verified address. For "Fraudulent Transaction" disputes, the merchant must provide the CVV match log, IP address of the purchaser, and any positive AVS (Address Verification System) response.

## Arbitration
If the merchant wins the initial representation but the cardholder's bank issues a pre-arbitration, the merchant may choose to accept the loss or push to the card network (Visa/Mastercard) for final arbitration. A network arbitration fee of $500 applies and is paid by the losing party.
""",

    "3_api_integration_guidelines.md": """# AuraPay Developer API Guidelines

## Authentication
The AuraPay REST API utilizes OAuth 2.0 for authentication. Developers must pass a valid Bearer Token in the authorization header of every request. Tokens expire every 3600 seconds. Test environment (Sandbox) keys begin with `sk_test_`, while live production keys begin with `sk_live_`.

## Rate Limiting
To ensure platform stability, the API enforces rate limits. Standard endpoints allow 100 requests per second (RPS) per IP address. High-volume endpoints, such as the `/v1/charges` endpoint, allow 50 RPS. Exceeding these limits will return an HTTP 429 "Too Many Requests" status code.

## Webhooks
Merchants must configure Webhook endpoints to receive asynchronous events (e.g., `payment.succeeded`, `chargeback.created`). Webhook payloads are signed using a cryptographic Hash-based Message Authentication Code (HMAC). Developers must verify the `AuraPay-Signature` header to prevent replay attacks.
""",

    "4_gdpr_data_privacy.md": """# AuraPay GDPR & Data Privacy Standards

## Data Subject Access Requests (DSAR)
Under the GDPR, European Union residents have the right to request a copy of all personal data AuraPay holds about them. Support agents must route all DSARs to the privacy team (privacy@aurapay.com). We have 30 days to comply with a DSAR from the date of identity verification.

## Right to be Forgotten
Customers may request data deletion. However, financial regulations supersede GDPR deletion requests. Transaction records, KYC documents, and chargeback history must be retained for a mandatory period of 5 years to comply with AML laws. Only marketing data and non-essential PII can be immediately purged.

## Data Breach Notification Protocol
In the event of unauthorized access to PII or Payment Card Industry (PCI) data, AuraPay is legally obligated to notify the relevant supervisory authority within 72 hours of becoming aware of the breach. Affected data subjects must be notified without undue delay.
""",

    "5_merchant_sla.md": """# AuraPay Service Level Agreement (SLA)

## Uptime Guarantees
AuraPay guarantees a 99.99% monthly uptime for its core payment processing API. This allows for approximately 4.32 minutes of allowable downtime per month. 

## Maintenance Windows
Scheduled maintenance will occur on the second Sunday of every month between 02:00 AM and 04:00 AM UTC. API traffic will be routed to secondary data centers during this time, but merchants may experience latency increases of up to 200ms.

## SLA Violation Compensation
If uptime falls below 99.99%, merchants are entitled to service credits. For 99.9% to 99.98% uptime, a 10% credit of monthly processing fees is applied. For uptime below 99.0%, a 30% credit is applied. Merchants must claim these credits by opening a Tier 2 support ticket within 30 days of the downtime event.
""",

    "6_support_escalation_matrix.md": """# Support Agent Escalation Matrix

## Tier 1: General Inquiries
Tier 1 agents handle password resets, basic dashboard navigation, API key generation, and standard payout questions. Target resolution time is 4 hours.

## Tier 2: Technical & Financial
Tier 2 agents handle webhook delivery failures, API integration errors (4xx and 5xx codes), chargeback arbitration, and manual payout reviews. Target resolution time is 24 hours.

## Tier 3: Legal & Security
Tier 3 is restricted to the Engineering and Legal teams. Escalations to Tier 3 involve suspected platform vulnerabilities, AML/SAR investigations, data breaches, and law enforcement subpoenas. Tier 1 and Tier 2 agents must NEVER contact Tier 3 directly via Slack; all escalations must go through the Jira ticketing system.
"""
}

# Write files and artificially pad them so the chunker works hard
for filename, content in docs.items():
    file_path = os.path.join(docs_dir, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        # Repeating the text to simulate a longer corporate document
        extended_content = content + "\n\n---\n\n" + content.replace("AuraPay", "AuraPay (EU region)")
        f.write(extended_content)

print(f"✅ Created 6 enterprise compliance and support documents in: {docs_dir}")