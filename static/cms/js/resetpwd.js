// jQuery(); 等价于 $();
// 这个 $() 传入一个函数，意义是：等整个页面html、图片文件等加载完毕之后，才会执行这个传入的函数

$(function () {
    // 1. 获取`立即登录`标签：通过id=submit获取，并且绑定点击事件，点击事件里面click()再传入一个函数+变量event事件进来，就代表，点击的时候执行什么操作
    $("#submit").click(function (event) {
        // 1.1 阻止传统(默认)的表单提交方式，走js提交代码的方式
        // 是为了组织按钮默认的提交表单的事件
        event.preventDefault();

        // 1.2 获取元素
        var oldpwdE = $("input[name=oldpwd]"); //css选择器：通过input标签获取到name=oldpwd的元素
        var newpwdE = $("input[name=newpwd]"); //css选择器：通过input标签获取到name=oldpwd的元素
        var newpwd2E = $("input[name=newpwd2]"); //css选择器：通过input标签获取到name=oldpwd的元素

        // 1.3 获取元素的值
        var oldpwd = oldpwdE.val();
        var newpwd = newpwdE.val();
        var newpwd2 = newpwd2E.val();

        // 2.1 要在模板的meta标签中渲染一个csrf-token
        // 2.2 在ajax请求的头部中设置X-CSRFtoken
        zlajax.post({
            // url：路径
            'url': '/cms/resetpwd/',
            // 'url': 'https://test.yunlu6.com/api/v1/customsize_goods?limit=8',
            // data：请求数据
            'data': {
                'oldpwd': oldpwd,
                'newpwd': newpwd,
                'newpwd2': newpwd2
            },
            //  回调函数：data 是服务器返回给我们的值
            'success': function (data) {
                // console.log(data);
                // 如果code==200代表请求成功
                if (data['code'] == 200) {
                    zlalert.alertSuccessToast("恭喜！密码修改成功！");
                    // 将标签的值设置为空字符串
                    oldpwdE.val("");
                    newpwdE.val("");
                    newpwd2E.val("");
                } else {
                    var message = data['message'];
                    zlalert.alertInfo(message);
                }
            },
            'fail': function (error) {
                // console.log(error);
                // 请求失败
                zlalert.alertNetworkError();
            }
        });
    });
});