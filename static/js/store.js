
var show_control = function(oid){
    var p = $('#bk_'+oid);
    var c = $('#bkc_'+oid);
    if (c.hasClass('none')){
        p.addClass('bg1');
        c.addClass('bg1').removeClass('none');
    }else if (c.hasClass('bg1')){
        p.removeClass('bg1');
        c.addClass('none').removeClass('bg1');
    }
}
var check_all = function(pid, cid){
        if ($(pid).is(':checked')) {  
            $(cid).prop('checked', true); 

        } else {   //反之 取消全选   
            $(cid).prop('checked', false);
        }
        if($('#choose').length == 1){
            $('#choose').html($(cid+':checked').length);
        }
}

var check_one = function(cid){
     if($('#choose').length == 1){
            $('#choose').html($(cid+':checked').length);
    }
}

var bcheck_all = function(pid, cid){
    if($(pid).is(':checked')){
        $(pid).prop('checked', false); 
        $(cid).prop('checked', false); 
    }else{
        $(pid).prop('checked', true); 
        $(cid).prop('checked', true);
    }
}

var loading = function(){
    balert('加载中...');
}
var balert = function(msg){
    $.blockUI({ 
        message: '<table><tr><td width="80px"><img src="/static/images/loading.gif"/></td><td>'+msg+'</td></tr></table>', 
        css: { 
            top:  ($(window).height() - 400) /2 + 'px', 
            left: ($(window).width() - 400) /2 + 'px', 
            minWidth: '300px',
            border: '2px solid #dedede', 
            borderRadius:'3px'
        }   
    }); 
    setTimeout($.unblockUI, 2500); 
}

var close_box = function(){
    $.unblockUI();
}

var bbox = function(msg){
    $.blockUI({ 
        message: msg, 
        css: { 
            top:  ($(window).height() - 400) /2 + 'px', 
            left: ($(window).width() - 400) /2 + 'px', 
            minWidth: '300px',
            border: '2px solid #dedede', 
            borderRadius:'3px'
        }   
    });
}

var close_time_box = function(oid){
     $.blockUI({ 
        message: '<div class="ctime_box"><h3>请输入关店时间</h3><p><input type="text" id="close_time" name="close_time"></p><p><input type="button" class="b2" value="提交" id="verfiy_cloe" oid="'+oid+'"/>     <a href="javascript:void(0)" onclick="close_box()">取消</a></p></div>', 
        css: { 
            top:  ($(window).height() - 400) /2 + 'px', 
            left: ($(window).width() - 400) /2 + 'px', 
            minWidth: '300px',
            border: '2px solid #dedede', 
            borderRadius:'3px'
        }   
    }); 
     $('#verfiy_cloe').click(function(){
        var oid = $(this).attr('oid');
        $.ajax({
            type: 'POST',
            url: '/store/assets/store/close/'+oid,
            data:{'close_time':$('#close_time').val()},
            dataType: 'json',
            beforeSend: function(){
                loading()
            },
            success: function(data){
                if(data.status == 1){
                    balert('关闭店铺成功');
                   
                    window.location.href='/store/assets/store/'+oid;
                }
            },
            error : function() {  
                balert('关闭店铺失败，请联系管理员');
               
            }
        })
     })
     $('#close_time').click(function(){
            WdatePicker();
    });
}

var url_parm = function(){
    var vars = {}, hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
      hash = hashes[i].split('=');
      vars[hash[0]] = hash[1];
    }
    return vars;
  }

var search_parm = function(){
    var vars = {}
    $('.search_box').children('ul').children('li').each(function(){
        vars[$(this).attr('name')] = $(this).attr('value');
    })
    return vars
}

var jump = function(name, value, delet){
    var vars = search_parm();
    $.each(url_parm(), function(index, item){
        if(delet!=index){
            vars[index] = item;
        }
    })
    vars[name] = value;
    var url = []
    $.each(vars, function(index, item){
        if (item != undefined){
            url.push(index+'='+item);
        }
    })
    window.location.href='?'+url.join('&')
 }
 

 var inventory = function(){
    var p = [];
    $.each($('input:checked'), function(index, item){
        if($(item).hasClass('c')){
            var v = $(this).val();
            if(v != undefined){
                p.push(v);
            }
        }
    })
    if(p.length == 0){
        balert('请选择需要盘点的餐厅');
        return 
    }
    $('#task_idc_oid').val(p.join(','));
    $('#append_task').submit();
 }

