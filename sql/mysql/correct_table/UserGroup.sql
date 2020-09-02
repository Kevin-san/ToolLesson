use alvin;

drop table IF EXISTS `UserGroup`;

create table IF NOT EXISTS `UserGroup`(
	`NameKey` VARCHAR(128) NOT NULL,
	`Name` VARCHAR(128) NOT NULL,
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0,
	`submission_user` VARCHAR(30),
	`submission_date` DATE,
	PRIMARY KEY ( `NameKey` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;