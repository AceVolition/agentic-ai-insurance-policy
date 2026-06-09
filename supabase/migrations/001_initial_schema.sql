create extension if not exists pgcrypto;

create table if not exists public.users (
  id uuid primary key references auth.users(id) on delete cascade,
  email text unique,
  created_at timestamptz not null default now()
);

create table if not exists public.policies (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users(id) on delete cascade,
  file_url text not null,
  insurance_type text,
  uploaded_at timestamptz not null default now()
);

create table if not exists public.analyses (
  id uuid primary key default gen_random_uuid(),
  policy_id uuid not null references public.policies(id) on delete cascade,
  summary text,
  exclusions text,
  risks text,
  denial_explanations text,
  appeal_recommendations text,
  policy_comparison text,
  created_at timestamptz not null default now()
);

create table if not exists public.chats (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users(id) on delete cascade,
  policy_id uuid not null references public.policies(id) on delete cascade,
  message text not null,
  response text not null,
  created_at timestamptz not null default now()
);

create index if not exists policies_user_id_idx on public.policies(user_id);
create index if not exists analyses_policy_id_created_at_idx on public.analyses(policy_id, created_at desc);
create index if not exists chats_policy_id_created_at_idx on public.chats(policy_id, created_at desc);

alter table public.users enable row level security;
alter table public.policies enable row level security;
alter table public.analyses enable row level security;
alter table public.chats enable row level security;

drop policy if exists "Users can read own profile" on public.users;
create policy "Users can read own profile"
on public.users for select
using (auth.uid() = id);

drop policy if exists "Users can update own profile" on public.users;
create policy "Users can update own profile"
on public.users for update
using (auth.uid() = id);

drop policy if exists "Users can read own policies" on public.policies;
create policy "Users can read own policies"
on public.policies for select
using (auth.uid() = user_id);

drop policy if exists "Users can read own analyses" on public.analyses;
create policy "Users can read own analyses"
on public.analyses for select
using (
  exists (
    select 1 from public.policies
    where policies.id = analyses.policy_id
    and policies.user_id = auth.uid()
  )
);

drop policy if exists "Users can read own chats" on public.chats;
create policy "Users can read own chats"
on public.chats for select
using (auth.uid() = user_id);

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.users (id, email)
  values (new.id, new.email)
  on conflict (id) do update set email = excluded.email;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

insert into storage.buckets (id, name, public)
values ('policies', 'policies', false)
on conflict (id) do nothing;

drop policy if exists "Users can access own policy PDFs" on storage.objects;
create policy "Users can access own policy PDFs"
on storage.objects for select
using (
  bucket_id = 'policies'
  and auth.uid()::text = (storage.foldername(name))[1]
);

