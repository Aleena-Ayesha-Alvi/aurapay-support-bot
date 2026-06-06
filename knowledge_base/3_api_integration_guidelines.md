# AuraPay Developer API Guidelines

## Authentication
The AuraPay REST API utilizes OAuth 2.0 for authentication. Developers must pass a valid Bearer Token in the authorization header of every request. Tokens expire every 3600 seconds. Test environment (Sandbox) keys begin with `sk_test_`, while live production keys begin with `sk_live_`.

## Rate Limiting
To ensure platform stability, the API enforces rate limits. Standard endpoints allow 100 requests per second (RPS) per IP address. High-volume endpoints, such as the `/v1/charges` endpoint, allow 50 RPS. Exceeding these limits will return an HTTP 429 "Too Many Requests" status code.

## Webhooks
Merchants must configure Webhook endpoints to receive asynchronous events (e.g., `payment.succeeded`, `chargeback.created`). Webhook payloads are signed using a cryptographic Hash-based Message Authentication Code (HMAC). Developers must verify the `AuraPay-Signature` header to prevent replay attacks.


---

# AuraPay (EU region) Developer API Guidelines

## Authentication
The AuraPay (EU region) REST API utilizes OAuth 2.0 for authentication. Developers must pass a valid Bearer Token in the authorization header of every request. Tokens expire every 3600 seconds. Test environment (Sandbox) keys begin with `sk_test_`, while live production keys begin with `sk_live_`.

## Rate Limiting
To ensure platform stability, the API enforces rate limits. Standard endpoints allow 100 requests per second (RPS) per IP address. High-volume endpoints, such as the `/v1/charges` endpoint, allow 50 RPS. Exceeding these limits will return an HTTP 429 "Too Many Requests" status code.

## Webhooks
Merchants must configure Webhook endpoints to receive asynchronous events (e.g., `payment.succeeded`, `chargeback.created`). Webhook payloads are signed using a cryptographic Hash-based Message Authentication Code (HMAC). Developers must verify the `AuraPay (EU region)-Signature` header to prevent replay attacks.
