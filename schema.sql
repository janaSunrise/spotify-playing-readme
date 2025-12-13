CREATE TABLE IF NOT EXISTS public.users (
    id TEXT PRIMARY KEY,
    access_token TEXT NOT NULL,
    refresh_token TEXT NOT NULL,
    token_type TEXT NOT NULL DEFAULT 'Bearer',
    expires_in INTEGER,
    scope TEXT,
    expired_time BIGINT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_expired_time ON public.users(expired_time);

-- Enable RLS
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow all operations" ON public.users
    FOR ALL
    USING (true)
    WITH CHECK (true);
