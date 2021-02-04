create table if not exists shipments (
    id uuid primary key not null,
    recipient text not null,
    address text not null,
    message text,
    due date not null,
    shipped date,
    tags varchar(20)[],
    meta json
);

alter table shipments add constraint meta_is_valid check (
    validate_json_schema($$
    {
        "type": "object",
        "properties": {
            "created": {"type": "string"},
            "updated": {"type": "string"},
            "deleted": {"type": "string"},
        }
    }
    $$, meta)
);


create table if not exists items {
    id uuid primary key not null,
    data json,
    tags varchar(20)[],
    meta json
);

alter table items add constraint meta_is_valid check (
    validate_json_schema($$
    {
        "type": "object",
        "properties": {
            "created": {"type": "string"},
            "updated": {"type": "string"},
            "deleted": {"type": "string"},
        }
    }
    $$, meta)
);
