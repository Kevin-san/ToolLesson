use alvin;

drop table IF EXISTS `User`;

create table IF NOT EXISTS `User`(
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`Name` VARCHAR(128) UNIQUE NOT NULL,
	`Password` VARCHAR(256) NOT NULL,
	`Email` VARCHAR(256) NOT NULL, 
	`Sex` CHAR(1) NOT NULL,
	`Permissions` VARCHAR(24) NOT NULL,
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0,
	`submission_user` VARCHAR(30),
	`submission_date` DATE,
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
用户：可以 进 不同的 菜单(Group)(菜单也有 操作限制，比如lesson 只有 read/write 权限，没有import/export) ,对 各个菜单有 不同的 权限 (Role) ,每个权限对应 多个 url (Function) ,最终登记在用户表里
example -> 张三 可以进 lessons/blogs/video/music , 每个 菜单 都有 lesson->read, blogs->write, video -> import , music -> export
admin 可以删除用户即进入用户管理界面
read - 1
write -2 
import -4
export -8
admin - 0

lessons - b
blogs - c
tools - d(all)
music - e
video - f
novel - g
hiders - h

https://www.cnblogs.com/cou1d/p/12079159.html