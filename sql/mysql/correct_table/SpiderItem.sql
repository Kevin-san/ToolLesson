use alvin;
drop table IF EXISTS `SpiderItem`;
create table IF NOT EXISTS `SpiderItem`( -- 爬虫组件表
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`SourceId` INT NOT NULL,
	`Url` VARCHAR(10000) NOT NULL, -- 网址
	`Name` VARCHAR(10000) NOT NULL,
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`CreateTime` DATETIME NOT NULL DEFAULT NOW(), --创建时间
	`UpdateTime` DATETIME NOT NULL DEFAULT NOW(), --更新时间
	`submission_user` VARCHAR(30) DEFAULT 'alvin', -- 上传人
	`submission_date` DATE DEFAULT curdate(), -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;