use alvin;

drop table `LessonMenu`;

create table IF NOT EXISTS `LessonMenu`(
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`MenuType` VARCHAR(100) character set utf8 NOT NULL, -- index, bash, linux
	`Href` VARCHAR(100) NOT NULL,
	`Text` VARCHAR(100) character set utf8 NOT NULL,
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0,
	`submission_user` VARCHAR(30),
	`submission_date` DATE,
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;