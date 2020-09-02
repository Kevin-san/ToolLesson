use alvin;

drop table IF EXISTS `UserFunction`;

create table IF NOT EXISTS `UserFunction`(
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`GroupKey` VARCHAR(30) NOT NULL,
	`RoleId` INT NOT NULL,
	`FunctionStr` VARCHAR(256) NOT NULL,
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0,
	`submission_user` VARCHAR(30),
	`submission_date` DATE,
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;