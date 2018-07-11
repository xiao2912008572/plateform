$(function () {
    var count = 0;
    var header = $("#env_header_key" + count);
    // console.log(header);

    // 绑定点击事件
    header.click(function (event) {
        event.preventDefault();

        $('#header_from').append('<p></p><div class="form-inline form-group" id="header_from">\n' +
            '                    <input type="text" class="form-control" id="env_header_key' + count + '"  placeholder="env.env_header" style="width: 200px">\n' +
            '                    <input type="text" class="form-control" id="env_header_value" placeholder="env.env_header" style="width: 200px;margin-left: 10px">\n' +
            '                </div><p></p>');

        // 解除绑定
        // header.unbind('click');
    });
});

// 🌟 点击增加对话框
$(function () {
    $('#env_header_key').click(function (event) {
        event.preventDefault();

        $('#header_from').append("  <div class=\"form-inline form-group\" id=\"header_from\">\n" +
            "                                <input type=\"text\" class=\"form-control\" id=\"env_header_key\" placeholder=\"header-key\"\n" +
            "                                       style=\"width: 200px\">\n" +
            "                                <input type=\"text\" class=\"form-control\" id=\"env_header_value\" placeholder=\"header-value\"\n" +
            "                                       style=\"width: 200px;margin-left: 10px\">\n" +
            "                                <p></p>\n" +
            "                            </div>")
    })
});

// 🌟 点击阻止envName a标签默认事件，显示相关内容
$(function () {
    $('#envName').click(function (event) {
        event.preventDefault();
        var envID = $('#envName').attr('data-envID');
        // console.log(envID);

        zlajax.get({
            'url': '/cms/projectEnv_iframe/',
            'data': {
                'envID': envID
            },
            'success': function (data) {
                $('#env_name1').val(data['envName']);
                $('#env_desc1').val(data['envDesc']);
                $('#env_uri1').val(data['envUri']);

                // //1. 遍历env_headers
                // for (var i = 0; i < data['env_headers'].length; i++) {
                //     console.log(data['env_headers'][i]);
                // }
            }
        });
    })
});