;(function($) {
    var cache = [];
    // Arguments are image paths relative to the current page.
    $.preLoadImages = function() {
        var args_len = arguments.length;
        for (var i = args_len; i--;) {
            var cacheImage = new Image();
            cacheImage.src = arguments[i];
            cache.push(cacheImage);
        }
    }
})(jQuery);

function perload_next_page_img(next_page){
    $.ajax({
        url: '/preload/page/'+next_page,
        type: 'get',
        data: {},
        dataType: "json",
        success: function(data) {
            list = data.data.split(",");
            for(i=0; i<list.length; i++){
                $.preLoadImages(list[i]);
            }
        }
    });
}
