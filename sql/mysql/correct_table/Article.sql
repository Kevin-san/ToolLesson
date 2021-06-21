use alvin;
drop table IF EXISTS `Article`;
create table IF NOT EXISTS `Article`( -- 博客文章表
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`Title` CHAR(50) NOT NULL DEFAULT '', -- 日志标题
	`Synopsis` TEXT NOT NULL DEFAULT '', --日志简介
	`AuthorId` INT UNSIGNED NOT NULL, 
	`AuthorName` VARCHAR(200) NOT NULL,
	`CategoryId` INT UNSIGNED NOT NULL, -- 分类
	`CategoryName` VARCHAR(200) NOT NULL,
	`TagId` INT UNSIGNED NOT NULL, --
	`TagName` VARCHAR(200) NOT NULL, -- 标签
	`Content` TEXT NOT NULL DEFAULT '', --正文
	`Type` INT NOT NULL DEFAULT 0, -- 文章类别 choices=(("0",u"草稿"),("1","正常"))
	`Original` INT NOT NULL DEFAULT 1, -- 是否原创 choices=(("1", "原创"), ("0", "转载"))
	`Click` INT DEFAULT 0, --点击量
	`Like` INT DEFAULT 0, -- 点赞量
	`Up` INT NOT NULL DEFAULT 0, --文章置顶 choices=(("1",u"置顶"),("0","取消置顶"))
	`Support` INT NOT NULL DEFAULT 0, -- 文章推荐 choices=(("1",u"推荐"),("0","取消推荐")), 
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`CreateTime` DATETIME NOT NULL, --创建时间
	`UpdateTime` DATETIME NOT NULL, --更新时间
	`submission_user` VARCHAR(30), -- 上传人
	`submission_date` DATE, -- 上传时间
	PRIMARY KEY ( `Id` ),
)ENGINE=InnoDB DEFAULT CHARSET=utf8;