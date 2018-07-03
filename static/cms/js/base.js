/**
 * Created by Administrator on 2016/12/17.
 */

$(function () {
    $('.nav-sidebar>li>a').click(function (event) {
        var that = $(this);
        if (that.children('a').attr('href') == '#') {
            event.preventDefault();
        }
        if (that.parent().hasClass('unfold')) {
            that.parent().removeClass('unfold');
        } else {
            that.parent().addClass('unfold').siblings().removeClass('unfold');
        }
        console.log('coming....');
    });

    $('.nav-sidebar a').mouseleave(function () {
        $(this).css('text-decoration', 'none');
    });
});

// 处理菜单栏
$(function () {
    var url = window.location.href; //拿到当前页面的url

    // 1. 判断当前页面中有没有一个'profile'这样的名字
    // 2. indexOf('profile') 会返回url中profile所在的位置
    // 3. 如果2.中的位置>=0,说明profile在url中存在
    if (url.indexOf('profile') >= 0) {
        var profileLi = $('.profile-li');
        //3.1 展开下拉菜单
        profileLi.addClass('unfold').siblings().removeClass('unfold');

        //3.2 添加active样式(在css表中已经写好了红色)，并且其他兄弟(同级)元素的选中状态就会被移除掉
        profileLi.children('.subnav').children().eq(0).addClass('active').siblings().removeClass('active');
    } else if (url.indexOf('resetpwd') >= 0) {
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(1).addClass('active').siblings().removeClass('active');
    } else if (url.indexOf('resetemail') >= 0) {
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(2).addClass('active').siblings().removeClass('active');
    } else if (url.indexOf('posts') >= 0) {
        var postManageLi = $('.post-manage');
        postManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('boards') >= 0) {
        var boardManageLi = $('.board-manage');
        boardManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('permissions') >= 0) {
        var permissionManageLi = $('.permission-manage');
        permissionManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('fusers') >= 0) {
        var userManageLi = $('.user-manage');
        userManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('cusers') >= 0) {
        var cmsuserManageLi = $('.cmsuser-manage');
        cmsuserManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('croles') >= 0) {
        var cmsroleManageLi = $('.cmsrole-manage');
        cmsroleManageLi.addClass('unfold').siblings().removeClass('unfold');
    } else if (url.indexOf('comments') >= 0) {
        var commentsManageLi = $('.comments-manage');
        commentsManageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('banners')>=0){
        var bannerManagerLi = $(".banner-manage");
        bannerManagerLi.addClass('unfold').siblings().removeClass('unfold');
    }
});