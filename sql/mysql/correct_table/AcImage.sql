use alvin;
drop table IF EXISTS `AcImage`;
create table IF NOT EXISTS `AcImage`( -- 网站相册表
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`Title` CHAR(50) NOT NULL DEFAULT '', -- 日志标题
	`Detail` TEXT NOT NULL DEFAULT '', --日志简介
	`Image` TEXT, -- 图片
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`submission_user` VARCHAR(30), -- 上传人
	`submission_date` DATE, -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;