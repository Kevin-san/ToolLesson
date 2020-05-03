use alvin;
drop table LessonMenuIndex;
create table IF NOT EXISTS `LessonMenuIndex`(
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`Type` VARCHAR(100) NOT NULL,
	`Href` VARCHAR(100) NOT NULL,
	`Alt` VARCHAR(100) NOT NULL,
	`Title` VARCHAR(100) NOT NULL,
	`Text` VARCHAR(400) NOT NULL,
	`ImgSrc` VARCHAR(100) NOT NULL,
	`ImgWidth` INT,
	`ImgHeight` INT,
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0,   
	`submission_user` VARCHAR(30),
	`submission_date` DATE,
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;