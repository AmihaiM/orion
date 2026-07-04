# ORION Blueprint v0.1-alpha

Status: Working Draft  
Owner: Product / Architecture  
Repository: `AmihaiM/orion`  
Current milestone: Sprint 1 — Mission API  

---

## 0. Executive Summary

ORION is a Mastery Engine first validated through spoken English.

The product is not only an English app. The first commercial use case is English speaking practice, but the architecture is designed so the same engine can later support other domains: foreign languages, public speaking, mathematics, science, music, physical training, and professional skills.

The key product promise is:

> Build the engine once. Change only the content.

The first MVP objective is simple and measurable:

> A learner completes one Mission from start to finish using the new architecture.

This means the learner can load a Mission from Supabase, see its sentences, practice, submit attempts, receive scoring and mastery feedback, and complete the Mission with results stored in the database.

The old demo proved the idea. ORION turns it into a scalable platform.

---

## 1. Product Vision

ORION provides every learner with a personal digital coach that helps them move from exposure to measurable mastery.

The platform complements teachers. It does not replace them.

For schools and ministries, ORION adds daily personal mastery practice without forcing schools to replace teachers, rewrite curricula, or redesign classroom models.

For learners, ORION offers structured practice, feedback, repetition, fluency tracking, and confidence building.

For parents and teachers, ORION provides visibility into what the learner practiced, where they struggled, and where they achieved mastery.

The first validated domain is spoken English, but the core model is subject-agnostic.

---

## 2. Guiding Principles

### 2.1 Learner First
Every product decision must improve the learner’s ability to practice, recover from mistakes, and build confidence.

### 2.2 Coach, Not Judge
The system should not behave like a harsh examiner. It should behave like a coach: clear, honest, encouraging, and specific.

### 2.3 Platform, Not Project
Every component should be designed as part of a reusable platform, not a one-off demo.

### 2.4 Content Is an Asset
Curriculum and Missions are strategic assets. They should not live only inside CSV files or hardcoded demos.

### 2.5 Engine Never Knows the Subject
The Mastery Engine must not depend on English-specific assumptions. English is the first implementation, not the limit of the platform.

### 2.6 Learning Policy vs Learning Engine
The engine provides capabilities: Discover, Practice, Master Challenge, Final Exam, Attempt, Score, Mastery.

The policy decides which path applies: Learning Mode, Assessment Mode, Resume Mode, Free Practice.

### 2.7 Security by Design
Authentication, roles, row-level security, secrets, auditability, and tenant isolation must be treated as foundation work, not future patches.

### 2.8 No Zero Progress Day
Every work cycle should produce a tangible deliverable: code, schema, API, documentation, tests, or a working feature.

---

## 3. Product Language

ORION uses a product vocabulary that should remain consistent across code, documentation, UI, and business communication.

| Term | Meaning |
|---|---|
| Organization | A school, institution, company, or B2B account |
| Learner | The person practicing and being assessed |
| Teacher | A user who assigns and monitors Missions |
| Parent Viewer | A parent or guardian with read-only progress visibility |
| Course | A broad learning path, such as Spoken English A0-A2 |
| Unit | A curriculum section within a course |
| Mission | A concrete learning goal assigned to a learner |
| Activity | A learning action inside a Mission |
| Sentence | The smallest spoken-English content item in the first domain |
| Attempt | A learner’s submitted performance on an item |
| Mastery | Evidence that the learner can perform with accuracy and fluency |
| Coach | The feedback/persona layer that guides the learner |

Current database terms may still use `exercises` and `sentences`. Product-facing language should prefer `Mission` and `Sentence`.

---

## 4. Domain Model

### 4.1 Core hierarchy

```text
Organization
  └── Users
       ├── Org Admin
       ├── Teacher
       ├── Learner
       └── Parent Viewer

Course
  └── Unit
       └── Mission
            └── Sentence
                 └── Attempt
                      └── Result / Mastery
```

### 4.2 Current Supabase schema mapping

| Product concept | Current table |
|---|---|
| Organization | `organizations` |
| User | `app_users` |
| Class | `classes` |
| Mission | `exercises` |
| Sentence | `sentences` |
| Assignment | `exercise_assignments` |
| Mission Session | `learning_sessions` |
| Attempt | `learning_attempts` |
| Sentence Result | `sentence_results` |
| Coach Profile | `coach_profiles` |
| Notification | `notification_events` |
| Billing Plan | `billing_plans` |
| Subscription | `subscriptions` |
| Usage Event | `usage_events` |

### 4.3 Important rule

The code may gradually rename API concepts to Mission while keeping existing table names until we migrate the schema cleanly.

Do not introduce another table named `profiles`. The product user table is `app_users`.

---

## 5. Learning Modes

ORION should not force one learning path in every context.

### 5.1 Learning Mode
Default pedagogical flow:

```text
Discover → Practice → Master Challenge → Final Exam → Complete
```

Used when the goal is acquisition and mastery.

### 5.2 Assessment Mode
Direct exam mode.

Used when:
- A learner wants to improve a score.
- A teacher assigns a quiz.
- A learner already knows the content.

### 5.3 Resume Mode
Restores the learner to the correct Mission, sentence, and stage after interruption.

Used when:
- Battery died.
- Browser closed.
- Network failed.

### 5.4 Free Practice Mode
Practice without formal scoring or progression pressure.

Used for confidence building and extra practice.

---

## 6. Learning Flow for Spoken English MVP

