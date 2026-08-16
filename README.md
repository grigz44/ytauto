# YT Shorts Automation

Dashboard (Render) + daily pipeline (GitHub Actions) for generating and publishing
YouTube Shorts. See the project brief for the full design; this README covers
environment setup.

## Phase 1 — Foundation

What exists at this phase: a Flask dashboard that reports whether Render and
Supabase are wired up correctly, the DB schema, and a weekly Supabase
keep-alive workflow. No topics/settings CRUD, no AI, no video yet — that's
Phase 2 onward.

### 1. Push this repo to GitHub

```
git init
git add .
git commit -m "Phase 1: foundation scaffold"
gh repo create ytauto --public --source=. --remote=origin --push
```

(Public repo = unlimited free GitHub Actions minutes. If you'd rather use the
web UI: create a new repo at github.com/new, then `git remote add origin <url>`
and `git push -u origin main`.)

### 2. Create the Supabase project

1. https://supabase.com → New project (free tier).
2. SQL Editor → paste the contents of [`db/schema.sql`](db/schema.sql) → Run.
3. Settings → Database → Connection string → URI. Use the **Transaction
   pooler** entry (port 6543) — it works more reliably from Render's network
   than the direct :5432 connection. Copy it; you'll need it twice (Render env
   var and GitHub secret).

### 3. Deploy the web service on Render

1. https://render.com → New → Web Service → connect your GitHub repo.
2. Render should detect `render.yaml` and pre-fill the service (Python,
   `pip install -r requirements.txt`, `gunicorn app.main:app`). If it doesn't
   auto-detect, set those manually and pick the **Free** plan.
3. In the service's Environment tab, set:
   - `DATABASE_URL` — the Supabase pooler connection string from step 2
   - `FLASK_SECRET_KEY` — any random string
4. Deploy. Once live, open the service URL — the Supabase card on the
   dashboard should show **connected**.

### 4. Add the GitHub secret for keep-alive

Repo → Settings → Secrets and variables → Actions → New repository secret:
- Name: `DATABASE_URL`
- Value: same Supabase pooler connection string

Then Actions tab → "Supabase Keep-Alive" → Run workflow, to confirm it passes
before waiting for the weekly schedule.

### 5. Verify Phase 1 is done

- [ ] Render URL loads and shows the dashboard
- [ ] Supabase card shows "connected"
- [ ] `db/schema.sql` has been applied (4 tables exist in Supabase's Table
      Editor: `topics`, `settings`, `shorts`, `youtube_accounts`)
- [ ] "Supabase Keep-Alive" workflow run succeeds manually via
      `workflow_dispatch`

Once all four are checked, Phase 2 (dashboard shell + Topics CRUD) starts.

## Local development

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # fill in DATABASE_URL
python -m app.main
```

Visit http://localhost:5000.
