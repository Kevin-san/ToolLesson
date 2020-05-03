use alvin;

drop table `LessonDetails`;

create table IF NOT EXISTS `LessonDetails`(
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`ParentKey` VARCHAR(100) NOT NULL, -- bash-index, bash-argvs or bash-index-table1 or bash-index-table1-tr3
	`Type` VARCHAR(100) NOT NULL, -- h1, h2, h3, p , -- ul , table, pre, ol , th , th, td, tr
	`OrderIndex` INT NOT NULL, -- h1/h2/h3/table/pre --> 1,2,3,4,5
	`AttributeMap` VARCHAR(1000) NOT NULL, -- href:/index onclick:mouse or
	`Text` VARCHAR(10000) character set utf8 NOT NULL,
	`ParentFlag` TINYINT NOT NULL DEFAULT 0, -- 0 is children just output -- 1 is parent query children 
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0,   
	`submission_user` VARCHAR(30),
	`submission_date` DATE,
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
