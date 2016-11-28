(function ($) {
    'use strict';

    var color_list = ['accent', 'green', 'warning', 'danger', 'purple'];

    var company = {'alias': '51快修', 'logo': '/static/assets/images/logo.png'};
    // set document title
    document.title = company.alias;

    window.app = {
        name: company.alias,
        logo: company.logo,
        version: '1.0.0',
        // for chart colors
        color: {
            'primary': '#0cc2aa',
            'accent': '#a88add',
            'warn': '#fcc100',
            'info': '#6887ff',
            'success': '#6cc788',
            'warning': '#f77a99',
            'danger': '#f44455',
            'white': '#ffffff',
            'light': '#f1f2f3',
            'dark': '#2e3e4e',
            'black': '#2a2b3c'
        },
        setting: {
            theme: {
                primary: 'primary',
                accent: 'accent',
                warn: 'warn'
            },
            color: {
                primary: '#0cc2aa',
                accent: '#a88add',
                warn: '#fcc100'
            },
            folded: false,
            boxed: false,
            container: false,
            themeID: 1,
            bg: ''
        },
        color_list: color_list,
        random_color: MyUtils.getRandomVal(color_list),
        parse_menu: parse_menu,
    };

    var app = window.app;
    var setting = 'jqStorage-' + app.name + '-Setting';
    //     storage = $.localStorage;
    //
    // if (storage.isEmpty(setting)) {
    //     storage.set(setting, app.setting);
    // } else {
    //     app.setting = storage.get(setting);
    // }
    //
    // if (getParams('bg')) {
    //     app.setting.bg = getParams('bg');
    //     storage.set(setting, app.setting);
    // }

    // init
    $('body').addClass(app.setting.bg);
    app.setting.boxed && $('body').addClass('container');
    app.setting.folded && $('#aside').addClass('folded');
    setTimeout(function () {
        $('[ng-model="app.setting.folded"]').prop('checked', app.setting.folded);
        $('[ng-model="app.setting.boxed"]').prop('checked', app.setting.boxed);
        $('#settingColor input[value=' + app.setting.themeID + ']').prop('checked', 'checked');
    }, 1000);

    // folded, boxed, container
    $(document).on('change', '#settingLayout input', function (e) {
        eval($(this).attr('ng-model') + "=" + $(this).prop('checked'));
        storage.set(setting, app.setting);
        location.reload();
    });
    // color and theme
    $(document).on('click', '[ng-click]', function (e) {
        eval($(this).attr('ng-click'));
        if ($(this).find('input')) {
            app.setting.themeID = $(this).find('input').val();
        }
        storage.set(setting, app.setting);
        location.reload();
    });

    init();

    function setTheme(theme) {
        app.setting.theme = theme.theme;
        setColor();
        if (theme.url) {
            setTimeout(function () {
                var layout = theme.url.split('=');
                window.location.href = 'dashboard.' + ( layout[1] ? layout[1] + '.' : '') + 'html';
            }, 1);
        }
    };

    function setColor() {
        app.setting.color = {
            primary: getColor(app.setting.theme.primary),
            accent: getColor(app.setting.theme.accent),
            warn: getColor(app.setting.theme.warn)
        };
    };

    function getColor(name) {
        return app.color[name] ? app.color[name] : palette.find(name);
    };

    function getParams(name) {
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
            results = regex.exec(location.search);
        return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
    }

    function init() {
        //TODO
        // $('[ui-jp]').uiJp();
        // $('body').uiInclude();
    }

    function parse_menu(menus) {
        if ("undefined" == typeof menus || null == menus || menus.length == 0) {
            toastr.warning("没有可用的菜单列表");
            return;
        }
        var menu_html = [];
        var index = 0;
        $.each(menus, function (key, value) {
            var menu = value;
            if ((menu.uri == null || menu.uri == '') && (menu.parent_id == null || menu.parent_id == '')) {
                if (index > 0) {
                    menu_html.push('<li class="line dk"></li>');
                }
                menu_html.push('<li class="nav-header hidden-folded">');
                menu_html.push('<small class="text-muted">' + menu.name + '</small>');
                menu_html.push('</li>');
            } else {
                if (menu.uri == null || menu.uri == '') {
                    menu_html.push('<li>');
                    menu_html.push('<a>');
                    menu_html.push('<span class="nav-caret"><i class="fa fa-caret-down"></i></span>');
                    menu_html.push('<span class="nav-icon">');
                    menu_html.push(menu.style);
                    menu_html.push('</span>');
                    menu_html.push('<span class="nav-text">' + menu.name + '</span>');
                    menu_html.push('</a>');
                    menu_html.push('<ul class="nav-sub">');
                    // check childs exists
                    if (menu.childs && menu.childs.length > 0) {
                        $.each(menu.childs, function (k, v) {
                            menu_html.push('<li ui-sref-active="active">');
                            menu_html.push('<a href="' + v.uri + '">');
                            menu_html.push('<span class="nav-text">' + v.name + '</span>');
                            menu_html.push('</a>');
                            menu_html.push('</li>');
                        });
                    }
                    menu_html.push('</ul>');
                    menu_html.push('</li>');
                } else {
                    menu_html.push('<li ui-sref-active="active">');
                    menu_html.push('<a href="' + menu.uri + '">');
                    menu_html.push('<span class="nav-icon">' + menu.style + '</span>');
                    menu_html.push('<span class="nav-text">' + menu.name + '</span>');
                    menu_html.push('</a>');
                    menu_html.push('</li>');
                }
            }
            index++;
        });
        //menu_html.push('<li>');
        //menu_html.push('<a href="#/app/profile/form">');
        //menu_html.push('<i class="icon-user icon text-success-lter"></i>');
        //menu_html.push('<span>个人信息</span>');
        //menu_html.push('</a>');
        //menu_html.push('</li>');
        return menu_html.join("");
    }

})(jQuery);

module.exports = window.app;
