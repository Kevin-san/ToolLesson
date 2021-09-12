use alvin;
drop table IF EXISTS `Section`;
create table IF NOT EXISTS `Section`( -- 章节表
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`OrderNo` INT NOT NULL, -- 章节顺序
	`RollName` VARCHAR(200), -- 卷名
	`Name` VARCHAR(200) NOT NULL, -- 章节名
	`Content` TEXT NOT NULL, -- 内容
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`CreateTime` DATETIME NOT NULL, --创建时间
	`UpdateTime` DATETIME NOT NULL, --更新时间
	`submission_user` VARCHAR(30), -- 上传人
	`submission_date` DATE, -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;