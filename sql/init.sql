CREATE TABLE IF NOT EXISTS public.Users (
    id            bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,

    user_id       varchar(255) NOT NULL,

    refresh_token varchar(255) NOT NULL UNIQUE,
    access_token  varchar(255) NOT NULL UNIQUE,
    scope         text NOT NULL,

    expired_time  int8 NOT NULL,
    expires_in    int8 NOT NULL,
)