### 6.1 Discover
The learner sees the Hebrew meaning and English sentence, and hears the target sentence.

Purpose: initial exposure and comprehension.

### 6.2 Practice
The learner repeats the sentence, receives feedback, and retries until the practice threshold is met or attempts are exhausted.

Purpose: guided repetition and correction.

### 6.3 Master Challenge
The learner performs a more demanding challenge, such as Cloze, with reduced support.

Purpose: verify active retrieval and partial independence.

### 6.4 Final Exam
The learner completes the Mission without feedback between items.

Purpose: assessment of retained performance and exam score.

---

## 7. Speech, Scoring, and Mastery

### 7.1 Current demo
The demo uses browser speech recognition and simple text comparison.

### 7.2 Product direction
The production engine should use a Speech Provider Interface.

Possible providers:
- Browser Web Speech API for demo and lightweight prototype
- OpenAI Whisper for higher accuracy and timestamps
- Google Speech-to-Text
- Azure Speech
- AWS Transcribe

### 7.3 Accuracy is not Mastery
Accuracy measures textual match.

Mastery should include:
- Accuracy score
- Fluency score
- Attempt count
- Pause duration
- Words per minute
- Time to first speech
- Consistency across retries

### 7.4 Initial Mastery formula
A first approximation:

```text
Mastery Score =
  40% Accuracy
+ 25% Fluency
+ 15% Retry Efficiency
+ 10% Pause Control
+ 10% Completion Stability
```

Weights are provisional and must be validated through usage data.

---

## 8. System Architecture

### 8.1 Current stack

```text
GitHub → Flask API → Supabase PostgreSQL
```

### 8.2 Planned platform structure

```text
Learner Web / Teacher Web / Parent Web
        ↓
Flask REST API
        ↓
Domain Services
        ├── Mission Engine
        ├── Learning State Engine
        ├── Mastery Engine
        ├── Speech Engine
        ├── Curriculum Engine
        ├── Coach Engine
        ├── Notification Engine
        └── Billing Skeleton
        ↓
Supabase PostgreSQL + Auth + Storage
```

### 8.3 Google Sheets role
Google Sheets is not the system database.

Allowed roles:
- Import content
- Export reports
- Temporary admin workflow

Not allowed as long-term source of truth for live learning sessions.

### 8.4 Firebase role
Firebase is not the primary database.

Possible future role:
- Mobile push notifications through Firebase Cloud Messaging.

---

## 9. Security and Scale Readiness

### 9.1 Current development posture
The local backend currently uses Supabase service role in `.env` for server-side access.

This key must never be committed and must never be exposed to browsers.

### 9.2 Production direction
- Use server-side secrets only in Render/AWS secret management.
- Use RLS for user-facing access.
- Use service role only in backend/admin jobs.
- Use audit logs for sensitive events.
- Ensure organization-level tenant isolation.

### 9.3 Future migration path
Current stack can support MVP and pilots.

If usage grows, migration path:

```text
Render → AWS ECS / App Runner / Kubernetes
Supabase managed Postgres → dedicated Postgres / RDS if required
Basic logs → structured observability
Manual deploy → CI/CD pipeline
```

---

## 10. Repository Strategy

Current repository: `AmihaiM/orion`

Target structure:

```text
orion/
  backend/
  database/
  docs/
  frontend/
  seed/
  curriculum/
  README.md
  .gitignore
```

Rules:
- Backend code lives only in `backend/`.
- No duplicate root-level backend files.
- No `.env` files committed.
- No `.venv` committed.
- Every sprint must produce runnable code or approved documentation.

---

## 11. Sprint 0 Status

Completed:
- GitHub repository created.
- Local Flask API runs.
- Supabase connected.
- `/health` returns API and Supabase status.
- Repository cleanup completed.
- First Mission stored in Supabase.
- `/missions` returns real Mission data.
- `/missions/{id}` returns Mission with sentences.

---

## 12. Sprint 1 Goal

User Story:

> As a learner, I can load one Mission from Supabase and begin a learning session.

Required capabilities:
- `GET /missions`
- `GET /missions/{id}`
- `POST /learning-sessions`
- `GET /learning-sessions/{id}`
- `POST /attempts`
- Basic Mastery Engine v1

Definition of Done:
- A Mission can be loaded from Supabase.
- A learner session can be created.
- At least one attempt can be saved.
- The API returns attempt score and pass/fail status.
- Data is persisted in Supabase.

---

## 13. Innovation Backlog

Future ideas not included in Sprint 1:
- AI Coach avatar/persona
- OCR/PDF/URL/Paste Mission Builder
- Parent weekly report
- Push notifications
- B2B billing
- B2C subscription
- Adaptive learning path
- Teacher marketplace
- Curriculum marketplace
- Mobile app
- Offline mode
- AI generated Missions
- AI lesson planner

---

## 14. Immediate Next Engineering Steps

1. Merge `sprint1-missions-api` after review.
2. Create `feature/learning-sessions`.
3. Implement `POST /learning-sessions`.
4. Implement `POST /attempts`.
5. Introduce `services/mastery_engine.py` as the scoring entry point.
6. Add minimal QA checklist.

---

## 15. Open Questions

1. Should table names be migrated from `exercises` to `missions`, or should we keep database names stable and expose Mission terminology only in API/UI?
2. When should Supabase Auth be introduced into the new API flow?
3. Do we keep Flask for MVP or switch to FastAPI before the codebase grows?
4. Which Speech Provider should be the production default?
5. How strict should RLS be before first pilot?

