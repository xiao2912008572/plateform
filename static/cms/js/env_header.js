$(function () {
    var count = 0;
    var header = $("#env_header_key" + count);
    console.log(header);

    // 绑定点击事件
    header.click(function (event) {
        event.preventDefault();
        count++;

        $('#header_from').append('<p></p><div class="form-inline form-group" id="header_from">\n' +
            '                    <input type="text" class="form-control" id="env_header_key' + count + '"  placeholder="env.env_header" style="width: 200px">\n' +
            '                    <input type="text" class="form-control" id="env_header_value" placeholder="env.env_header" style="width: 200px;margin-left: 10px">\n' +
            '                </div><p></p>');

        // 解除绑定
        // header.unbind('click');
    });
});



