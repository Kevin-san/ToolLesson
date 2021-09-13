use alvin;
drop table IF EXISTS `SpiderRule`;
create table IF NOT EXISTS `SpiderRule`( -- 爬虫规则表
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`Url` TEXT NOT NULL DEFAULT '', -- 网址
	`IntroAttr` TEXT,
	`AuthorAttr` TEXT,
	`ImageAttr` TEXT,
	`IndexAttr` TEXT NOT NULL,
	`ContentAttr` TEXT NOT NULL,
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`CreateTime` DATETIME NOT NULL DEFAULT NOW(), --创建时间
	`UpdateTime` DATETIME NOT NULL DEFAULT NOW(), --更新时间
	`submission_user` VARCHAR(30) DEFAULT 'alvin', -- 上传人
	`submission_date` DATE DEFAULT curdate(), -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;