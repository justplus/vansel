/**
 * Created by zhaoliang on 15/12/22.
 */
$(function(){
    $("#password").keydown(function(e){
        var curKey = e.which;
        if(curKey == 13){
            $("#login-btn").click();
            return false;
        }
    });

    $("#login-btn").click(function(){
        if($.trim($('#login-name').val())=="" || $.trim($('#password').val())==""){
            alert("用户名或密码不能为空！");
        }
        else{
            $.ajax({
                url: '/login',
                data: {'account': $.trim($('#login-name').val()), 'password': $.md5($.trim($('#password').val()))},
                type: 'POST',
                success:function(data){
                    if(data['statusCode'] != 200){
                        alert(data['msg']);
                    }
                    else{
                        window.location.href = '/';
                    }
                },
                error:function(err){
                    console.log(err);
                }
            });
        }
    });

});
