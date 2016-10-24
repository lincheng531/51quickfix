(function($) {
	$.fn.ksearch = function(f1) {
		var _select	 = this;
		var _ul = _select.children('ul');

		_ul.children('li').each(function(index, item){
			$(this).append(' <img src="/static/images/icon_close.png" class="close">')
		})	
		_ul.children('li').each(function(index, item){
			var li = $(this);
			var name = li.attr('name')
			$(this).children('.close').click(function(){
				$.when(li.remove()).then(f1(undefined, undefined, name));
			})
		})


	}
})(jQuery);