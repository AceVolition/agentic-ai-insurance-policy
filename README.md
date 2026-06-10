# Agentic AI Insurance Policy

Full-stack MVP based exclusively on the supplied PRD and System Design docs.

> This is an educational MVP. It is not legal advice, insurance advice, financial advice, or a production compliance system. See [Privacy and Disclaimer](PRIVACY_AND_DISCLAIMER.md).

## Stack

- Frontend: Next.js App Router, React, Tailwind CSS, shadcn/ui-style components
- Backend: FastAPI
- AI orchestration: LangGraph supervisor plus specialized agents
- LLM provider layer: DeepSeek default, with Claude/OpenAI/Gemini stubs
- Database and storage: Supabase PostgreSQL + private Storage bucket
- Auth: Supabase Auth

## Project Structure

```text
frontend/                 Next.js app
backend/                  FastAPI app
supabase/migrations/      PostgreSQL, RLS, trigger, storage bucket SQL
```

## Prerequisites

- Node.js 20+
- Python 3.11+
- A Supabase project
- DeepSeek API key
- Tesseract OCR installed locally if scanned PDFs need OCR fallback

## Open Source Safety

Before publishing your fork or deployment:

- Commit example env files only. Do not commit `.env`, `.env.local`, real API keys, JWT secrets, or Supabase service role keys.
- Keep `SUPABASE_SERVICE_ROLE_KEY` on the backend only. Never expose it in Vercel or browser-accessible variables.
- Review [SECURITY.md](SECURITY.md) and [PRIVACY_AND_DISCLAIMER.md](PRIVACY_AND_DISCLAIMER.md).
- Add your own privacy policy and terms if real users can upload policies.
- Review your LLM provider's data retention terms before sending policy text to it.
- Treat uploaded policies as sensitive personal documents.

## Supabase Setup

1. Create a Supabase project.
2. Run the migration in `supabase/migrations/001_initial_schema.sql` from the Supabase SQL editor or Supabase CLI.
3. Copy the project URL, anon key, service role key, and JWT secret into your env files.
4. Ensure the private `policies` storage bucket exists. The migration creates it when allowed by your Supabase permissions.

## Environment

Copy the examples:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
```

Fill in:

- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `SUPABASE_JWT_SECRET`
- `DEEPSEEK_API_KEY`
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`

## Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`.

Implemented endpoints from the system design:

- `POST /auth/signup`
- `POST /auth/login`
- `POST /policies/upload`
- `GET /policies/{id}`
- `POST /analysis/run/{policy_id}`
- `GET /analysis/{policy_id}`
- `POST /chat/{policy_id}`

The dashboard also uses `GET /policies` to show all policies for the signed-in user.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## MVP Flow

1. Sign up or sign in with Supabase Auth.
2. Upload a policy PDF.
3. FastAPI stores the PDF in private Supabase Storage.
4. The LangGraph supervisor runs:
   - PDF Parsing Agent
   - Policy Summary Agent
   - Exclusion Detection Agent
   - Risk Detection Agent
   - Claim Denial Explanation Agent
   - Appeal Recommendation Agent
   - Policy Comparison Agent
5. Results are stored in PostgreSQL and displayed in the dashboard.
6. Ask follow-up questions in the policy chat.

## Notes

- Storage object paths are user-scoped, and API responses use signed URLs.
- The backend uses the Supabase service role key for server-side inserts and storage operations.
- Browser auth uses the Supabase anon key; FastAPI validates Supabase JWTs.
- DeepSeek is the default provider at `https://api.deepseek.com/v1/chat/completions`.
- AI outputs can be incomplete or incorrect. Users should verify results against the original policy and consult qualified professionals before making coverage, claim, appeal, or purchasing decisions.

## License

MIT. See [LICENSE](LICENSE).
