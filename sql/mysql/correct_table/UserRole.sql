use alvin;

drop table `UserRole`;

create table IF NOT EXISTS `UserRole`(
	`Id` INT NOT NULL,
	`Name` VARCHAR(128) NOT NULL,
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0,
	`submission_user` VARCHAR(30),
	`submission_date` DATE,
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;