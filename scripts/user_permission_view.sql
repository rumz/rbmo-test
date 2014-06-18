CREATE VIEW user_permissions AS
SELECT auth_user.id, auth_user.username,
	groups.name, permissions.action, permissions.target
FROM auth_user
       INNER JOIN user_group ON
       user_group.user_id=auth_user.id
       INNER JOIN groups ON 
       groups.id = user_group.group_id
       INNER JOIN group_perm ON
       group_perm.group_id=groups.id
       INNER JOIN permissions ON 
       permissions.id=group_perm.permission_id
