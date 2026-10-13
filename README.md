# International Student Information setup

The AI summary reads text already saved in the database. It does not scrape USCIS again. Each click sends one Gemini request; summaries are not saved in the database in this version.

## Start or update the app

1. In the project folder, copy `.env.example` to `.env` if `.env` does not exist. Keep your existing `.env` if it already has your database password.
2. Set `POSTGRES_PASSWORD` and `GEMINI_API_KEY` in `.env`. Keep the API key private. `GEMINI_MODEL=gemini-3.5-flash-lite` is the default. `CHECK_TIMEZONE=America/Chicago` means the daily check happens at midnight Chicago time.
3. Run `docker compose up -d --build`.
4. Open <http://127.0.0.1:5000>, enter a USCIS URL, and click **Get Information**.
5. Click **Create AI summary**. The summary or a specific error appears below the button. A failed summary does not remove the saved page.

# Do not run `docker compose down -v` on the server because `-v` removes the PostgreSQL data volume.
