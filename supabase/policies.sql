-- Políticas RLS e configurações base para n.Gabi (Supabase)
-- Execute no SQL Editor do Supabase, ajustando nomes de esquemas/tabelas conforme necessário

-- 1) Agents
alter table public.agents enable row level security;

create policy agents_select_tenant on public.agents
for select using (
  (jwt() ->> 'role') = 'service_role'
  or (tenant_id = (jwt() ->> 'tenant_id'))
);

create policy agents_mutate_tenant on public.agents
for all using (
  (jwt() ->> 'role') = 'service_role'
  or (tenant_id = (jwt() ->> 'tenant_id'))
) with check (
  (jwt() ->> 'role') = 'service_role'
  or (tenant_id = (jwt() ->> 'tenant_id'))
);

-- 2) Chat History
alter table public.chat_history enable row level security;

create policy chat_history_select on public.chat_history
for select using (
  (jwt() ->> 'role') = 'service_role'
  or (
    tenant_id = (jwt() ->> 'tenant_id')
    and user_id = auth.uid()
  )
);

create policy chat_history_mutate on public.chat_history
for all using (
  (jwt() ->> 'role') = 'service_role'
  or (
    tenant_id = (jwt() ->> 'tenant_id')
    and user_id = auth.uid()
  )
) with check (
  (jwt() ->> 'role') = 'service_role'
  or (
    tenant_id = (jwt() ->> 'tenant_id')
    and user_id = auth.uid()
  )
);

-- 3) Vector Embeddings (pgvector)
alter table public.vector_embeddings enable row level security;

create policy vector_select on public.vector_embeddings
for select using (
  (jwt() ->> 'role') = 'service_role'
  or (tenant_id = (jwt() ->> 'tenant_id'))
);

create policy vector_mutate on public.vector_embeddings
for all using (
  (jwt() ->> 'role') = 'service_role'
  or (tenant_id = (jwt() ->> 'tenant_id'))
) with check (
  (jwt() ->> 'role') = 'service_role'
  or (tenant_id = (jwt() ->> 'tenant_id'))
);

-- 4) Voice Style Base
alter table public.voice_style_base enable row level security;

create policy voice_style_select on public.voice_style_base
for select using (
  (jwt() ->> 'role') = 'service_role'
  or (tenant_id = (jwt() ->> 'tenant_id'))
);

create policy voice_style_mutate on public.voice_style_base
for all using (
  (jwt() ->> 'role') = 'service_role'
  or (tenant_id = (jwt() ->> 'tenant_id'))
) with check (
  (jwt() ->> 'role') = 'service_role'
  or (tenant_id = (jwt() ->> 'tenant_id'))
);

-- 5) Users Profiles (escopo por user_id)
alter table public.users_profiles enable row level security;

create policy users_profiles_select on public.users_profiles
for select using (
  (jwt() ->> 'role') = 'service_role'
  or (user_id = auth.uid())
);

create policy users_profiles_mutate on public.users_profiles
for all using (
  (jwt() ->> 'role') = 'service_role'
  or (user_id = auth.uid())
) with check (
  (jwt() ->> 'role') = 'service_role'
  or (user_id = auth.uid())
);

-- 6) Realtime: publicar tabelas
-- select supabase_realtime.add_table('public', 'chat_history');
-- select supabase_realtime.add_table('public', 'agents');

-- 7) Índices recomendados
create index if not exists idx_agents_tenant on public.agents(tenant_id);
create index if not exists idx_history_user_tenant on public.chat_history(user_id, tenant_id);
create index if not exists idx_vector_tenant on public.vector_embeddings(tenant_id);

-- 8) Storage policies (exemplo de buckets)
-- Nota: criar buckets no dashboard e aplicar políticas equivalentes
-- Exemplo conceitual (ajustar para storage policies via UI/SQL APIs)
-- Public: leitura pública, escrita restrita ao tenant
-- Private: leitura/escrita somente do owner/tenant 