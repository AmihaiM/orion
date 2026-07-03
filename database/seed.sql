insert into organizations (id, name, account_type)
values ('00000000-0000-0000-0000-000000000001', 'SLE Demo Org', 'organization')
on conflict do nothing;

insert into courses (id, organization_id, title, domain, visibility)
values ('00000000-0000-0000-0000-000000000101', '00000000-0000-0000-0000-000000000001', 'Spoken English Foundation', 'spoken_english', 'system')
on conflict do nothing;

insert into missions (id, course_id, title, level_code, status, source_type)
values ('00000000-0000-0000-0000-000000000201', '00000000-0000-0000-0000-000000000101', 'Demo Mission: Basic Confidence', 'A0', 'active', 'system')
on conflict do nothing;

insert into mission_items (mission_id, item_order, item_type, prompt_text, target_text, translation_text)
values
('00000000-0000-0000-0000-000000000201', 1, 'sentence', 'אני אוהב ללמוד אנגלית', 'I love learning English', 'אני אוהב ללמוד אנגלית'),
('00000000-0000-0000-0000-000000000201', 2, 'sentence', 'אני רוצה לדבר בביטחון', 'I want to speak with confidence', 'אני רוצה לדבר בביטחון'),
('00000000-0000-0000-0000-000000000201', 3, 'sentence', 'אני מתרגל כל יום', 'I practice every day', 'אני מתרגל כל יום')
on conflict do nothing;
