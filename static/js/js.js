$(function(){
	$('.sidebar li').click(function(){
		$('.sidebar li').removeClass('active')
		$(this).addClass('active');
		$.cookie("curr", $(this).attr('id')); 
	})
	
	KindEditor.ready(function(K) {
	            window.editor = K.editor({
	                    uploadJson : '/admin/upload?category=sale&max_size=80,80',
	                    allowFileManager : true,
						shadowMode:false
	                });

	            K('#id_cover_image_bak').click(function() {
	                editor.loadPlugin('image', function() {
	                    editor.plugin.imageDialog({
	                        imageUrl : K('#id_cover_image').val(),
	                        clickFn : function(url, title, width, height, border, align) {
								var l = url.length;
	                           	var purl = url.substring(0, url.lastIndexOf('.'));
								var furl = url.substring(url.lastIndexOf('.'), l);
								var p = [purl, '_thumb', furl];
								$(window.frames["main"].document).find("#id_cover_image").val(p.join(''))
	                            editor.hideDialog();
	                        }
	                    });
	                });
	            });
	});
	
	
})


var send_sms = function(){
	var content = $('#sms_content').val();
	if(content.length == 0){
		alert('内容不得为空!');
		return 
	}
	var ids = $('.user:checked');
	if(ids.length == 0){
		alert('请选择需要发送短信的用户!');
		return
	}
	var pids = [];
	$.each(ids, function(){
		var v = $(this).val();
		var vs = v.split('_');
		if(vs[0] == 'user'){
			pids.push(vs[1]);

		}
	})
	if(pids.length > 0){
		$.post("/admin/account/send_sms",{content:content, 'mobiles':pids.join('|')},function(result){
		    if(result.status == 1){
		    	alert('发送成功')
				$('#dismiss_sms').click();
				$('#sms_content').val('');
		    }else{
		    	alert('发送失败')
		    }
		});
	}	
}


var create_price = function(month){
	var m = $('#id_price_month').val();
	if(m.length >0){
		month = m
	}
	var shop = $('#id_price_no').val();
	$.post("/admin/price/create_price",{'month':month, 'shop':shop}, function(result){
	    if(result.status == 1){
	    	alert('生成成功')
			window.location.reload();
	    }else{
	    	alert('生成失败')
			window.location.reload();
	    }
	});
}

var create_read = function(curr, month){
	var m = $('#id_read_month').val();
	if(m.length >0){
		month = m
	}
	$.post("/admin/"+curr+"/create",{'month':month}, function(result){
	    if(result.status == 1){
	    	alert('生成成功')
			window.location.reload();
	    }else{
	    	alert('生成失败')
			window.location.reload();
	    }
	});
}

var complete = function(id, db, parm){

	$(id).autocomplete({
   		source: function(request, response) {
        	$.ajax({
            	url: "/admin/account/autocomplate",
            	dataType: "json",
            	data: {'db':db, 'query':$(id).attr('base_name')+':'+$(id).val(), 'return':parm},
            	success: function(data) {
                	response($.map(data.data, function(item) {
						var n = $(id).attr('base_name');
						var fn = n.split(',')[0];
                    	return {
                        	label: item[fn],
                        	value: item[fn]
                    	}
                }));
            	}
        	});
    	},
    	minLength: 1
	});

}


var box = function(currItem, cid){
	var p = [];
	if(cid){
		p.push(cid);
	}else{
		$("input[class='c']:checkbox:checked").each(function(){
			p.push($(this).val());
		})
	}
	if (p.length == 0){
		alert("您没有选择任何数据！")
		return
	}
	par_box = $("#dialog-box", parent.document.body)
	dialog = par_box.dialog({
	     autoOpen: true,
	     height: 200,
	     width: 450,
	     modal: true,
	     buttons: {
	       "发送": function(){
			   var v = $('#send_sms_textarea', parent.document.body).val();
		   		$.ajax({
					type:'POST',
		       		url: "/admin/account/send_sms2",
		       		dataType: "json",
		       		data: {'ids':p.join(','), 'curr':currItem, 'content':v},
		       		success: function(data) {
		           		if(data.status){
		           			 alert('发送成功')
		   					 dialog.dialog( "close" );
							 $('#send_sms_textarea', parent.document.body).val('') 
		           		}else{
		           			alert('发送失败')
		           		}
		       	}
		   		});
	       },
	       "取消": function() {
			 $('#send_sms_textarea', parent.document.body).val('') 
	         dialog.dialog( "close" );
	       }
	     },
	     close: function() {
	       $('#send_sms_textarea', parent.document.body).val('')
	     }
	   });
	//par_box.dialog( "open" );
}


var checkAll = function(id){
	var checkFlag = $(id).prop("checked");
	$("input[class='c']:checkbox:enabled").each(function() { 
	    $(this).prop("checked", checkFlag); 
	}); 
}

var removeItem = function(currItem){
	var p = [];
	$("input[class='c']:checkbox:checked").each(function(){
		p.push($(this).val())
	})
	if (p.length == 0){
		alert("您没有选择任何数据！")
		return
	}
	if (!confirm('您确定要删除吗?')) return;
	$.ajax({
    	url: "/admin/building/delete",
    	dataType: "json",
    	data: {'ids':p.join(','), 'currItem':currItem},
    	success: function(data) {
        	if(data.status){
        		alert('删除成功')
				location.reload();
        	}else{
				var msg = '删除失败';
				if(data.alert.length > 0){
					msg = data.alert;
				}
        		alert(msg)
        	}
    	}
	});
	
}


var removeItem2 = function(currItem, oid){
	if (!confirm('您确定要删除吗?')) return;
	var p = [oid];
	$.ajax({
    	url: "/admin/building/delete",
    	dataType: "json",
    	data: {'ids':p.join(','), 'currItem':currItem},
    	success: function(data) {
        	if(data.status){
        		alert('删除成功')
				location.reload();
        	}else{
				var msg = '删除失败'
				if (data.alert.length > 0){
					msg = data.alert
				}
        		alert(msg)
        	}
    	}
	});
	
}

var changeStatus = function(head_id, id, active){
	$.ajax({
    	url: "/admin/price/change_status",
    	dataType: "json",
    	data: {'id':id, 'active':active, 'head_id':head_id},
    	success: function(data) {
        	if(data.status == 1){
        		location.reload();
        	}
    	}
	});
}

var changeActive = function(curr, obj, oid){
	$.ajax({
    	url: "/admin/"+curr+"/change_active",
    	dataType: "json",
    	data: {'oid':oid, 'active':$(obj).val()},
    	success: function(data) {
        	if(data.status == 1){
        		alert('更新状态成功');
        	}else{
        		alert(data.alert);
        	}
    	}
	});
}

var dump = function(curr, oid){
	var url = "/admin/"+curr+"/export?" + $(oid).serialize();
	$("iframe[name='export']").attr('src', url);
}


