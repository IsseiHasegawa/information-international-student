# Plan — International Student Info Site (working title)

## Overview

- **Goal**: Provide international students in the U.S. with up-to-date, easy-to-read information on visas and government policy
- **Site language**: English
- **Tech**: HTML / CSS / JavaScript, Python (Flask), PostgreSQL
- **Team**: 2 people
  - **A** (Backend & Data): \_\_\_\_
  - **B** (Frontend & Content): \_\_\_\_

## How We Work

- Weekly meeting agenda
  1. Review last week's TODOs (mark finished items as `[x]`)
  2. Blockers and questions
  3. Pick this week's TODOs, assign owners, and set due dates
  4. Record decisions in the Decision Log
  5. Add an entry to the Weekly Log
- TODO format: `- [ ] Task [Owner] (Due: YYYY-MM-DD)`
  - Owner: `[A]`, `[B]`, or `[A+B]`
  - Leave `Due` blank until the task is scheduled
- Split any TODO that can't be finished within one week
- Create a GitHub Issue for implementation tasks and add its number (e.g., `#12`)

## Schedule (Estimate)

| Section                          | Target               | Due |
| -------------------------------- | -------------------- | --- |
| 1. Planning & Design             | Week 1–2             |     |
| 2. Dev Environment & CI/CD       | Week 1–2             |     |
| 3. Articles & Search (MVP)       | Week 3–6             |     |
| 4. Data Collection & Admin (MVP) | Week 3–6             |     |
| 5. Content                       | Week 2–6             |     |
| 6. Legal & Policies              | Week 2–6             |     |
| 7. Launch                        | Week 6–7             |     |
| 8. Notifications                 | Week 7–8             |     |
| 9. Q&A Forum                     | Week 9–11            |     |
| 10. Chatbot                      | Week 12–14           |     |
| 11. Operations                   | Ongoing after launch |     |

## Tech Stack

| Area                     | Choice                                                      |
| ------------------------ | ----------------------------------------------------------- |
| Web                      | Flask + Jinja2, organized with Blueprints                   |
| Database                 | PostgreSQL + SQLAlchemy + Flask-Migrate                     |
| Search                   | PostgreSQL full-text search (`tsvector`, `english` config)  |
| Data collection          | requests / feedparser / BeautifulSoup                       |
| Background jobs          | Separate worker process or cron (not inside the web server) |
| Auth & security          | Flask-Login, Flask-WTF (CSRF), Flask-Limiter                |
| Cache & rate limit store | Redis                                                       |
| Notifications            | Email delivery service + double opt-in                      |
| Chatbot                  | LLM API + RAG (approved articles only), pgvector            |
| Testing                  | pytest (with PostgreSQL service container)                  |
| CI/CD                    | GitHub Actions + auto-deploy via hosting provider           |
| Monitoring               | Sentry + uptime monitoring                                  |

```
app/
  __init__.py        # create_app()
  models.py
  articles/          # browsing & search
  admin/             # article management & review queue
  collectors/        # data collection
  notify/            # email subscriptions
  forum/             # Q&A forum
  chatbot/
  templates/  static/
tests/
  fixtures/          # saved responses from sources
worker.py            # scheduled jobs (runs as a separate process)
docker-compose.yml
.env.example
.github/workflows/   # CI
```

---

## TODO

### 1. Planning & Design

- [ ] Decide on site name and domain [A+B] (Due: )
- [ ] Define the scope of visas and topics (F-1, J-1, M-1, CPT/OPT/STEM OPT, travel & re-entry, post-graduation options, etc.) [A+B] (Due: )
- [ ] Define categories and tags (topic / visa type / nationality) [A+B] (Due: )
- [ ] List all pages and create wireframes (home, article list, article detail, search results, subscribe, admin) [B] (Due: )
- [ ] Design the database (articles, categories, tags, sources, fetched_items, collector_runs, subscribers, users, questions, answers, reports) [A] (Due: )
- [ ] Finalize the source list and test how to fetch each one (see "Sources" below) [A] (Due: )
- [ ] Choose a hosting provider (Render / Railway / Fly.io, etc.) and check the cost of staging and Redis [A] (Due: )
- [ ] Choose an email delivery service [A] (Due: )

### 2. Dev Environment & CI/CD

**Setup**

- [ ] Create GitHub repo and branch rules (protect main, PRs reviewed by the other person) [A] (Due: )
- [ ] Set up Docker Compose (Flask + PostgreSQL) [A] (Due: )
- [ ] Create Flask skeleton (`create_app`, Blueprints, separate config for dev / test / prod) [A] (Due: )
- [ ] Set up Flask-Migrate [A] (Due: )
- [ ] Add `.env.example` and keep secrets out of Git [A] (Due: )
- [ ] Seed script for sample data in local dev [A] (Due: )
- [ ] README with local setup steps [A+B] (Due: )
- [ ] PR template and pre-commit hooks (ruff, Prettier) [A] (Due: )
- [ ] Build base layout (header, footer, shared CSS) [B] (Due: )

