function getId(obj) {
    return document.getElementById(obj);
}

function line(n,paramId){
	var num = "";
	var lineobj = $("#"+paramId);
	for(var i = 1;i <= n;i ++){
		num += i + "\n";
	}
	lineobj.val(num);
}

function inputKeyUp(paramId){
    	var strarr = [];
    	var inputobj= getId(paramId+"_inputarea");
    	var str = inputobj.value;
    	var repstr = str.replace(/\r/gi,"");
    	strarr = repstr.split("\n");
    	var n = strarr.length;
    	line(n,paramId+"_inleftNum");
}
function outputKeyUp(paramId){
    	var strarr = [];
    	var outputobj= getId(paramId+"_"+"outputarea");
    	var str= outputobj.value;
    	var repstr = str.replace(/\r/gi,"");
    	strarr = repstr.split("\n");
    	var n = strarr.length;
    	line(n,paramId+"_outleftNum");
}
