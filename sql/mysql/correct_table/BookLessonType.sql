use alvin;
drop table IF EXISTS `BookLessonType`;
create table IF NOT EXISTS `BookLessonType`( -- 书的分类表
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`CommonType` VARCHAR(100) NOT NULL, -- 分类
	`CommonValue` VARCHAR(100) NOT NULL, -- # id
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`submission_user` VARCHAR(30), -- 上传人
	`submission_date` DATE, -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;