create table if not exists shipments (
    id uuid primary key not null,
    recipient text not null,
    address text not null,
    message text,
    due date not null,
    shipped date,
    tags varchar(20)[],
    created timestamp not null,
    updated timestamp,
    deleted timestamp
);

create table if not exists items (
    id uuid primary key not null,
    shipment_id uuid not null,
    data json not null,
    tags varchar(20)[],
    created timestamp not null,
    updated timestamp,
    deleted timestamp
);
