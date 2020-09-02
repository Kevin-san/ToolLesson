use alvin;
drop table IF EXISTS `BookLesson`;
create table IF NOT EXISTS `BookLesson`( -- 书的信息表
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`BookName` VARCHAR(100) NOT NULL, -- 书名
	`LessonName` VARCHAR(100) NOT NULL, -- 书名
	`LessonHref` VARCHAR(100) NOT NULL, -- 网页大章节所对应的超链接
	`BookLessonType_Id` INT NOT NULL, -- 大章分类
	`Description` VARCHAR(100) NOT NULL, -- 介绍
	`ImageContent_Id` INT NOT NULL, -- 图片Id
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`submission_user` VARCHAR(30), -- 上传人
	`submission_date` DATE, -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;