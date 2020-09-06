use alvin;

drop table IF EXISTS `UserConfirmString`;

create table IF NOT EXISTS `UserConfirmString`(
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`code` VARCHAR(256) NOT NULL,
	`User_Id` INT NOT NULL,
	`c_time` DATETIME,
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
