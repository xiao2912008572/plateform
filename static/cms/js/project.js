// function() 包裹在$()中，表示整个网页都加载完毕之后才会执行function中的代码
// 🌟 模态对话框保存按钮
$(function () {
    $("#save-project-btn").click(function (event) {
        event.preventDefault();
        // 先获取模态对话框的元素，效率更高
        var self = $(this);
        var dialog = $('#project-dialog');
        var nameInput = $("input[name='project_name']");
        var versionInput = $("input[name='version_code']");
        var typeInput = $("input[name='project_type']");

        var projectName = nameInput.val();
        var projectVersion = versionInput.val();
        var projectType = typeInput.val();
        // var priority = priorityInput.val();

        // 将data-type属性绑定到'保存'按钮上面：意思是提交的类型
        var submitType = self.attr('data-type');
        var projectId = self.attr('data-id');

        // 判断是否输入完整
        if (!projectName || !projectVersion || !projectType) {
            zlalert.alertInfoToast("请输入完整的项目数据！");
            return;
        }

        // 如果提交类型是更新类型
        if (submitType == 'update') {
            url = '/cms/uproject/'
        } else {
            url = '/cms/aproject/'
            // url = '/cms/'
        }
        zlajax.post({
            'url': url,
            'data': {
                'projectName': projectName,
                'projectType': projectType,
                'projectVersion': projectVersion,
                'projectID': projectId
            },
            'success': function (data) {
                // 隐藏模态对话框
                dialog.modal("hide");
                if (data['code'] == 200) {
                    zlalert.alertInfoToast('保存成功！');
                    //重新加载当前页面
                    window.location.reload();
                } else {
                    zlalert.alertInfo(data['message'])
                }
            },
            'fail': function () {
                zlalert.alertNetworkError();
            }
        })
    })
});

// 🌟 模态对话框：编辑按钮 - 更新
$(function () {
    $(".edit-project-btn").click(function (event) {
        // 0. 拿到当前对象，就是这个edit-project-btn按钮
        var self = $(this);
        event.preventDefault();
        // 1. 找到模态对话框
        var dialog = $('#project-dialog');

        // 2. 显示模态对话框
        dialog.modal('show');

        // 3. 通过edit-project-btn这个button标签的父级的父级获取到tr标签
        var tr = self.parent().parent();

        // 4. 获取相关数据，从tr标签的属性中取值
        var projectName = tr.attr("data-projectName");
        var projectVersion = tr.attr('data-projectVersion');
        var projectType = tr.attr('data-projectType');

        // 5. 取各个标签
        var nameInput = dialog.find("input[name='project_name']");
        var versionInput = dialog.find("input[name='version_code']");
        var typeInput = dialog.find("input[name='project_type']");
        var saveBtn = dialog.find("#save-project-btn");

        // 6. 将获取到的数值复制给当前的各个标签
        nameInput.val(projectName);
        versionInput.val(projectVersion);
        typeInput.val(projectType);

        // 7. 给编辑中的保存按钮绑定一个属性：data-type,属性的值为update
        // 意思是：点击了编辑之后，才绑定这个属性，说明是编辑界面的'保存'按钮
        saveBtn.attr("data-type", "update");
        saveBtn.attr("data-id", tr.attr('data-projectID'));

    })
});

// 🌟 删除
$(function () {
    $('.delete-project-btn').click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        //1. 拿到project_id
        var project_id = tr.attr('data-projectID');
        event.preventDefault();

        //2. 弹出框
        zlalert.alertConfirm({
            'msg': '您确定要删除这个项目吗?',
            // 确认删除 - 回调函数
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/dproject/',
                    'data': {
                        'projectID': project_id
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            zlalert.alertInfoToast('删除成功！');
                            //重新加载当前页面
                            window.location.reload();
                        } else {
                            zlalert.alertInfo(data['message']);
                        }
                    }
                })
            }
        })
    })
});
















