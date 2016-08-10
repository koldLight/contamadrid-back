create table station (
  id serial primary key,
  external_id varchar(10) not null,
  name varchar(100) not null,
  address varchar(100) not null,
  altitude integer not null,
  type varchar(10) not null,
  longitude numeric,
  latitude numeric
);
create unique index idx_station_extid on station(external_id);

create table variable (
  id serial primary key,
  external_id integer not null,
  name varchar(100) not null,
  formula varchar(10) not null,
  units varchar(10) not null
);
create unique index idx_variable_extid on variable(external_id);

create table measure (
  id serial primary key,
  station_id integer not null,
  variable_id integer not null,
  technique integer not null,
  periodicity integer not null,
  date date not null,
  hour integer not null,
  value numeric not null,
  valid boolean not null
);
create unique index idx_measure on measure(station_id, variable_id, date, hour);
create index idx_measure_var_date on measure(variable_id, date);

create table warning_forecast (
  id serial primary key,
  date date not null,
  prewarning boolean not null,
  warning boolean not null
);
create unique index idx_warning_forecast on warning_forecast(date);
