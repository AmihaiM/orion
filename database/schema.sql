-- SLE Platform schema v0.1

create extension if not exists pgcrypto;

create table if not exists organizations (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  account_type text not null default 'organization' check (account_type in ('organization','individual')),
  created_at timestamptz not null default now()
);

create table if not exists app_users (
  id uuid primary key default gen_random_uuid(),
  auth_user_id uuid unique,
  organization_id uuid references organizations(id) on delete cascade,
  full_name text not null,
  email text,
  created_at timestamptz not null default now()
);

create table if not exists user_roles (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references app_users(id) on delete cascade,
  role text not null check (role in ('org_admin','teacher','learner','parent_viewer')),
  created_at timestamptz not null default now(),
  unique(user_id, role)
);

create table if not exists courses (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid references organizations(id) on delete cascade,
  title text not null,
  domain text not null default 'spoken_english',
  visibility text not null default 'organization' check (visibility in ('system','organization','private')),
  created_at timestamptz not null default now()
);

create table if not exists missions (
  id uuid primary key default gen_random_uuid(),
  course_id uuid references courses(id) on delete cascade,
  title text not null,
  level_code text,
  status text not null default 'draft' check (status in ('draft','active','archived')),
  source_type text default 'manual' check (source_type in ('system','manual','csv','google_sheet','ocr','pdf','url','paste')),
  created_at timestamptz not null default now()
);

create table if not exists mission_items (
  id uuid primary key default gen_random_uuid(),
  mission_id uuid references missions(id) on delete cascade,
  item_order int not null,
  item_type text not null default 'sentence',
  prompt_text text not null,
  target_text text not null,
  translation_text text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  unique(mission_id, item_order)
);

create table if not exists learner_mission_sessions (
  id uuid primary key default gen_random_uuid(),
  learner_user_id uuid references app_users(id) on delete cascade,
  mission_id uuid references missions(id) on delete cascade,
  mode text not null default 'learning' check (mode in ('learning','assessment','resume','free_practice')),
  current_state text not null default 'discover',
  started_at timestamptz not null default now(),
  completed_at timestamptz,
  status text not null default 'active' check (status in ('active','completed','abandoned'))
);

create table if not exists attempts (
  id uuid primary key default gen_random_uuid(),
  session_id uuid references learner_mission_sessions(id) on delete cascade,
  item_id uuid references mission_items(id) on delete cascade,
  activity_type text not null check (activity_type in ('discover','practice','master_challenge','final_exam')),
  attempt_number int not null default 1,
  expected_text text not null,
  recognized_text text,
  accuracy_score numeric(5,2),
  fluency_score numeric(5,2),
  pause_score numeric(5,2),
  mastery_score numeric(5,2),
  mastered boolean default false,
  recording_duration_ms int,
  pause_duration_ms int,
  words_per_minute numeric(6,2),
  created_at timestamptz not null default now()
);

create table if not exists subscriptions (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid references organizations(id) on delete cascade,
  plan_code text not null default 'free',
  status text not null default 'trial',
  created_at timestamptz not null default now()
);

create table if not exists notification_events (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid references organizations(id) on delete cascade,
  recipient_user_id uuid references app_users(id) on delete cascade,
  event_type text not null,
  payload jsonb not null default '{}'::jsonb,
  status text not null default 'pending',
  created_at timestamptz not null default now()
);
