use alvin;

drop table `ImageContent`;

create table IF NOT EXISTS `ImageContent`(
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`Directory` VARCHAR(100),
	`ImageName` VARCHAR(100) NOT NULL,
	`Width` INT NOT NULL, 
	`Height` INT NOT NULL, 
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0,
	`submission_user` VARCHAR(30),
	`submission_date` DATE,
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;