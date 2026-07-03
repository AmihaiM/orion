# System Architecture v0.1

## Current Stack

- Backend API: Flask on Render
- Database: Supabase PostgreSQL
- Auth/Roles: Supabase Auth + application RBAC
- Frontend: Web first, mobile later
- Google Sheets: Import/Export only
- Firebase: Push notifications later

## Runtime Flow

Learner Web → Flask API → Mission Engine → Supabase

Teacher Web → Flask API → Assignment/Analytics → Supabase

## Sprint 0 Target
One learner completes one mission end-to-end using Supabase as source of truth.
