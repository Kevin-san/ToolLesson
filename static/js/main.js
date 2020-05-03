jQuery.article_load = function(param) {
	var arr=param.split("\.");
	var dir=arr[0];
	var name=arr[1];
	$(".main").load(dir+"/"+name);
};