var query_inventory = function(){
    var p = [];
    $.each($('.c'), function(index, item){
        p.push($(this).val());
    })
    $('#id_oid').val(p.join(','));
    $('#task_append_form').submit();
}

var notify_inventory = function(hid, oid){
    $.ajax({
            type: 'POST',
            url: '/store/inventory/notify/'+hid+'/'+oid,
            dataType: 'json',
            beforeSend: function(){
                loading();
            },
            success: function(data){
                if(data.status == 1){
                    balert('提醒成功');
                  
                }
            },
            error : function() {  
                balert('提醒失败');
                
            }
        })
}


var dump_qrcode = function(){
    var p = [];
    $.each($('input:checked'), function(index, item){
        if($(item).hasClass('c')){
            var v = $(this).val();
            if(v != undefined){
                p.push(v);
            }
        }
    })
    if(p.length == 0){
        alert('请选择需要生成的二维码');
    }else{
       $('#dump_qrcode_oid').val(p.join(',')) ;
       $('#cdump_qrcode').submit();
    }

}

var dump_export = function(){  
    var p = [];
    $.each($('input:checked'), function(index, item){
        if($(item).hasClass('c')){
            var v = $(this).val();
            if(v != undefined){
                p.push(v)
            }
        }
    })
    
    if(p.length == 0){
        alert('请选择导出报表的餐厅');
    }else{
       $('#dump_idc_oid').val(p.join(',')); 
       $('#dump_idc').submit();
    }
 }

 var store_edit_submit = function(){
    var province  = store_data[form.province.value];
    var city      = store_data[form.city.value];
    var area      = store_data[form.area.value];
    $('input[name="cprovince"]').val(province);
    $('input[name="ccity"]').val(city);
    $('input[name="carea"]').val(area);
    form.submit()
 }

 var ctoggle = function(target){
    var p = $(target).hasClass('p');
    if(p){
        $(target).css('display','none').removeClass('p');
    }else{
        $(target).removeAttr('style').addClass('p');
    }
 }

var insert_district = function(v, d){
   $.ajax({
        type: 'POST',
        url: '/store/assets/region',
        data:{'name':v},
        dataType: 'json',
        beforeSend: function(){
            loading();
        },
        success: function(data){
            if(data.status == 1){
                var p = [];
                $.each(data.results, function(index, item){
                    if(item == d){
                        p.push('<option  selected="selected"  value="'+item+'">'+item+'</option>')
                    }else{
                        p.push('<option value="'+item+'">'+item+'</option>')
                    }
                    
                })
                $('#id_district').html(p.join(''))
            }
        },
        error : function() {  
            balert('提醒失败');
            
        }
    })
}

var init_product = function(){
    $('#id_product').change(function(){
        
    })
}

var init_region = function(){
    insert_district($('#id_city').val(),$('#id_district').val())
    $('#id_city').change(function(){
        insert_district($(this).val(),'')
    })
}

var dump_inventory = function(){
    var p = [];
    $.each($('input:checked'), function(index, item){
        if($(item).hasClass('c')){
            var v = $(this).val();
            if(v != undefined){
                p.push(v)
            }
        }
    })
    if(p.length == 0){
        balert('请选择需要导出的盘点');
        return 
    }
    $('#inventory_form1').children('#oid').val(p.join(','));
    $('#inventory_form1').submit()
}

