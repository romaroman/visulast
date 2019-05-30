create table users
(
    id              serial not null
        constraint users_pk
            primary key,
    lastfm_username varchar(255),
    lastfm_token    varchar(255),
    telegram_id     integer,
    start_timestamp timestamp
);

alter table users
    owner to postgres;

create table artists_scrapped
(
    id          serial not null
        constraint artists_scrapped_pk
            primary key,
    mbid        varchar(255),
    name        varchar(255),
    country     varchar(255),
    info_source varchar(255)
);

alter table artists_scrapped
    owner to postgres;

create table results
(
    id        serial  not null,
    user_id   integer not null
        constraint results_users_id_fk
            references users,
    img_path  text,
    obj_path  text,
    timestamp timestamp,
    request   text
);

alter table results
    owner to postgres;

create table logs
(
    id        serial    not null
        constraint logs_pk
            primary key,
    timestamp timestamp not null,
    message   text      not null,
    level     integer   not null
);

alter table logs
    owner to postgres;

