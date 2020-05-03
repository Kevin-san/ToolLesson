use alvin;

create table IF NOT EXISTS `MstAttrVals`(
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`ParentKey` VARCHAR(100) NOT NULL, -- 父类（html,pdf或其它）
	`SpecKey` VARCHAR(100) NOT NULL, -- 特殊关键字(...)
	`Type` VARCHAR(100) NOT NULL, -- 子类型 （html 时为 table, pre, ul,ol, p,img等等, pdf时为pdf 样式内容)
	`AttrKey` VARCHAR(500) NOT NULL, -- 属性关键字 (class , id)
	`AttrVal` VARCHAR(500) NOT NULL, -- 值 （ class val, 或 id val）
	`OtherVals` VARCHAR(500),
	`Comments` VARCHAR(500),
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;