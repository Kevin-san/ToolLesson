use alvin;
drop table BookArticle;
create table IF NOT EXISTS `BookArticle`(
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`ArticleId` INT NOT NULL, -- 段落顺序
	`TitleHref` VARCHAR(100) character set utf8 NOT NULL, -- 段落来源超链接 对应BookTitle 中的Href
	`ParagraphType` VARCHAR(100) character set utf8 NOT NULL, -- 段落类型，暂时支持 段落  p, 脚本块  pre, 标题 h1, 表 table,图片 img ,队列 ul , 超链接 a
	`ParagraphText` VARCHAR(10000) character set utf8 NOT NULL, -- 段落内容
	`ParagraphChildText1` VARCHAR(1000) character set utf8,
	`ParagraphChildText2` VARCHAR(1000) character set utf8,
	`ParagraphChildText3` VARCHAR(1000) character set utf8,
	`ParagraphChildText4` VARCHAR(1000) character set utf8,
	`ParagraphChildText5` VARCHAR(1000) character set utf8,
	`ParagraphChildId` VARCHAR(100), -- 特殊段落对应Id 或null
	`ParagraphOtherAttrs` VARCHAR(100) character set utf8, -- h1, h2, 100*100 , null 段落大小 （支持图片和标题）
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0,
	`submission_user` VARCHAR(30),
	`submission_date` DATE,
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


