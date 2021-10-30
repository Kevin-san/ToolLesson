$(function () {
	$('#datetimepicker1').datetimepicker({
	    format: "YYYY-MM-DD",
	    locale: moment.locale('zh-cn'),
	    defaultDate:moment()
	});
	$(".pagination-lg").find("li").each(function(){
		var a = $(this).find("a:first")[0];
		var href = $(a).attr("href")+"/";
		var pathname=location.pathname;
		if (pathname == href){
			$(this).addClass("active");
		} else {
			$(this).removeClass("active");
		}
	});
});