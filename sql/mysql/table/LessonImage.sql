use alvin;

drop table `LessonImage`;

create table IF NOT EXISTS `LessonImage`(
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`ImgKey` VARCHAR(100) NOT NULL,
	`Class` VARCHAR(500),
	`Href` VARCHAR(100) NOT NULL,
	`Alt` VARCHAR(100) NOT NULL,
	`Src` VARCHAR(500) NOT NULL, -- /static/img/...png
	`Width` INT,
	`Height` INT,
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0,
	`submission_user` VARCHAR(30),
	`submission_date` DATE,
	PRIMARY KEY (`Id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;