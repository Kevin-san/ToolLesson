use alvin;

drop table IF EXISTS `SiteInfo`;

create table IF NOT EXISTS `SiteInfo`(
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`Name` VARCHAR(100),
	`Detail` VARCHAR(100) NOT NULL,
	`User` INT NOT NULL, 
	`Logo` TEXT NOT NULL,
	`TopImage` TEXT NOT NULL, 
	`Powered` VARCHAR(100) NOT NULL, 
	`Links` VARCHAR(100) NOT NULL,
	`ContactEmail` VARCHAR(100) NOT NULL,
	`ContactQQ` VARCHAR(100) NOT NULL,
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0,
	`submission_user` VARCHAR(30),
	`submission_date` DATE,
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;