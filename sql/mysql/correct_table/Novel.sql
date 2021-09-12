use alvin;
drop table IF EXISTS `Spider`;
create table IF NOT EXISTS `Spider`( -- 爬虫内容表
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`Name` VARCHAR(50) NOT NULL DEFAULT '', -- 名字
	`Author` VARCHAR(50) NOT NULL, --作者
	`Synopsis` TEXT NOT NULL DEFAULT '', -- 简介
	`Image` TEXT NOT NULL, -- 图片
	`Category` VARCHAR(50) NOT NULL, -- 分类 书籍，图片，视频，音频
	`CategoryId` INT UNSIGNED NOT NULL, -- 子分类
	`CategoryName` VARCHAR(200) NOT NULL,
	`Type` INT NOT NULL DEFAULT 0, -- 类别 choices=(("0",u"连载"),("1","完结"))
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`CreateTime` DATETIME NOT NULL, --创建时间
	`UpdateTime` DATETIME NOT NULL, --更新时间
	`submission_user` VARCHAR(30), -- 上传人
	`submission_date` DATE, -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;