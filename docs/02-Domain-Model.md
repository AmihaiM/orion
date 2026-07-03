# Domain Model v0.1

## Core Entities

- Organization — school, company, institution, or individual account owner.
- User — authenticated person.
- Role — org_admin, teacher, learner, parent_viewer.
- Course — high-level learning path.
- Level — A0/A1/A2/B1/B2 or any future scale.
- Unit — thematic section inside a level.
- Mission — learning goal assigned to learner/class.
- Activity — Discover, Practice, Master Challenge, Final Exam.
- Item — generic learning item. In English MVP, item = sentence.
- Attempt — learner response to an item.
- MasteryResult — calculated mastery outcome.
- NotificationEvent — event to teacher/parent/learner.
- Subscription — billing readiness.

## Key Rule
The engine handles Mission → Activity → Item → Attempt → Mastery.
The subject-specific layer defines what an Item means.
