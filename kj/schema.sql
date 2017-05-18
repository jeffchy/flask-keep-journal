drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null
);

drop table if exists experience;
create table experience (
  id integer primary key autoincrement,
  title text not null unique,
  cate text,
  discription text,
  eventdate text not null,
  eventrank real not null

);

drop table if exists content;
create table content (
  id integer primary key autoincrement,
  title text not null unique,
  cate text,
  discription text,
  eventdate text not null,
  eventrank real not null

);
drop table if exists skill;
create table skill (
  id integer primary key autoincrement,
  title text not null unique,
  cate text,
  discription text,
  eventdate text not null,
  eventrank real not null

);
drop table if exists curricular;
create table curricular (
  id integer primary key autoincrement,
  title text not null unique,
  cate text,

  discription text,
  eventdate text not null,
  eventrank real not null

);
drop table if exists project;
create table project (
  id integer primary key autoincrement,
  title text not null unique,
  cate text,
  discription text,
  eventdate text not null,
  eventrank real not null

);
drop table if exists award;
create table award (
  id integer primary key autoincrement,
  title text not null unique,
  cate text,
  discription text,
  eventdate text not null,
  eventrank real not null

);