var inventory_search = function(obj, head_type){
    var ele = $(obj);

    if(head_type == 1){
        if(ele.hasClass('active')){
            $('a[area="'+ele.html()+'"]').removeClass('active');
        }else{
            $('a[area="'+ele.html()+'"]').addClass('active');
        }
        
    };
    if(head_type == 2){
        if(ele.hasClass('active')){
            $('a[company="'+ele.html()+'"]').removeClass('active');
        }else{
            $('a[company="'+ele.html()+'"]').addClass('active');
        }
    };
    if(ele.hasClass('active')){
       ele.removeClass('active') 
    }else{
        ele.addClass('active')
    };
    var areas = [];
    var companys = [];
    var citys = [];
    var scope = [];
    $.each($('a[cid="c2"]'), function(index, item){
        if($(this).hasClass('active')){
            var v = $(this).html();
            if($(this).attr('name') == 'area'){
                areas.push(v);
            }
            if($(this).attr('name') == 'company'){
                companys.push(v);
            }
            if($(this).attr('name') == 'city'){
                citys.push(v);
            }
            scope.push(v);
        }
    })
    $.ajax({
        type: 'POST',
        url: '/store/inventory/store',
        dataType: 'json',
        data:{'area':areas.join(','),'company':companys.join(','),'city':citys.join(',')},
        beforeSend: function(){
            loading();
        },
        success: function(data){
            if(data.status == 1){
                var p = [];
                var oids = [];
                var count = 0;
                $.each(data.results, function(index, item){
                    count += 1;
                    p.push('<tr id="bk_'+item.id+'" onmouseover="this.style.backgroundColor=\'#e1e1e1\'" onmouseout="this.style.backgroundColor=\'#fff\'">'+
                                '<td style="width:80px" class="center"><input type="hidden" value="'+item.id+'"  class="c"><a href="/store/assets/store/'+item.id+'">'+item.city+'</a></td>'+
                                '<td style="width:80px"><a href="/store/assets/store/'+item.id+'">'+item.no+'</a></td>'+
                                '<td class="tip1"><a href="/store/assets/store/'+item.id+'">'+item.name+'</a><p><a href="/store/assets/store/'+item.id+'">'+item.address+'</a></p></td>'+
                                '<td>'+item.opening_time+'</td>'+
                                '<td  style="line-height: 20px;">'+item.store_manager+'<p class="f3">'+item.mobile+'</p></td>'+
                                '<td>待盘点'+item.device_count+'项</td>'+
                                '<td style="text-align: center"><img onclick="$(\'#bk_'+item.id+'\').remove();$(\'#store_total\').html($(\'.c\').length)" src="/static/images/icon_close.png"/></td>'+
                            '</tr>');
                    oids.push(item.id);

                });
            
                $('#inventory_content').html(p.join(''));
                $('#store_total').html(count);
                $('#id_oid').val(oids.join(','));
                $('#id_scope').val(scope.join(','))
            }
        },
        error : function() {  
            balert('提醒失败');
            
        }
    })


}

var dump_repair = function(){
    var p = [];
    $('.search_box').find('li').each(function(){
        var name = $(this).attr('name');
        var value = $(this).attr('value');
        p.push(name+':'+value);
    })
    $('input[name="sb"]').val(p.join('|'));
    $('#repair_form1').submit();
}

var verify_account  = function(ids){
    $(ids).bind('click', function(){
        var v = $(this).val();
        var vclass = $(this).attr('class');
        if(v == '-1'){
            $.each($('.'+vclass+'1'), function(){
                $(this).val('');
            })
        }else{
            $.each($('.'+vclass+'0'), function(){
                $(this).val('');
            })
        }
    })
}

var valid_forms = function(form1){
    var lic_type = $('input[name="licence_type"]:checked').val();
    var cer_type = $('input[name="certificate_type"]:checked').val();
    if(lic_type == undefined){
        alert('营业执照必须审核');
        return 
    }
    if(cer_type == undefined){
        alert('税务登记证必须审核');
        return
    }
    if(lic_type == 1){
        var ld   = $('#id_licence_day').val();
        var ld1  = $('#id_licence_day1').val();
        if(ld.length == 0 || ld1.length==0){
            alert('营业执照必须填写起始时间和结束时间');
            return false;
        }
    }
    if(cer_type == 1){
        var cd   = $('#id_certificate_day').val();
        var cd1  = $('#id_certificate_day1').val();
        if(cd.length == 0 || cd1.length==0){
            alert('税务登记证必须填写起始时间和结束时间');
            return false;
        }
    }
    $(form1).submit();
}

var valid_forms2 = function(form1){
    var data = $(form1).serializeArray();
    var pdata = {};
    $.each(data, function(index, item){
        pdata[item.name] = item.value;
    })
    var p = 1;
    $.each(data, function(index, item){
        var name = item.name;
        var value = item.value;
        if(name.indexOf('card_type') > -1){
            if(value == '1' && (pdata['screen_name'].length==0 || pdata['card_no'].length==0)){
                alert('用户名,身份证号码不得为空');
                p = 0;
            }
        }else if(name.indexOf('electrician_type') > -1){
            if(value == '1' && (pdata['electrician_day1'].length==0 || pdata['electrician_day2'].length==0)){
                alert('电工证有效期不得为空');
                p = 0;
            }
        }else if(name.indexOf('gas_type') > -1){
            if(value == '1' && (pdata['gas_day1'].length==0 || pdata['gas_day2'].length==0)){
                alert('煤气证有效期不得为空');
                p = 0;
            }
        }else if(name.indexOf('refrigeration_type') > -1){
            if(value == '1' && (pdata['refrigeration_day1'].length==0 || pdata['refrigeration_day2'].length==0)){
                alert('制冷证有效期不得为空');
                p = 0;
            }
        }else if(name.indexOf('train_type_') > -1){
            var step = name.split('_')[2];
            if(value == '1' && (pdata['train_name_'+step].length==0 || pdata['train_day1_'+step].length==0 || pdata['train_day2_'+step].length==0 || pdata['train_brand_'+step].length==0 || pdata['train_category_'+step].length==0)){
                alert('厂家培训证,证件名称,品牌,设备,有效期不得为空');
                p = 0;
            }
        };
    });
    if(p == 1){
      $(form1).submit();  
    }
    
}

