use alvin;
drop table IF EXISTS `Comment`;
create table IF NOT EXISTS `Comment`( -- 博客评论表
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`ArticleId` INT NOT NULL , -- 日志Id
	`Content` TEXT NOT NULL DEFAULT '', --评论内容
	`AuthorId` INT UNSIGNED NOT NULL, 
	`AuthorName` VARCHAR(200) NOT NULL,
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`CreateTime` DATETIME NOT NULL, --创建时间
	`UpdateTime` DATETIME NOT NULL, --更新时间
	`submission_user` VARCHAR(30), -- 上传人
	`submission_date` DATE, -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;