**CI (GitHub Actions)**

- [ ] Run ruff (lint + format check) on every PR [A] (Due: )
- [ ] Run pytest against a PostgreSQL service container (not SQLite) [A] (Due: )
- [ ] Check that migrations apply cleanly (`flask db upgrade`) [A] (Due: )
- [ ] Lint JS/CSS (ESLint / Prettier) [B] (Due: )
- [ ] Enable Dependabot and run pip-audit to catch vulnerable dependencies [A] (Due: )

**CD**

- [ ] Set up a staging environment and deploy to it early [A] (Due: )
- [ ] Auto-deploy: merge to main → CI passes → deploy [A] (Due: )
- [ ] Run DB migrations automatically on deploy [A] (Due: )
- [ ] Health check endpoint (`/healthz`) [A] (Due: )
- [ ] Document rollback steps [A] (Due: )

### 3. Articles & Search (MVP)

- [ ] Article model (title, body, summary, source URL, last verified date, category, tags, publish status) [A] (Due: )
- [ ] Home page (latest news, links to key guides) [B] (Due: )
- [ ] Article list, category, and tag pages [B] (Due: )
- [ ] Article detail page (always shows source link, last verified date, and disclaimer) [B] (Due: )
- [ ] Implement full-text search [A] (Due: )
- [ ] Search UI with visa type and nationality filters [B] (Due: )
- [ ] Mobile layout and accessibility check [B] (Due: )
- [ ] SEO (title/description, sitemap.xml, OGP) [B] (Due: )

### 4. Data Collection & Admin (MVP)

**Admin**

- [ ] Admin login [A] (Due: )
- [ ] Admin: create, edit, publish/unpublish articles [A] (Due: )
- [ ] Review queue (fetched item → draft → approve & publish) [A] (Due: )

**Collectors**

- [ ] Federal Register API collector [A] (Due: )
- [ ] USCIS News / Alerts RSS collector [A] (Due: )
- [ ] U.S. Department of State RSS collector [A] (Due: )
- [ ] Decide how to track Study in the States (scraping or manual check procedure) [A] (Due: )
- [ ] Keyword-based relevance filter [A] (Due: )
- [ ] Duplicate detection (same URL / same document number) [A] (Due: )
- [ ] Scraping etiquette (check robots.txt, contact info in User-Agent, rate limiting) [A] (Due: )
- [ ] (Optional) LLM-generated plain English summary drafts [A] (Due: )

**Scheduling & reliability**

- [ ] Run scheduled jobs in a separate worker/cron process, not inside the web server [A] (Due: )
- [ ] Log each collector run (start, end, items found, errors) in a `collector_runs` table [A] (Due: )
- [ ] Alert admins on fetch failures or page structure changes [A] (Due: )
- [ ] Collector tests using saved responses (fixtures), so CI never calls government sites [A] (Due: )
- [ ] Daily smoke check against the real sources to catch format changes [A] (Due: )

### 5. Content

- [ ] Writing guide (tone, vocabulary level, citing sources, article template) [B] (Due: )
- [ ] Write initial guide articles [B] (Due: )
  - [ ] F-1 basics / maintaining status (Due: )
  - [ ] CPT (Due: )
  - [ ] OPT / STEM OPT (Due: )
  - [ ] Travel & re-entry (Due: )
  - [ ] SEVIS transfer (Due: )
  - [ ] Duration of Status changes (fixed admission period) (Due: )
  - [ ] Grace period / post-graduation options (Due: )
- [ ] Cross-check all articles together before launch [A+B] (Due: )

### 6. Legal & Policies

- [ ] Disclaimer [B] (Due: )
- [ ] Terms of Use [B] (Due: )
- [ ] Privacy Policy [B] (Due: )
- [ ] Ask an expert (immigration attorney, university international office, etc.) to review [A+B] (Due: )
- [ ] Decide whether to use analytics (if so, a privacy-focused one) [A+B] (Due: )

### 7. Launch