var verify_box = function(count, cid){
    msg = '<div class="vbox">'+
            '<h3>提示</h3>'+
            '<div class="content"><p>你已经选择了<span class="f1">'+count+'</span>个工单</p><p>请务必确认开票确认之后再结算</p></div>'+
            '<div class="footer">'+
                '<input class="b4" type="button" value="取消" onclick="close_box()"/>'+
                '<input class="b2" type="button" value="结算" onclick="push_verify(\''+cid+'\')"/>'+
            '</div>'+
          '</div>'
    bbox(msg)
}

var verify_one = function(cid, category){
    if(category == 1){
        var cid = $(cid).attr('cid');
    }else{
        var checkeds = $('input[class="c"]:checked');
        var p = []
        $.each(checkeds, function(){
            p.push($(this).attr('cid'))
        })
        var cid = p.join(',')

    }
    verify_box(cid.split(',').length, cid)

}

var push_verify = function(id, cids){
    $.ajax({
        type: 'POST',
        url: '/provider/verify/close',
        dataType: 'json',
        data:{'ids':cids},
        beforeSend: function(){
            loading();
        },
        success: function(data){
            if(data.status == 1){
                balert('结算成功，请等待商户结算')
                window.location.href='/provider/repair/edit/'+id
            }
        },
        error : function() {  
            balert('结算失败，请联系管理员');
            
        }
    })
}

var tr_delete = function(obj){
    $(obj).parent('td').parent('tr').remove()
}

var add_cost = function(){
    $('#sum_total').before('<tr ><th><input  class="tr" type="text" name="other_name"  onfocus="if(this.value==\'请输入花费名称\'){this.value=\'\'}; this.className=\'tr\'" onblur="if(this.value==\'\'){this.value=\'请输入花费名称\'};this.className=\'f2 tr\'"  value="请输入花费名称"></th><td><div class="input_box">¥<input name="other_price" class="charge" value="请输入花费费用" onpropertychange="sum_charge(\'.charge\', \'#sum_total2\')" oninput="sum_charge(\'.charge\', \'#sum_total2\')" onfocus="if(this.value==\'请输入花费费用\'){this.value=\'\'}" onblur="if(this.value==\'\'){this.value=\'请输入花费费用\'}" > </div><a class="fr" style="margin-right: 50px;padding:0;line-height:20px;course:pointer; href="javascript:void(\'0\')" onclick="tr_delete(this);ctrigger(\'.charge\')">X</a></td></tr>')
}

var open_spare = function(oid){
     $.blockUI({ 
        message: '<div style="height:500px;position:relative"><a style="position:absolute;right:0px;top:0px" href="javascript:void(0)" onclick="close_box()">X</a> <iframe id="id_iframe" src="/provider/repair/spare/'+oid+'" frameborder="0" scrolling="no" width="100%" height="100%"></div>',      
        css: { 
            top:  ($(window).height() - 500) /2 + 'px', 
            left: ($(window).width() - 500) /2 + 'px', 
            minWidth: '500px',
            height: '500px',
            border: '2px solid #dedede', 
            borderRadius:'6px'
        }   
    }); 
}


var active_button = function(obj){
    var buttons = $(obj).siblings('.button');
    buttons.removeClass('active');
    $(obj).addClass('active');
    var input = $(obj).children('input');
    var name  = $(input).attr('name');
    $.each(buttons, function(index, item){
        $(item).children('input').removeAttr('checked');
    })
    input.attr('checked','checked');
    spare_change(obj);
    ctrigger('.charge')

}

