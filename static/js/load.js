$(function () {
	$('#datetimepicker1').datetimepicker({
	    format: "YYYY-MM-DD",
	    locale: moment.locale('zh-cn'),
	    defaultDate:moment()
	});
});