- [ ] Set up production (HTTPS, environment variables) [A] (Due: )
- [ ] Automated DB backups + test a restore at least once [A] (Due: )
- [ ] Set up Sentry (backend + frontend JS) [A] (Due: )
- [ ] Uptime monitoring (alert when the site goes down) [A] (Due: )
- [ ] Structured logging (request ID, log levels) [A] (Due: )
- [ ] Security headers and CSP (e.g., Flask-Talisman) [A] (Due: )
- [ ] Secure session cookies (Secure, HttpOnly, SameSite) [A] (Due: )
- [ ] Use Redis as the rate limit storage in production [A] (Due: )
- [ ] (Optional) Cache article pages (Flask-Caching) [A] (Due: )
- [ ] Lighthouse check (performance, accessibility, SEO) [B] (Due: )
- [ ] Pre-launch check (broken links, layout issues, initial articles ready) [B] (Due: )
- [ ] Decide how to announce the launch [A+B] (Due: )

### 8. Notifications

- [ ] Subscriber model (email, categories, nationality, confirmation status, unsubscribe token) [A] (Due: )
- [ ] Double opt-in (confirmation email) [A] (Due: )
- [ ] Unsubscribe link [A] (Due: )
- [ ] Instant alerts for major updates + weekly digest [A] (Due: )
- [ ] Set up SPF, DKIM, and DMARC for the sending domain [A] (Due: )
- [ ] Handle bounces and spam complaints from the email service [A] (Due: )
- [ ] Subscribe form and subscription settings page [B] (Due: )
- [ ] Email templates (HTML / plain text) [B] (Due: )

### 9. Q&A Forum

- [ ] User sign-up and login (nickname, email verification) [A] (Due: )
- [ ] Hash passwords (argon2 or Werkzeug's password hashing) [A] (Due: )
- [ ] Questions, answers, and best answer logic [A] (Due: )
- [ ] Sanitize user posts to prevent XSS (e.g., nh3) [A] (Due: )
- [ ] Report feature, admin delete/hide [A] (Due: )
- [ ] Spam protection (rate limiting, banned words) [A] (Due: )
- [ ] CAPTCHA on sign-up and posting (e.g., Cloudflare Turnstile or hCaptcha) [B] (Due: )
- [ ] Forum UI (list, detail, post form) [B] (Due: )
- [ ] "Official info" badge and links to related articles [B] (Due: )
- [ ] Community guidelines (no personal info, not legal advice) [B] (Due: )
- [ ] Moderation page [B] (Due: )

### 10. Chatbot

- [ ] Choose an LLM API and set a monthly cost limit [A+B] (Due: )
- [ ] Call the LLM API only from the server (never expose the API key to the browser) [A] (Due: )
- [ ] Generate embeddings for approved articles (pgvector) [A] (Due: )
- [ ] RAG: retrieve → generate answer → show sources [A] (Due: )
- [ ] For questions it can't answer, refer users to their DSO or an attorney instead of guessing [A] (Due: )
- [ ] Rate limiting and abuse prevention [A] (Due: )
- [ ] Track LLM usage and cost, and alert when nearing the monthly limit [A] (Due: )
- [ ] Chat UI (JavaScript) and disclaimer [B] (Due: )
- [ ] Build a test question set (~30 questions) and evaluate answer quality [B] (Due: )
- [ ] Decide how to handle chat logs (retention period, masking personal info) [A+B] (Due: )

### 11. Operations (after launch)

- [ ] Set up a rotation for checking the review queue (e.g., by day of the week) [A+B] (Due: )
- [ ] Set up a rotation for forum moderation [A+B] (Due: )
- [ ] Monthly: review "last verified" dates on guide articles [B]
- [ ] Monthly: check collector status and errors [A]
- [ ] Monthly: review Dependabot PRs and update dependencies [A]

---

## Sources

| Source                       | Method                            | URL                                                             | Notes                                             |
| ---------------------------- | --------------------------------- | --------------------------------------------------------------- | ------------------------------------------------- |
| Federal Register             | Official REST API (no key needed) | https://www.federalregister.gov/developers/documentation/api/v1 | Primary source for rules and notices              |
| USCIS News Releases / Alerts | RSS                               | https://www.uscis.gov/newsroom/news-releases                    | Some servers get blocked with 403 — needs testing |
| U.S. Department of State     | RSS                               | https://www.state.gov/rss-feeds                                 | Includes travel.state.gov info                    |
| Study in the States (SEVP)   | Scraping or manual check          | https://studyinthestates.dhs.gov                                | No public API found yet                           |

## Decision Log

| Date       | Decision                       | Reason / Notes                                     |
| ---------- | ------------------------------ | -------------------------------------------------- |
| 2026-09-29 | Site language is English       | To serve international students from all countries |
| 2026-09-29 | Team of 2                      |                                                    |
| 2026-09-29 | Built with Flask + HTML/CSS/JS |                                                    |
|            |                                |                                                    |

## Weekly Log

<!-- Copy this template and add it above the previous week's entry -->

### Week 1 (YYYY-MM-DD)

- **Done last week**:
- **Blockers / questions**:
- **TODOs this week**:
- **Notes**:
