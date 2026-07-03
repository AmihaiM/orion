-- SLE Product Foundation Schema
-- Run this in Supabase SQL Editor.

create extension if not exists "pgcrypto";

create table if not exists organizations (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  account_type text not null default 'organization', -- organization | individual
  created_at timestamptz not null default now()
);

create table if not exists app_users (
  id uuid primary key default gen_random_uuid(),
  auth_user_id uuid,
  organization_id uuid references organizations(id) on delete cascade,
  email text,
  full_name text not null,
  role text not null check (role in ('org_admin','teacher','student','parent_viewer')),
  created_at timestamptz not null default now()
);

create table if not exists classes (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid references organizations(id) on delete cascade,
  teacher_id uuid references app_users(id),
  name text not null,
  created_at timestamptz not null default now()
);

create table if not exists class_students (
  class_id uuid references classes(id) on delete cascade,
  student_id uuid references app_users(id) on delete cascade,
  primary key (class_id, student_id)
);

create table if not exists parent_students (
  parent_id uuid references app_users(id) on delete cascade,
  student_id uuid references app_users(id) on delete cascade,
  primary key (parent_id, student_id)
);

create table if not exists exercises (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid references organizations(id) on delete cascade,
  created_by_user_id uuid references app_users(id),
  title text not null,
  level text default 'custom',
  unit text,
  source_type text not null default 'system' check (source_type in ('system','organization_library','teacher_custom','content_builder')),
  visibility text not null default 'system' check (visibility in ('system','organization','private')),
  source_url text,
  created_at timestamptz not null default now()
);

create table if not exists sentences (
  id uuid primary key default gen_random_uuid(),
  exercise_id uuid references exercises(id) on delete cascade,
  sentence_order int not null,
  english_text text not null,
  hebrew_text text,
  difficulty text,
  tags text[] default '{}',
  created_at timestamptz not null default now(),
  unique(exercise_id, sentence_order)
);

create table if not exists exercise_assignments (
  id uuid primary key default gen_random_uuid(),
  exercise_id uuid references exercises(id) on delete cascade,
  assigned_by_user_id uuid references app_users(id),
  organization_id uuid references organizations(id) on delete cascade,
  class_id uuid references classes(id),
  student_id uuid references app_users(id),
  due_at timestamptz,
  created_at timestamptz not null default now()
);

create table if not exists learning_sessions (
  id uuid primary key default gen_random_uuid(),
  student_id uuid references app_users(id) on delete cascade,
  exercise_id uuid references exercises(id) on delete cascade,
  assignment_id uuid references exercise_assignments(id),
  started_at timestamptz not null default now(),
  finished_at timestamptz,
  status text not null default 'active'
);

create table if not exists learning_attempts (
  id uuid primary key default gen_random_uuid(),
  student_id uuid references app_users(id) on delete cascade,
  exercise_id uuid references exercises(id) on delete cascade,
  sentence_id uuid references sentences(id) on delete cascade,
  session_id uuid references learning_sessions(id),
  stage text not null check (stage in ('discover','practice','master_challenge','final_exam')),
  spoken_text text,
  accuracy_score int,
  passed boolean,
  recording_duration_ms int default 0,
  silence_ms int default 0,
  words_per_minute int default 0,
  fluency_status text,
  created_at timestamptz not null default now()
);

create table if not exists sentence_results (
  id uuid primary key default gen_random_uuid(),
  student_id uuid references app_users(id) on delete cascade,
  exercise_id uuid references exercises(id) on delete cascade,
  sentence_id uuid references sentences(id) on delete cascade,
  session_id uuid references learning_sessions(id),
  practice_attempts int default 0,
  cloze_attempts int default 0,
  mastery_attempts int default 0,
  total_attempts int default 0,
  best_accuracy_score int,
  exam_score int,
  mastery_status text,
  fluency_status text,
  mastered boolean default false,
  started_at timestamptz default now(),
  finished_at timestamptz
);

create table if not exists coach_profiles (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  style text not null default 'encouraging',
  voice_gender text,
  accent text,
  is_system boolean default true,
  created_at timestamptz not null default now()
);

create table if not exists notification_events (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid references organizations(id) on delete cascade,
  recipient_user_id uuid references app_users(id) on delete cascade,
  event_type text not null,
  title text not null,
  body text not null,
  delivery_status text not null default 'pending',
  created_at timestamptz not null default now()
);

create table if not exists billing_plans (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  audience text not null check (audience in ('b2b','b2c')),
  monthly_price numeric,
  active_student_limit int,
  created_at timestamptz not null default now()
);

create table if not exists subscriptions (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid references organizations(id) on delete cascade,
  user_id uuid references app_users(id) on delete cascade,
  plan_id uuid references billing_plans(id),
  status text not null default 'trial',
  provider text,
  provider_subscription_id text,
  started_at timestamptz default now(),
  ends_at timestamptz
);

create table if not exists usage_events (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid references organizations(id) on delete cascade,
  user_id uuid references app_users(id),
  event_type text not null,
  quantity int default 1,
  metadata jsonb default '{}',
  created_at timestamptz not null default now()
);

alter table organizations enable row level security;
alter table app_users enable row level security;
alter table classes enable row level security;
alter table class_students enable row level security;
alter table parent_students enable row level security;
alter table exercises enable row level security;
alter table sentences enable row level security;
alter table exercise_assignments enable row level security;
alter table learning_sessions enable row level security;
alter table learning_attempts enable row level security;
alter table sentence_results enable row level security;

-- Sprint 0 note:
-- The Flask API uses SUPABASE_SERVICE_ROLE_KEY server-side.
-- User-facing RLS policies will be tightened when Supabase Auth is connected.
