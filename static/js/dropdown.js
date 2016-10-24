(function($) {
	$.fn.cdropdown = function(f1) {
		var _select			= this;	
		var _div            = $('#dropdown_'+$(this).attr('ref'))
		var _type1          = 0;
		var _type2          = 0;

		reset_css();

		_select.bind('click', function(){
			change_div();
		}).mouseout(function(){
			_type1 = 0;	
		}).blur(function(){
			_type1 = 0;	
		}).mouseover(function(){
			_type1 = 1;
		}).keyup(function(){
			_type1 = 1
		}).keydown(function(){
			_type1 = 1
		})
		_div.bind('click', function(){
			_type2 = 1
		}).mouseout(function(){
			_type2 = 0;	
		}).blur(function(){
			_type2 = 0;	
		}).mouseover(function(){
			_type2 = 1;
		}).keyup(function(){
			_type2 = 1
		}).keydown(function(){
			_type2 = 1
		})

		f1(_div);
		function reset_css(){
			var ps = _select.offset();
			var left = (ps.left)+'px';
			var top = (ps.top+40)+'px';
			_div.css({
					'position':'absolute', 'top':top, 'left':left, 
					'backgroundColor':'#ffffff', 'textAlign':'center','color':'#878E9A',
					'padding':'10px 0', 'lineHeight':'20px',
					'border':'1px solid #999', 'boxShadow':'0 0 5px #999',
					'minWidth':'100px','maxHeight':'250px','overflow':'auto',
					'border-bottom-left-radius':'5px','border-bottom-right-radius':'5px'
					});
			_div.css({'left':(_select.width()-_div.width())/2+ps.left});
		} 
		function change_div(){
			if(_div.hasClass('active')){
				_div.removeClass('active').addClass('none');
				_type1 = 0;
			}else{
				_div.removeClass('none').addClass('active');
				_type1 = 1;
			}
		}

		$(document).click(function(event){
			if(_type1 == 0){
				_div.removeClass('active').addClass('none');
			}
		});

	}
})(jQuery);