drop table if exists players;
create table players (
  p_id integer primary key autoincrement,
  p_name text not null,
  p_time timestamp not null,
  p_status text,
  p_phase integer
);
