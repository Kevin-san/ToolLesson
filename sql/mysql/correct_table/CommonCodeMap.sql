use alvin;

drop table IF EXISTS `CommonCodeMap`;

create table IF NOT EXISTS `CommonCodeMap`(
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`CodeType` VARCHAR(100) NOT NULL,
	`TypeKey` VARCHAR(100) NOT NULL,
	`TypeVal` VARCHAR(100) NOT NULL,
	`Description1` VARCHAR(100)NULL,
	`Description2` VARCHAR(1000)NULL,
	`DescriptionText` VARCHAR(1000)NULL,
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0,
	`submission_user` VARCHAR(30) NOT NULL DEFAULT 'alvin',
	`submission_date` DATE NOT NULL DEFAULT curdate(),
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into CommonCodeMap(CodeType,TypeKey,TypeVal) values('LinkDirectory','/audio/','I:/音频/');
insert into CommonCodeMap(CodeType,TypeKey,TypeVal) values('LinkDirectory','/img/','I:/图片/');
insert into CommonCodeMap(CodeType,TypeKey,TypeVal) values('LinkDirectory','/video/','I:/视频/');
insert into CommonCodeMap(CodeType,TypeKey,TypeVal) values('LinkDirectory','/novel/','I:/小说/');
insert into CommonCodeMap(CodeType,TypeKey,TypeVal) values('LinkDirectory','/learn/','I:/学习/');
insert into CommonCodeMap(CodeType,TypeKey,TypeVal) values('LinkDirectory','/blog/','I:/博客/');