//导航高亮
(function(){
    _tmp_path = window.location.pathname;
    _tmp_param = window.location.search.substr(1);
    _arr_path = _tmp_path.split('/page/');
    _path = _arr_path[0];
    if(_tmp_param.length>0){
        $('.navbar .nav .dropdown-menu a').each(function(){
            _href = $(this).attr('href');
            _arr_href = _href.split('?');
            if(_arr_href[1]==_tmp_param){
                $(this).parent().addClass('active');
            }else{
                $(this).parent().removeClass('active');
            }
        });
    }
})();


//赋值
function setValue(name, val){
    if(val != ""){
        var htmlType = $("[name='"+name+"']").attr("type");
        if(htmlType == "text" || htmlType == "textarea" || htmlType == "select-one" || htmlType == "hidden" || htmlType == "button"){
            $("[name='"+name+"']").val(val);
        }else if(htmlType == "radio"){
            $("input[type=radio][name='"+name+"'][value='"+val+"']").attr("checked",true);
        }else if(htmlType == "checkbox"){
            var vals = val.split(",");
            for(var i=0; i<vals.length; i++){
                $("input[type=checkbox][name='"+name+"'][value='"+vals[i]+"']").attr("checked",true);
            }
        }
    }
}

//获取多选框选中值
function getCheckboxValue(name){
    var selectVal = [];
    $("[name='"+name+"']:checked").each(function(){
      selectVal.push($(this).val());
    });
    return selectVal;
}

//绑定全选
$("#checkAll").on('click', checkAll);

//绑定全选检查
$(".check:checkbox").on('click', checkItem);

//点击行选中复选框
$('.table tbody td').on('click', checkboxSelected);

//全选
function checkAll() {
    $(".check:checkbox").attr("checked", 'checked' == $("#checkAll").attr("checked"));
}

//选中复选框
function checkboxSelected(){
    if($(this).find(":checkbox").length==0){
        var obj = $(this).parent().find(":checkbox");
        obj.attr("checked", !obj.attr('checked'));
        checkItem();
    }
}

//全选检查
function checkItem() {
    var _tmp = $(".check:checkbox");
    $('#checkAll').attr('checked', _tmp.length == _tmp.filter(':checked').length);
}

//字符串转日期
function string2date(str){
    if(null == str || str.length == 0){return;}
    return new Date(Date.parse(str.replace(/-/g,"/")));
}

//重新加载当前页面内容
function load_location(){
    load_url(window.location.href);
}

//获取url内容（table）
function load_url(url){
    $.get(url, function(data) {
        $('.table tbody').html($(data).find('.table tbody').html()).find('td').on('click', checkboxSelected);
        $('#pages').html($(data).find('#pages').html());
        $('#checkAll').attr('checked', false);
        $("html, body").animate({'scrollTop': 0}, 400);
    });
}

//go2top
$("#go-to-top").click(function(){
    $("html, body").animate({'scrollTop': 0}, 400);
    return false;
});
$(window).scroll(function() {
    var top = $(document).scrollTop();
    var g = $("#go-to-top");
    if (top > 300 && g.is(":hidden")) {
        g.fadeIn("slow");
    } else if(top < 300 && g.is(":visible")) {
        g.fadeOut();
    }
});

//全局AjaxStart&ajaxStop
$(document).ajaxStart(function () {$('#ajax-loading').show(); });
$(document).ajaxStop(function () { $('#ajax-loading').hide('slow'); });
