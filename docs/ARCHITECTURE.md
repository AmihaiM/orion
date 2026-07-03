# SLE API — Product Foundation

Working name: **Speech Learning Engine (SLE)**.
Brand name can stay EZRA or change later.

## Core idea
The engine teaches spoken language through a four-station journey:

1. Discover — student sees/hears the sentence.
2. Practice — student practices until threshold.
3. Master Challenge — cloze challenge without hints.
4. Final Exam — continuous assessment without feedback.

## Content sources
1. System Curriculum
2. Organization Library
3. Teacher Custom Exercises
4. Content Builder: CSV, Google Sheet, PDF/OCR, image, paste, URL

## Runtime stack
- GitHub: source control
- Render: Flask API runner
- Supabase: PostgreSQL/Auth/permissions/source of truth
- Google Sheets: import/export/reporting only
- Firebase later: push notifications only

## Billing strategy
Billing-ready now, billing-provider later.
Tables exist for plans, subscriptions, usage events.
Stripe / Meshulam / CardCom can be added as connectors.

## Next steps
1. Create Supabase tables with `db/schema.sql`.
2. Add environment variables.
3. Seed system curriculum.
4. Connect current student UI to `/api/curriculum` and `/api/learning`.
