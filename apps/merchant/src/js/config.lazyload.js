// lazyload config
var MODULE_PATH = '/static/';

var MODULE_CONFIG = {
    easyPieChart: [MODULE_PATH + 'libs/jquery/jquery.easy-pie-chart/dist/jquery.easypiechart.fill.js'],
    sparkline: [MODULE_PATH + 'libs/jquery/jquery.sparkline/dist/jquery.sparkline.retina.js'],
    plot: [MODULE_PATH + 'libs/jquery/flot/jquery.flot.js',
        MODULE_PATH + 'libs/jquery/flot/jquery.flot.resize.js',
        MODULE_PATH + 'libs/jquery/flot/jquery.flot.pie.js',
        MODULE_PATH + 'libs/jquery/flot.tooltip/js/jquery.flot.tooltip.min.js',
        MODULE_PATH + 'libs/jquery/flot-spline/js/jquery.flot.spline.min.js',
        MODULE_PATH + 'libs/jquery/flot.orderbars/js/jquery.flot.orderBars.js'],
    vectorMap: [MODULE_PATH + 'libs/jquery/bower-jvectormap/jquery-jvectormap-1.2.2.min.js',
        MODULE_PATH + 'libs/jquery/bower-jvectormap/jquery-jvectormap.css',
        MODULE_PATH + 'libs/jquery/bower-jvectormap/jquery-jvectormap-world-mill-en.js',
        MODULE_PATH + 'libs/jquery/bower-jvectormap/jquery-jvectormap-us-aea-en.js'],
    dataTable: [
        MODULE_PATH + 'libs/jquery/datatables/extensions/Buttons/css/buttons.bootstrap.min.css',
        MODULE_PATH + 'libs/jquery/datatables/extensions/FixedColumns/css/fixedColumns.bootstrap.min.css',
        MODULE_PATH + 'libs/jquery/datatables/extensions/FixedHeader/css/fixedHeader.bootstrap.min.css',
        MODULE_PATH + 'libs/jquery/datatables/extensions/Responsive/css/responsive.bootstrap.min.css',
        MODULE_PATH + 'libs/jquery/datatables/extensions/Select/css/select.bootstrap.min.css',
        MODULE_PATH + 'libs/jquery/datatables/datatables.js',
        MODULE_PATH + 'libs/jquery/plugins/integration/bootstrap/3/dataTables.bootstrap.js',
        MODULE_PATH + 'libs/jquery/plugins/integration/bootstrap/3/dataTables.bootstrap.css',
        MODULE_PATH + 'libs/jquery/datatables/extensions/Buttons/js/dataTables.buttons.min.js',
        MODULE_PATH + 'libs/jquery/datatables/extensions/Buttons/js/buttons.bootstrap.min.js',
        MODULE_PATH + 'libs/jquery/datatables/extensions/Buttons/js/buttons.html5.min.js',
        MODULE_PATH + 'libs/jquery/datatables/extensions/FixedColumns/js/dataTables.fixedColumns.min.js',
        MODULE_PATH + 'libs/jquery/datatables/extensions/FixedHeader/js/dataTables.fixedHeader.min.js',
        MODULE_PATH + 'libs/jquery/datatables/extensions/Responsive/js/dataTables.responsive.min.js',
        MODULE_PATH + 'libs/jquery/datatables/extensions/Select/js/dataTables.select.min.js',
    ],
    footable: [
        MODULE_PATH + 'libs/jquery/footable/dist/footable.all.min.js',
        MODULE_PATH + 'libs/jquery/footable/css/footable.core.css'
    ],
    screenfull: [
        MODULE_PATH + 'libs/jquery/screenfull/dist/screenfull.min.js'
    ],
    sortable: [
        MODULE_PATH + 'libs/jquery/html.sortable/dist/html.sortable.min.js'
    ],
    nestable: [
        MODULE_PATH + 'libs/jquery/nestable/jquery.nestable.css',
        MODULE_PATH + 'libs/jquery/nestable/jquery.nestable.js'
    ],
    summernote: [
        MODULE_PATH + 'libs/jquery/summernote/dist/summernote.css',
        MODULE_PATH + 'libs/jquery/summernote/dist/summernote.js',
        MODULE_PATH + 'libs/jquery/summernote/dist/lang/summernote-zh-CN.min.js'
    ],
    parsley: [
        MODULE_PATH + 'libs/jquery/parsleyjs/dist/parsley.css',
        MODULE_PATH + 'libs/jquery/parsleyjs/dist/parsley.min.js',
        MODULE_PATH + 'libs/jquery/parsleyjs/dist/i18n/zh_cn.js'
    ],
    select2: [
        MODULE_PATH + 'libs/jquery/select2/dist/css/select2.min.css',
        MODULE_PATH + 'libs/jquery/select2-bootstrap-theme/dist/select2-bootstrap.min.css',
        MODULE_PATH + 'libs/jquery/select2-bootstrap-theme/dist/select2-bootstrap.4.css',
        MODULE_PATH + 'libs/jquery/select2/dist/js/select2.min.js',
    ],
    datetimepicker: [
        MODULE_PATH + 'libs/js/moment/moment.js',
        MODULE_PATH + 'libs/js/datetimepicker/bootstrap-datetimepicker.js',
        MODULE_PATH + 'libs/js/datetimepicker/css/bootstrap-datetimepicker.css',
        MODULE_PATH + 'libs/js/datetimepicker/locales/bootstrap-datetimepicker.zh-CN.js',
    ],
    echarts: [
        MODULE_PATH + 'libs/js/echarts/echarts.js',
    ],
    bootstrapWizard: [
        MODULE_PATH + 'libs/jquery/twitter-bootstrap-wizard/jquery.bootstrap.wizard.min.js'
    ],
    fullCalendar: [
        MODULE_PATH + 'libs/jquery/moment/moment.js',
        MODULE_PATH + 'libs/jquery/fullcalendar/dist/fullcalendar.min.js',
        MODULE_PATH + 'libs/jquery/fullcalendar/dist/fullcalendar.css',
        MODULE_PATH + 'libs/jquery/fullcalendar/dist/fullcalendar.theme.css',
        MODULE_PATH + 'js/plugins/calendar.js'
    ],
    dropzone: [
        MODULE_PATH + 'libs/js/dropzone/dist/min/dropzone.min.js',
        MODULE_PATH + 'libs/js/dropzone/dist/min/dropzone.min.css'
    ],
    fullscreen: [
        MODULE_PATH + 'libs/jquery/fullscreen/screenfull.min.js'
    ],
    jsPDF: [
        MODULE_PATH + 'libs/jquery/jsPDF/dist/jspdf.min.js'
    ],
    jqPrint: [
        // MODULE_PATH + 'libs/jquery/print/print.js',
        MODULE_PATH + 'libs/jquery/print/print-this.js'
    ],
    fancytree: [
        MODULE_PATH + 'libs/jquery/fancytree/lib/jquery-ui.custom.js',
        MODULE_PATH + 'libs/jquery/fancytree/dist/skin-lion/ui.fancytree.css',
        MODULE_PATH + 'libs/jquery/fancytree/dist/jquery.fancytree-all.min.js',
    ],
    jqueryContextMenu: [
        MODULE_PATH + 'libs/jquery/jquery-contextMenu/jquery.ui.position.js',
        MODULE_PATH + 'libs/jquery/jquery-contextMenu/jquery.contextMenu.css',
        MODULE_PATH + 'libs/jquery/jquery-contextMenu/jquery.contextMenu.js'
    ],
    flipclock: [
        MODULE_PATH + 'libs/jquery/flipclock/dist/flipclock.css',
        MODULE_PATH + 'libs/jquery/flipclock/dist/flipclock.min.js',
    ],
    simple_timer: [
        MODULE_PATH + 'libs/jquery/flipclock/jquery.simple.timer.js',
    ],
    // start customer javascript
    main: [
        MODULE_PATH + 'js/main.js',
    ],
    flextext: [
        MODULE_PATH + 'libs/jquery/flextext/jquery.flexText.js',
        MODULE_PATH + 'libs/jquery/flextext/flextext.css'
    ],
    admin: [
        MODULE_PATH + 'js/manage/admin.js',
    ],
    deptManage: [
        MODULE_PATH + 'js/manage/dept.js',
    ],
    paper: [
        MODULE_PATH + 'js/evaluate/paper.js',
    ],
    paper2: [
        MODULE_PATH + 'js/evaluate/paper_2.js',
    ],
    paper4: [
        MODULE_PATH + 'js/evaluate/paper_4.js',
    ],
    evaluatePerson: [
        MODULE_PATH + 'js/evaluate/person.js',
    ],
    evaluateResult: [
        MODULE_PATH + 'js/evaluate/result.js',
    ],
    paperTimer: [
        MODULE_PATH + 'js/manage/paper.js',
    ],
    snapsvg: [
        MODULE_PATH + 'libs/snap/snap.svg.js',
    ],
    jqueryform: [
        MODULE_PATH + 'libs/jquery/jquery.form.js'
    ],
    weeklypaper: [
        MODULE_PATH + 'js/weeklypaper/weeklypaper.js',
    ],
    atwho: [
        MODULE_PATH + 'libs/js/caret/js/jquery.caret.js',
        MODULE_PATH + 'libs/js/atwho/js/jquery.atwho.js',
        MODULE_PATH + 'libs/js/atwho/css/jquery.atwho.css'
    ],
    todo: [
        MODULE_PATH + 'libs/js/moment/moment.js',
        MODULE_PATH + 'libs/js/moment/locale/zh-cn.js',
        MODULE_PATH + 'js/todo/todo.js',
        MODULE_PATH + 'libs/vue/Sortable.js',
        MODULE_PATH + 'libs/jquery/html.sortable/dist/jquery.sortable.js',
        MODULE_PATH + 'libs/vue/vue-sortable.js',
    ],
    punchcard:[
        MODULE_PATH + 'js/punchcard/punchcard.js'
    ],
    profile: [
        MODULE_PATH + 'js/user/profile.js',
        MODULE_PATH + 'libs/cropper/cropper.js',
        MODULE_PATH + 'libs/cropper/cropper.css',
    ],
    directive: [
        MODULE_PATH + 'js/vue_directives.js',
    ],
    messageComponent: [
        MODULE_PATH + 'js/components/message.js',
    ],
    message: [
        MODULE_PATH + 'js/user/message.js',
    ],
    bootstrap_daterangepicker: [
        MODULE_PATH + 'libs/bootstrap-daterangepicker/moment.js',
        MODULE_PATH + 'libs/bootstrap-daterangepicker/daterangepicker.js',
        MODULE_PATH + 'libs/bootstrap-daterangepicker/daterangepicker.css',
    ],
    todo_analysis: [
        MODULE_PATH + 'js/user/todo_analysis.js',
    ],
    my_feedback: [
        MODULE_PATH + 'js/user/feedback.js',
    ],
    market_feedback: [
        MODULE_PATH + 'js/market/feedback.js',
    ],
    twbspagination: [
        MODULE_PATH + 'libs/jquery.twbsPagination.js',
    ],
    // end customer javascript
};

module.exports = MODULE_CONFIG;