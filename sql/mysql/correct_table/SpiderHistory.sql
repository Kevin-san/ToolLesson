use alvin;
drop table IF EXISTS `SpiderHistory`;
create table IF NOT EXISTS `SpiderHistory`( -- 爬虫履历表
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`RootPath` VARCHAR(100) NOT NULL, -- 根目录
	`RootUrl` VARCHAR(100) NOT NULL, -- 主页
	`RealPath` VARCHAR(100) NOT NULL, -- 真实路径
	`RealUrl` VARCHAR(100) NOT NULL, -- 真实url
	`DivIndexAttrs` VARCHAR(100), -- 对应组目录属性(默认class)
	`DivContentAttrs` VARCHAR(100), -- 对应组内容属性(默认class)
	`ValIndexAttrs` VARCHAR(100) NOT NULL, -- 对应目录属性(默认class)
	`ValContentAttrs` VARCHAR(100) NOT NULL, -- 对应内容属性(默认class)
	`Directory` VARCHAR(100) NOT NULL, -- 目录名
	`FileName` VARCHAR(100) NOT NULL, -- 文件名
	`SpiderVal` VARCHAR(10000) NOT NULL, -- img src, novel val, music src,
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`submission_user` VARCHAR(30), -- 上传人
	`submission_date` DATE, -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;