var init_tr = function(tbody){
    var trs = $(tbody).children('tr');
    $.each(trs, function(index, item){
        if(index%2 == 0){
            $(item).addClass('active')
        }
    })
}

var sum_charge = function(cl, tl){
    var cls = $(cl);
    var total = 0;
    $.each(cls, function(index, item){
        var v = $(item).val();
        if(isNaN(v)){
            balert('只允许输入字符');
            $(item).val('');
            return 
        }
        if(v.length == 0){
            v = 0;
        }
        total += parseFloat(v)
        
    })
    $(tl).html(total.toFixed(2))
}

var verify_detail_submit = function(category){
    if($('input[name="tip"]').is(':checked') != true){
        alert('请勾选本工单已核对无误');
        return;
    }
    var query = {};
    query['status'] = category;
    query['user_message'] = $('textarea[name="user_message"]').val();
    if(query['user_message'] == '请填写备注信息') query['user_message'] = '';
    $.ajax({
        type: 'POST',
        url: '',
        dataType: 'json',
        data:query,
        beforeSend: function(){
            loading();
        },
        success: function(data){
            balert('提交成功！');
        },
        error : function() {  
            balert('提交失败！');
            
        }
    }) 
}

var verify_submit = function(category){
    if($('input[name="tip"]').is(':checked') != true){
        alert('请勾选本工单已核对无误');
        return;
    }
    
    var other_name = [];
    var _p = 0;
    $.each($('input[name="other_name"]'), function(index, item){
        var v = $(item).val();
        if(v.length==0 || v=='请输入花费名称'){
            alert('花费名称不得为空');
            _p = 1;
        }
        other_name.push(v)
    });
    var other_price = [];
    $.each($('input[name="other_price"]'), function(index, item){
        var v = $(item).val();
        if(v.length == 0 || v == '请输入花费费用'){
            alert('请输入花费费用');
            _p = 1; 
        }
        other_price.push(v)
    });
    if(_p == 1) return;
    var spare_id       = [];
    var spare_count    = [];
    var spare_category = [];
    var spare_status   = [];
    $.each($('input[name="spare_id"]'), function(index, item){
        spare_id.push($(item).val());
    });
    $.each($('input[name="spare_count"]'), function(index, item){
        spare_count.push($(item).val());
    });
    $.each($('input[name="spare_category"][checked="checked"]'), function(index, item){
        spare_category.push($(item).val());
    });
    $.each($('input[name="spare_status"][checked="checked"]'), function(index, item){
        spare_status.push($(item).val());
    });

    var query = {};
    query['travel'] = $('input[name="travel"]').val();
    query['labor']  = $('input[name="labor"]').val();
    query['stay_total']  = $('input[name="stay_total"]').val();
    query['other_name']  = other_name.join('|');
    query['other_price'] = other_price.join('|');
    query['spare_id']       = spare_id.join('|');
    query['spare_count']    = spare_count.join('|');
    query['spare_category'] = spare_category.join('|');
    query['user_message']   = $('textarea[name="user_message"]').val();
    query['spare_status']   = spare_status.join('|');
    query['category']       = category;
    if(query['user_message'] == '请填写备注信息') query['user_message'] = '';

    $.ajax({
        type: 'POST',
        url: '',
        dataType: 'json',
        data:query,
        beforeSend: function(){
            loading();
        },
        success: function(data){
            balert('提交成功！');
        },
        error : function() {  
            balert('提交失败！'); 
        }
    })  
}


var ctrigger = function(cls){
    var oninput = jQuery.Event("oninput");
    var onpropertychange = jQuery.Event("onpropertychange"); 
    $(cls).trigger(onpropertychange).trigger(oninput); 

}

var spare_change = function(obj){
    var tr1 = $(obj).parent('div').parent('td').parent('tr')
    var tr2 = $(obj).parent('td').parent('tr');
    if(tr1.length >0)var tr = tr1;
    if(tr2.length >0)var tr = tr2;
    var category = tr.find('input[name="spare_category"][checked="checked"]').val();
    var status   = tr.find('input[name="spare_status"][checked="checked"]').val();
    var count    = tr.find('input[name="spare_count"]').val();
    var price    = tr.find('input[name="spare_price"]').val();
    console.log(category);
    console.log(status);
    console.log(count);
    console.log(price);
    if(category == '1' && status == '1'){
        price = 0;
    }
    var total = count * price;
    tr.find('input[name="spare_charge"]').val(total);
    tr.find('.spare_total').html(total);
}





