delete from UserFunction;
insert into UserFunction(GroupKey,RoleId,FunctionStr,DeleteFlag,submission_user,submission_date) select 'b',1,concat('/',Href),0,'alvin',curdate() from Chapter;
insert into UserFunction(GroupKey,RoleId,FunctionStr,DeleteFlag,submission_user,submission_date) select 'b',2,replace(LessonHref,'/index','/ins'), 0,'alvin',curdate() from BookLesson;
insert into UserFunction(GroupKey,RoleId,FunctionStr,DeleteFlag,submission_user,submission_date) select 'b',2,replace(LessonHref,'/index','/upd'), 0,'alvin',curdate() from BookLesson;
insert into UserFunction(GroupKey,RoleId,FunctionStr,DeleteFlag,submission_user,submission_date) select 'b',2,replace(LessonHref,'/index','/del'), 0,'alvin',curdate() from BookLesson;
