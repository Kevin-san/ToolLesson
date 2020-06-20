use alvin;

drop table `Content`;

create table IF NOT EXISTS `Content`(
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`ChapterId` INT NOT NULL, -- bash-index, bash-argvs or bash-index-table1 or bash-index-table1-tr3
	`ElementTag` VARCHAR(100) NOT NULL, -- h1, h2, h3, p , -- ul , table, pre, ol , image
	`OrderIndex` INT NOT NULL, -- h1/h2/h3/table/pre --> 1,2,3,4,5
	`AttributeMap` VARCHAR(1000), -- href:/index onclick:mouse or
	`Text` VARCHAR(10000) character set utf8,
	`InnerHtmlText` VARCHAR(10000) character set utf8 NOT NULL,
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0,
	`submission_user` VARCHAR(30),
	`submission_date` DATE,
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;