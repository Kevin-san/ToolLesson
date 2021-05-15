var interVal;
function fixText(text){
	var replaceRegex = /(\n\r|\r\n|\r|\n)/g;
	var strval = text.toString() || '';
	strval = strval.replace(/\"/g,'\\"');
	return strval.replace(replaceRegex,'\\r\\n');
}

function clean(paramId){
	var inputItem = $('#'+paramId+"_inputarea");
	var outputItem = $('#'+paramId+"_outputarea");
	outputItem.val("");
	inputItem.val("");
}

function selectDiv(obj,paramId){
	$("#"+paramId+"_" + obj.value).show().siblings().hide();
}

function ajaxFunction(paramId){
	var selectedOption=$('#'+paramId+" select option:selected");
	var selectedFunc=selectedOption.val();
	var inputValue=$('#'+paramId+"_inputarea").val();
	var outputItem=$('#'+paramId+"_outputarea");
	var pass = "";
	if(paramId == "codetool" || paramId == "converttool"){
		pass = prompt("请输入特殊值");
	}
	if(inputValue == ""){
		alert('please input text into left text area.');
	}else{
		$.ajax({
			url: '/tool/funcs',
			type: 'post',
			dataType:'json',
			data: {
				tool: paramId,
				method: selectedFunc,
				inputarea: inputValue,
				passkey:pass
			},
			success:function(data){
				outputItem.empty();
				if(paramId == "ziptool" || paramId == "converttool" || paramId == "strtool"){
					outputItem.val(data.outputarea);
				}else{
					outputItem.val(eval("'"+fixText(data.outputarea)+"'"));
				}
			},
		})
	}
}

var timeoutBox;//timeout定时器存储器
//设置正常的timeout定时器
function startTimerTimeout() {
	interVal=setTimeout("",1000); //设置控件时间
    clearTimeout(timeoutBox);//初始化timeout定时器，防止定时器重叠
    timeoutBox = setTimeout(function(){//设置timeout定时器
    	$('#toolspicker').data('DateTimePicker').date(moment());
        clearTimeout(timeoutBox);//清除当前timeout定时器，timeout定时器只运行一次代码，直接清掉它
        // location.href="timer.html";//一段时间后跳转页面是setTimeout的常用场景之一
    }, 1000);
}
//设置循环的timeout定时器
function startTimerTimeoutTwo() {
    clearTimeout(timeoutBox);//初始化timeout定时器，防止定时器重叠
    timeoutBox = setTimeout(function(){
    	$('#toolspicker').data('DateTimePicker').date(moment());
        startTimerTimeoutTwo();//循环调用函数自身，以达到循环的效果
    }, 1000);
}
// 结束循环的timeout定时器
function stopTimeout() {
    clearTimeout(timeoutBox);
}

function make_qr_code(divId,inputId){
	$('#'+divId).empty();
	var inputval = $('#'+inputId).val();
	var qrcode = new QRCode(document.getElementById(divId), {
        text: inputval,
        width: 128,
        height: 128,
        colorDark: "#000000",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.H
    });
}

function make_bar_code(divId,inputId){
	$('#'+divId).empty();
	var inputval = $('#'+inputId).val();
	JsBarcode('#'+divId, inputval, {
        format: "CODE128",
        displayValue: true, 
        fontSize: 24,
        lineColor: "#0cc"
    });
}

function tool_picker(toolName){
	stopTimeout();
	$('#clickbutton').off();
	$('#toolintext').off();
	$('#toolspicker').off('touchstart');
	$('#toolspicker').off('click');
	$('#toolspicker').attr('class','input-group-btn form-group');
	$('#clickbutton').attr('class','btn btn-default');
	$('#toolintext').removeAttr('readonly');
	$('#toolintext').val("");
	if(toolName =="timer"){
		$('#clickspan').attr("class","glyphicon glyphicon-time");
		$('#toolspicker').datetimepicker({format:'YYYY-MM-DD HH:mm:ss'});
		$('#toolintext').attr('readonly','readonly');
		startTimerTimeoutTwo();
	}else if(toolName=="colorpicker"){
		$('#clickspan').attr("class","glyphicon glyphicon-tint");
		$('#toolspicker').spectrum({
			preferredFormat: "hex3",
			showInput: true,
		    showPalette: true,
	    });
	}else if(toolName=="colorpickerHSLFormat"){
		$('#clickspan').attr("class","glyphicon glyphicon-edit");
		$('#toolspicker').spectrum({
			preferredFormat: "hsl",
			showInput: true,
		    showPalette: true,
	    });
	}else if(toolName=="colorpickerRGBFormat"){
		$('#clickspan').attr("class","glyphicon glyphicon-map-marker");
		$('#toolspicker').spectrum({
			preferredFormat: "rgb",
			showInput: true,
		    showPalette: true,
	    });
	}else if(toolName=="searcher"){
		$('#clickspan').attr("class","glyphicon glyphicon-search");
		$('#clickbutton').click(function(){
			var searchtext = $('#toolintext').val();
			$.post('/search',{
				search:searchtext
			},
			function(data,status){
				alert("");
			})
		})
	}else if(toolName =="qrcodew"){
		$('#clickspan').attr("class","glyphicon glyphicon-qrcode");
		$('#clickbutton').click(function(){
			var inputval = $('#toolintext').val();
			var $textAndPic = $('<div id="barqrcode"></div>');
			BootstrapDialog.show({
				size: BootstrapDialog.SIZE_SMALL,
	            title: 'QR Code:'+inputval,
	            message: $textAndPic,
	            buttons: [{
	            	label: 'Generate QR Code',
	            	cssClass: 'btn-primary',
	            	action: function(dialogRef){
	            		make_qr_code('barqrcode','toolintext');
	            	}
	            }]
	        });
		});
	}else if(toolName =="barcodew"){
		$('#clickspan').attr("class","glyphicon glyphicon-barcode");
		$('#clickbutton').click(function(){
			var inputval = $('#toolintext').val();
			var $textAndPic = $('<div></div>');
			$textAndPic.append('<img id="barqrcode"/>');
			BootstrapDialog.show({
				size: BootstrapDialog.SIZE_SMALL,
				title: 'Bar Code:'+inputval,
	            message: $textAndPic,
	            buttons: [{
	            	label: 'Generate Bar Code',
	            	cssClass: 'btn-primary',
	            	action: function(dialogRef){
	            		make_bar_code('barqrcode','toolintext');
	            	}
	            }]
	        });
		});
	}
}

