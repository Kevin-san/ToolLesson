use alvin;

drop table IF EXISTS `CommonRules`;

create table IF NOT EXISTS `CommonRules`(
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`TypeKey` VARCHAR(100) NOT NULL, -- html5,pdf ...
	`TypeVal` VARCHAR(100) NOT NULL, --ElementTagName h1, h2, h3, p , | ul , table, pre, ol , image
	`Rules` VARCHAR(100) NOT NULL, -- h1(text),h2(text),h3(text),p(text),ul(li(text)),table(tbody(tr(th(text0))tr(td(text)))),pre(text),ol(li(text),p(img(attrs)
	`RulesDescription` VARCHAR(1000) NOT NULL, -- <h1>text</h1>,<h2>text</h2>,<h3>text</h3>,p(text),ul(li(text)),table(tbody(tr(th(text0))tr(td(text)))),pre(text),ol(li(text),p(img(attrs)
	`RulesText` VARCHAR(10000) character set utf8 ,
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0,
	`submission_user` VARCHAR(30),
	`submission_date` DATE,
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;