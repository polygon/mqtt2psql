create table plugs_ids (
    plug_id serial primary key, 
    name text not null unique
);

create table plugs_sensor_data (time timestamp not null
, plug_id integer not null
, total double precision not null
, yesterday double precision not null
, power double precision not null
, apparent_power double precision not null
, reactive_power double precision not null
, factor double precision not null
, voltage double precision not null
, current double precision not null
, foreign key(plug_id) references plugs_ids(plug_id) on delete no action
);

select create_hypertable('plugs_sensor_data', 'time');

create table plugs_status_data (time timestamp not null
, plug_id integer not null
, uptime integer not null
, power boolean not null
, wifi_rssi double precision not null
, wifi_signal double precision not null
, foreign key(plug_id) references plugs_ids(plug_id) on delete no action
);

select create_hypertable('plugs_status_data', 'time');
