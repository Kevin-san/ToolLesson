use alvin;

create table IF NOT EXISTS `BookTitle`( -- 书的大章节表
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`OrderId` INT NOT NULL, -- 章节顺序
	`Title` VARCHAR(100) character set utf8 NOT NULL, -- 网页上对应的课程名 （父键）  对应LessonMenuIndex中的Title值小写
	`Href` VARCHAR(100) NOT NULL, -- 网页大章节所对应的超链接
	`Text` VARCHAR(100) character set utf8 NOT NULL, -- 大章节名 （主键）
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`submission_user` VARCHAR(30), -- 上传人
	`submission_date` DATE, -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


