# Security Policy

## Supported Versions

This project is an MVP. Security fixes are handled on the latest version of the main branch.

## Reporting a Vulnerability

Please do not open a public issue for suspected vulnerabilities. If you fork or deploy this project, create a private reporting channel for your deployment and document it in your own README.

## Security Notes

- Never commit `.env`, `.env.local`, Supabase service role keys, JWT secrets, or LLM API keys.
- Keep `SUPABASE_SERVICE_ROLE_KEY` on the backend only.
- Use HTTPS in production.
- Set `FRONTEND_ORIGIN` to the exact deployed frontend origin.
- Use Supabase Row Level Security and private Storage buckets.
- Review your LLM provider's data retention and privacy terms before sending uploaded policy text to it.
- Do not treat this MVP as production-ready for regulated insurance, financial, legal, or healthcare workloads without a full security and compliance review.

