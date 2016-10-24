
function total_out_in(){
    var total_out = 0;
        total_in = 0;
    
    // out
    for(i=1; i<=9; i++){ 
        var k = '#id_hole_' + i;
        v = Number($(k).val());

        total_out += v;

        console.log(k);
        console.log(v);
    }        

    // in
    for(i=10; i<=18; i++){ 
        var k = '#id_hole_' + i;
        v = Number($(k).val());

        total_in += v;

        console.log(k);
        console.log(v);
    }        
    
    console.log(total_out);
    console.log(total_in);
}


var complete = function(id, db, parm, fnn){
	$(id).autocomplete({
	        source:function(query,process){
	            $.post('/admin/account/autocomplate',{'db':db, 'query':$(id).attr('base_name')+':'+$(id).val(), 'return':parm},function(respData){
	                return process(respData.data);
	            });
	        },
	        formatItem:function(item){
				var p = []
				$.each(parm.split('|'), function(index, name){
					p.push(item[name])
				})
	            return p.join(' ');
	        },
	        setValue:function(item){
				var n = $(id).attr('base_name');
				var fn = n.split(',')[0];
	            return {'data-value':item[fn],'real-value':item[fn]};
	        },
			delay:0
	    });
 
}