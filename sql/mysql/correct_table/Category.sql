use alvin;
drop table IF EXISTS `Category`;
create table IF NOT EXISTS `Category`(
	`CategoryId` INT UNSIGNED AUTO_INCREMENT,
	`CategoryName` VARCHAR(200) NOT NULL,
	`CategoryValue1` VARCHAR(200),
	`CategoryValue2` VARCHAR(200),
	`CategoryValue3` VARCHAR(200),
	`CategoryFather` INT NOT NULL,
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0,
	`submission_user` VARCHAR(30),
	`submission_date` DATE,
	PRIMARY KEY ( `CategoryId` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
