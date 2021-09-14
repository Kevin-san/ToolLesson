use alvin;
drop table IF EXISTS `SpiderProperty`;
create table IF NOT EXISTS `SpiderProperty`( -- 爬虫组件属性表
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`ItemId` INT NOT NULL,
	`OrderId` INT NOT NULL,
	`PropertyKey` VARCHAR(3000) NOT NULL, -- 网址 作者，章节，图片，简介
	`PropertyValue` VARCHAR(3000) NOT NULL, 
	`PropertyBigVal` VARCHAR(12000) NOT NULL,
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`CreateTime` DATETIME NOT NULL DEFAULT NOW(), --创建时间
	`UpdateTime` DATETIME NOT NULL DEFAULT NOW(), --更新时间
	`submission_user` VARCHAR(30) DEFAULT 'alvin', -- 上传人
	`submission_date` DATE DEFAULT curdate(), -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;