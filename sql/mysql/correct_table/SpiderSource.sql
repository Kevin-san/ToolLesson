use alvin;
drop table IF EXISTS `SpiderSource`;
create table IF NOT EXISTS `SpiderSource`( -- 爬虫源表
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`Name` VARCHAR(50) NOT NULL DEFAULT '', -- 名字
	`Section` VARCHAR(50) NOT NULL, -- 分类
	`Url` VARCHAR(3000) NOT NULL DEFAULT '', -- 网址
	`Attr` VARCHAR(3000) NOT NULL, -- 属性
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`CreateTime` DATETIME NOT NULL, --创建时间
	`UpdateTime` DATETIME NOT NULL, --更新时间
	`submission_user` VARCHAR(30), -- 上传人
	`submission_date` DATE, -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;