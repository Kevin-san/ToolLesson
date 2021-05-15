use alvin;
drop table IF EXISTS `SpiderImageGroup`;
create table IF NOT EXISTS `SpiderImageGroup`( -- 图片组的信息表
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`RootUrl` VARCHAR(100) NOT NULL, -- 图片主页
	`RootPath` VARCHAR(100) NOT NULL, -- 图片本地目录
	`GroupName` VARCHAR(100) NOT NULL, -- 图片组名
	`GroupUrl` VARCHAR(100) NOT NULL, -- 图片组url
	`DivIndexAttrs` VARCHAR(100) NOT NULL, -- 对应目录属性(默认class)
	`DivContentAttrs` VARCHAR(100) NOT NULL, -- 对应内容属性(默认class)
	`Directory` VARCHAR(100) NOT NULL, -- 组目录
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`submission_user` VARCHAR(30), -- 上传人
	`submission_date` DATE, -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;