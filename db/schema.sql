-- YouTube AI Shorts Automation - schema
-- Run this once in the Supabase SQL editor (or via psql) against a fresh project.

create extension if not exists pgcrypto;

create table if not exists topics (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  description text,
  style text,
  tone text,
  duration_seconds int default 40,
  active boolean default true,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table if not exists settings (
  id int primary key default 1,
  youtube_channel_id text,
  daily_limit int default 1,
  publish_time text default '19:00',
  timezone text default 'Asia/Kolkata',
  auto_publish boolean default false,
  language text default 'en',
  tone text default 'engaging',
  default_duration_seconds int default 40
);

-- Ensure exactly one settings row exists (id is pinned to 1 by default).
insert into settings (id)
values (1)
on conflict (id) do nothing;

create table if not exists shorts (
  id uuid primary key default gen_random_uuid(),
  topic_id uuid references topics(id),
  title text,
  script text,
  description text,
  hashtags text[],
  status text default 'draft', -- draft | ready | approved | published | failed
  youtube_video_id text,
  failure_reason text,
  scheduled_at timestamptz,
  published_at timestamptz,
  created_at timestamptz default now()
);

create table if not exists youtube_accounts (
  id uuid primary key default gen_random_uuid(),
  channel_id text,
  channel_name text,
  access_token text,
  refresh_token text,
  expires_at timestamptz
);
