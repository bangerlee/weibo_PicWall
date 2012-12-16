$('#txtUsername').blur(function(){
    $(this).isEmpty() ? $(this).parent().parent().addClass('error') : $(this).parent().parent().removeClass('error');
    $(this).isEmail() ? $(this).parent().parent().removeClass('error') : $(this).parent().parent().addClass('error');
    if($('.error').length==0){ajaxCheck($(this).val());}
});
$('#txtPassword').blur(function(){
    $(this).isEmpty() ? $(this).parent().parent().addClass('error') : $(this).parent().parent().removeClass('error');
});
$('#txtRePassword').blur(function(){
    if($(this).isEmpty()){
        $(this).parent().parent().addClass('error');
        $(this).next().text('再次输入密码');
        return false;
    }else{
        $(this).parent().parent().removeClass('error')
    }
    if($('#txtPassword').val()!=$(this).val()){
        $(this).parent().parent().addClass('error');
        $(this).next().text('两次输入密码不一致');
    }else{
        $(this).parent().parent().removeClass('error');
        $(this).next().text('密码正确');
    }
});

$('#btnSubmit').click(function(){
    $('#txtUsername').blur();
    $('#txtPassword').blur();
    if('none'!=$('#divRePassword').css('display')){$('#txtRePassword').blur();}
    if($('.error').length>0){return false;}
    if ('注册' == $('#btnSubmit').text()){
        //console.info('注册');
        return ajaxRegister();
    }
    if ('登录' == $('#btnSubmit').text()){
        return ajaxLogin();
    }
});

//注册新用户并登录
function ajaxRegister(){
    $.ajax({
            url: '/admin/register',
            type: 'post',
            data: {
                email: $('#txtUsername').val(),
                password: $('#txtPassword').val(),
                re_password: $('#txtRePassword').val()
            },
            dataType: "json",
            success: function(data) {
                location.href='/admin?type=pic&status=2';
            }
        });
}

//登录
function ajaxLogin(){
    $.ajax({
            url: '/admin/login',
            type: 'post',
            data: {
                email: $('#txtUsername').val(),
                password: $('#txtPassword').val()
            },
            dataType: "json",
            success: function(data) {
                if(data.uid>0){
                    location.href='/admin?type=pic&status=2';
                }else{
                    $('#txtPassword').next().text(data.message);
                    $('#txtPassword').parent().parent().addClass('error');
                }
            }
        });
}

//检查Email是否已经存在
function ajaxCheck(value){
    $.ajax({
            url: '/admin/check-email',
            type: 'post',
            data: {
                email: $('#txtUsername').val()
            },
            dataType: "json",
            beforeSend: function(xhr){
                $('#btnSubmit').addClass('disabled');
            },
            success: function(data) {
                $('#btnSubmit').removeClass('disabled');
                if(!data.reg) {
                    $('#divRePassword').show('slow');
                    $('#txtUsername').next().text(data.message);
                    $('#btnSubmit').text('注册');
                }
                else {
                    if('none'!=$('#divRePassword').css('display')){
                        $('#divRePassword').hidden('slow');
                    }
                    $('#btnSubmit').text('登录');
                }
            }
        });
}
