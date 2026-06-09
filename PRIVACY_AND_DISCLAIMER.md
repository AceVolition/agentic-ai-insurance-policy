# Privacy and Disclaimer

## Privacy Notice

This application processes insurance policy documents uploaded by users. Insurance policies may contain personal information, addresses, financial information, vehicle or property details, claim history, and other sensitive data.

When deployed, the application may send extracted policy text and user questions to the configured LLM provider, such as DeepSeek. Operators of this software are responsible for reviewing the provider's privacy, security, data retention, and compliance terms before allowing real users to upload documents.

The MVP stores uploaded PDFs in Supabase Storage and stores analysis results and chat history in Supabase PostgreSQL. Deployers are responsible for configuring Supabase security, access controls, backups, retention periods, and deletion workflows.

## Legal and Insurance Disclaimer

This software does not provide legal advice, insurance advice, financial advice, or claims handling services. AI-generated summaries, risk flags, exclusion lists, denial explanations, appeal recommendations, and chat responses may be incomplete or incorrect.

Users should verify all outputs against the original policy documents and consult a licensed insurance professional, attorney, or qualified advisor before making coverage, claim, appeal, cancellation, or purchasing decisions.

## Open Source Use

This repository is provided as an educational MVP. If you deploy it for other people, you are responsible for adding your own privacy policy, terms of service, abuse controls, logging policy, incident response plan, and compliance review.

