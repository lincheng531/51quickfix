(function($) {
	$.fn.kfilter = function(f1) {
		var _data           = {};
		var _select			= this;	
		var _input          = $(this).children('input');
		var _ul             = $(this).children('ul');
		var _type1          = 0;
		var _type2			= 0;
		var _new_input      = '';
		var show_type       = 0;

		_input.bind('click', function(){
			change_ul();
			_type1 = 1;
			$(this).val();
		}).mouseout(function(){
			_type1 = 0;	
		}).blur(function(){
			_type1 = 0;	
		}).mouseover(function(){
			_type1 = 1;
		}).keyup(function(){
			reset_ul();
		}).keydown(function(event){
			reset_ul();
		})

		_ul.bind('click', function(){
			change_ul();
			_type2 = 1;
		}).mouseout(function(){
			_type2 = 0;	
		}).blur(function(){
			_type2 = 0;	
		}).mouseover(function(){
			_type2 = 1;
		})

		_ul.children('li').each(function(){
			var oid  = $(this).attr('id');
			var text = $(this).html();
			_data[oid] = text;
			$(this).bind('click', function(){
				f1($(this).attr('id'));
			})
		})

		function reset_ul(){
			var val = _input.val().trim();
			//if(val == _new_input){
			//	return
			//}
			_new_input = val;
			var lis = [];
			$.each(_data, function(index, item){
				if(item.indexOf(val) > -1){
					lis.push('<li id="'+index+'">'+item+'</li>');
				}
			})
			_ul.html(lis.join(''));
			_ul.children('li').each(function(){
				$(this).bind('click', function(){
					f1($(this).attr('id'));
				})
			})

		}

		function change_ul(){
			if(_ul.hasClass('active')){
				show_type = 0
				_ul.removeClass('active').css('display', 'none');
			}else{
				show_type = 1
				_ul.addClass('active').css('display','block');
			}
		}

		$(document).click(function(){
			if(_type1==0 && _type2 == 0 && show_type ==1){
				_ul.css('display','none');
				show_type = 0;
			}
			
		});

	}
})(jQuery);