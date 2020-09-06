use alvin;

drop table IF EXISTS `django_session`;

create table IF NOT EXISTS `django_session`(
	`session_key` VARCHAR(40) NOT NULL,
	`session_data` LONGTEXT NOT NULL,
	`expire_date` DATETIME,
	PRIMARY KEY ( `session_key` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
