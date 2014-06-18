create table permissions(
       id serial,
       action character varying(10),
       target character varying(45),
       constraint perm_pk primary key(id)
);

create table groups(
       id serial,
       name character varying(45),
       constraint grp_pk primary key(id)
);


create table group_perm(
       id serial,
       group_id integer not null,
       permission_id integer not null,
       constraint gp_pk primary key(id),	
       constraint gp_fk_grp foreign key(group_id)
       references groups(id) on delete cascade on update cascade,
       constraint gp_fk_perm foreign key(permission_id)
       references permissions(id) on delete cascade on update cascade
);

create table user_group(
       id serial,
       user_id integer not null,
       group_id integer not null,
       constraint ug_pk primary key(id),	
       constraint ug_fk_user foreign key(user_id)
       references auth_user(id) on delete cascade on update cascade,
       constraint ug_fk_grp foreign key(group_id)
       references groups(id) on delete cascade on update cascade
);



--group inserts
insert into permissions(action, target) VALUES
('add', 'agency'), --1
('edit', 'agency'), --2
('delete', 'agency'), --3
('view', 'agency information'), --4
('view', 'agency submitted documents'), --5
('add', 'agency submitted documents'), --6
('delete', 'agency submitted documents'),--7
('add', 'agency approved budget'), --8
('edit', 'agency approved budget'), --9
('delete', 'agency approved budget'), --10
('view', 'agency approved budget'), --11
('add', 'fund request'), --12
('edit', 'fund request'), --13
('delete', 'fund request'), --14
('view', 'running balances'), --15
('print', 'running balances'), --16
('view', 'status of allotment releases'), --17
('print', 'status of allotment releases'), --18
('view', 'total releases'), --19
('print', 'total releases'), --20
('view', 'monthly reports'), --21
('print', 'monthly reports'), --22
('view', 'quarterly report'), --23
('print', 'quarterly report'), --24
('view', 'transaction history'), --25
('delete', 'transaction history'), --26
('view', 'analysis report'), --27
('print', 'analysis report'), --28
('print', 'fund utilization'), --29
('view', 'fund utilization'), --30
('add', 'user'), --31
('edit', 'user'), --32
('view', 'user'); --33



insert into groups(name) VALUES
('Recording Officer'),
('BEAM'),
('BPAC'),
('Internal User'),
('Executive Director');


insert into group_perm(group_id, permission_id) VALUES
--recording officer
(1, 4),
(1, 5),
(1, 6),
(1, 11),
(1, 7),
(1, 15),
(1, 16),
(1, 17),
(1, 18),
(1, 19),
(1, 20),
(1, 21),
(1, 22),
(1, 23),
(1, 24),
(1, 27),
(1, 28),
--BEAM
(2, 4),
(2, 5),
(2, 8),
(2, 9),
(2, 10),
(2, 11),
(2, 12),
(1, 13),
(1, 14),
(1, 15),
(1, 16),
(1, 17),
(1, 18),
(1, 19),
(1, 20),
(1, 21),
(1, 22),
(1, 23),
(1, 24),
(1, 27),
(1, 28),
--BPAC
(3, 4),
(3, 5),
(3, 11),
(3, 27),
(3, 28),
(3, 29),
(3, 30),
--internal users
(4, 4),
(4, 5),
(4, 11),
(4, 15),
(4, 16),
(4, 17),
(4, 18),
(4, 19),
(4, 20),
(4, 21),
(4, 22),
(4, 23),
(4, 24),
(4, 29),
(4, 30),
--executive director
(5, 1),
(5, 2),
(5, 3),
(5, 4),
(5, 5),
(5, 6),
(5, 7),
(5, 8),
(5, 9),
(5, 10),
(5, 11),
(5, 12),
(5, 13),
(5, 14),
(5, 15),
(5, 16),
(5, 17),
(5, 18),
(5, 19),
(5, 20),
(5, 21),
(5, 22),
(5, 23),
(5, 24),
(5, 25),
(5, 26),
(5, 27),
(5, 28),
(5, 29),
(5, 30),
(5, 31),
(5, 32),
(5, 33);




