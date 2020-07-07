use alvin;
drop table `Chapter`;
create table IF NOT EXISTS `Chapter`( -- 书的大章节表
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`BookLessonId` INT NOT NULL, -- 课程id
	`ChapterNo` INT NOT NULL, -- 第几章
	`ChapterName` VARCHAR(100) character set utf8 NOT NULL, -- 章节名
	`Href` VARCHAR(100) NOT NULL, -- 网页章节所对应的超链接 
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`submission_user` VARCHAR(30), -- 上传人
	`submission_date` DATE, -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;