// lazyload config
(function() {
    'use strict';
    angular
      .module('app')
      .constant('MODULE_CONFIG', [
          {
              name: 'mgcrea.ngStrap',
              module: true,
              serie: true,
              files: [
                  '/static/bower_components/angular-motion/dist/angular-motion.min.css',
                  '/static/bower_components/bootstrap-additions/dist/bootstrap-additions.min.css',
                  '/static/bower_components/angular-strap/dist/angular-strap.js',
                  '/static/bower_components/angular-strap/dist/angular-strap.tpl.js'
              ]
          },
          {
              name: 'ui.bootstrap',
              module: true,
              serie: true,
              files: [
                  '/static/bower_components/angular-bootstrap/ui-bootstrap-tpls.min.js',
                  '/static/bower_components/angular-bootstrap/ui-bootstrap-tpls.js'
              ]
          },
          {
              name: 'ui.select',
              module: true,
              files: [
                  '/static/bower_components/angular-ui-select/dist/select.min.js',
                  '/static/bower_components/angular-ui-select/dist/select.min.css'
              ]
          },
          {
              name: 'vr.directives.slider',
              module: true,
              files: [
                  '/static/bower_components/angular-slider/build/angular-slider.min.js',
                  '/static/bower_components/angular-slider/angular-slider.css'
              ]
          },
          {
              name: 'angularBootstrapNavTree',
              module: true,
              files: [
                  '/static/bower_components/angular-bootstrap-nav-tree/dist/abn_tree_directive.js',
                  '/static/bower_components/angular-bootstrap-nav-tree/dist/abn_tree.css'
              ]
          },
          {
              name: 'angularFileUpload',
              module: true,
              files: [
                  '/static/bower_components/angular-file-upload/angular-file-upload.js'
              ]
          },
          {
              name: 'ngImgCrop',
              module: true,
              files: [
                  '/static/bower_components/ngImgCrop/compile/minified/ng-img-crop.js',
                  '/static/bower_components/ngImgCrop/compile/minified/ng-img-crop.css'
              ]
          },
          {
              name: 'smart-table',
              module: true,
              files: [
                  '/static/bower_components/angular-smart-table/dist/smart-table.min.js'
              ]
          },
          {
              name: 'ui.map',
              module: true,
              files: [
                  '/static/bower_components/angular-ui-map/ui-map.js'
              ]
          },
          {
              name: 'ui.grid',
              module: true,
              files: [
                  '/static/bower_components/angular-ui-grid/ui-grid.min.js',
                  './static/bower_components/angular-ui-grid/ui-grid.min.css',
                  './static/bower_components/angular-ui-grid/ui-grid.bootstrap.css'
              ]
          },
          {
              name: 'xeditable',
              module: true,
              files: [
                  '/static/bower_components/angular-xeditable/dist/js/xeditable.min.js',
                  '/static/bower_components/angular-xeditable/dist/css/xeditable.css'
              ]
          },
          {
              name: 'smart-table',
              module: true,
              files: [
                  '/static/bower_components/angular-smart-table/dist/smart-table.min.js'
              ]
          },
          {
              name:'ui.calendar',
              module: true,
              files: ['/static/bower_components/angular-ui-calendar/src/calendar.js']
          },
          {
              name:'summernote',
              module: true,
              files: [
                '/static/bower_components/summernote/dist/summernote.css',
                '/static/bower_components/summernote/dist/summernote.js',
                '/static/bower_components/angular-summernote/dist/angular-summernote.js'
              ]
          },
          {
              name: 'dataTable',
              module: false,
              files: [
                  '/static/bower_components/datatables/media/js/jquery.dataTables.min.js',
                  '/static/integration/bootstrap/3/dataTables.bootstrap.js',
                  '/static/integration/bootstrap/3/dataTables.bootstrap.css'
              ]
          },
          {
              name: 'footable',
              module: false,
              files: [
                  '/static/bower_components/footable/dist/footable.all.min.js',
                  '/static/bower_components/footable/css/footable.core.css'
              ]
          },
          {
              name: 'easyPieChart',
              module: false,
              files: [
                  '/static/bower_components/jquery.easy-pie-chart/dist/jquery.easypiechart.fill.js'
              ]
          },
          {
              name: 'sparkline',
              module: false,
              files: [
                  '/static/jquery.sparkline/dist/jquery.sparkline.retina.js'
              ]
          },
          {
              name: 'plot',
              module: false,
              files: [
                  '/static/bower_components/Flot/jquery.flot.js',
                  '/static/bower_components/Flot/jquery.flot.resize.js',
                  '/static/bower_components/Flot/jquery.flot.pie.js',
                  '/static/bower_components/flot.tooltip/js/jquery.flot.tooltip.min.js',
                  '/static/bower_components/flot-spline/js/jquery.flot.spline.min.js',
                  '/static/bower_components/flot.orderbars/js/jquery.flot.orderBars.js'
              ]
          },
          {
              name: 'vectorMap',
              module: false,
              files: [
                  '/static/bower_components/bower-jvectormap/jquery-jvectormap-1.2.2.min.js',
                  '/static/bower_components/bower-jvectormap/jquery-jvectormap.css',
                  '/static/bower_components/bower-jvectormap/jquery-jvectormap-world-mill-en.js',
                  '/static/bower_components/bower-jvectormap/jquery-jvectormap-us-aea-en.js'
              ]
          },
          {
              name: 'moment',
              module: false,
              files: [
                  '/static/bower_components/moment/moment.js'
              ]
          },
          {
              name: 'fullcalendar',
              module: false,
              files: [
                  '/static/bower_components/moment/moment.js',
                  '/static/bower_components/fullcalendar/dist/fullcalendar.min.js',
                  '/static/bower_components/fullcalendar/dist/fullcalendar.css',
                  '/static/bower_components/fullcalendar/dist/fullcalendar.theme.css'
              ]
          },
          {
              name: 'sortable',
              module: false,
              files: [
                  '/static/bower_components/html.sortable/dist/html.sortable.min.js'
              ]
          },
          {
              name: 'nestable',
              module: false,
              files: [
                  '/static/bower_components/nestable/jquery.nestable.css',
                  '/static/bower_components/nestable/jquery.nestable.js'
              ]
          },
          {
              name: 'chart',
              module: false,
              files: [
                  '/static/bower_components/echarts/build/dist/echarts-all.js',
                  '/static/bower_components/echarts/build/dist/theme.js',
                  '/static/bower_components/echarts/build/dist/jquery.echarts.js'
              ]
          }
        ]
      )
      .config(['$ocLazyLoadProvider', 'MODULE_CONFIG', function($ocLazyLoadProvider, MODULE_CONFIG) {
          $ocLazyLoadProvider.config({
              debug: false,
              events: false,
              modules: MODULE_CONFIG
          });
      }]);
})();

