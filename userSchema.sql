drop table if exists players;
create table players (
  p_id integer primary key autoincrement,
  p_name text not null,
  p_time timestamp not null, -- used to record the font_of_life 'last use' date
  p_status text,
  p_is_alive integer,
  p_birth_time timestamp not null,
  p_death_time timestamp not null,
  p_oracle_state integer,
  p_trap_state integer,
  p_inventory integer
);
