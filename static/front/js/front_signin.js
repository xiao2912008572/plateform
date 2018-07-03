$(function () {
    $('#submit-btn').click(function (event) {
        event.preventDefault();

        var telephone_input = $("input[name='telephone']");
        var password_input = $("input[name='password']");
        var remeber_input = $("input[name='remember']");

        var telephone = telephone_input.val();
        var password = password_input.val();
        var remember = remeber_input.checked ? 1 : 0;// checked选择(True)，就返回1，没有选择(False)就返回0

        zlajax.post({
            'url': '/signin/',
            'data': {
                'telephone': telephone,
                'password': password,
                'remember': remember
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    var return_to = $("return-to-span").text();
                    if (return_to) {
                        window.location = return_to;
                    } else {
                        window.location = '/'
                    }
                } else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function () {
                console.log(data);
            }
        })
    })
});