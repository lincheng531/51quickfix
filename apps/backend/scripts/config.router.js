/**
 * @ngdoc function
 * @name app.config:uiRouter
 * @description
 * # Config
 * Config for the router
 */
(function () {
    'use strict';
    angular
        .module('app')
        .run(runBlock)
        .config(config)
        .constant('sys', {
            'API': 'http://www.51quickfix.com/admin'
        });

    runBlock.$inject = ['$rootScope', '$state', '$stateParams'];
    function runBlock($rootScope, $state, $stateParams) {
        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;
    }

    config.$inject = ['$stateProvider', '$urlRouterProvider', 'MODULE_CONFIG'];
    function config($stateProvider, $urlRouterProvider, MODULE_CONFIG) {

        var layout = '/static/views/layout/layout.4.html',
            dashboard = '/static/views/dashboard/dashboard.4.html';

        $urlRouterProvider
            .otherwise('/app/fix/pending');
        $stateProvider
            .state('app', {
                abstract: true,
                url: '/app',
                views: {
                    '': {
                        templateUrl: layout
                    }
                }
            })
            // Fix routers
            .state('app.fix', {
                url: '/fix',
                templateUrl: '/static/views/htmls/nav.html',
                controller: function ($scope) {
                    $scope.tabs = [
                        {
                            name: 'pending',
                            title: '未接的工单',
                            sref: 'app.fix.pending'
                        },
                        {
                            name: 'working',
                            title: '维修中工单',
                            sref: 'app.fix.working'
                        },
                        {
                            name: 'done',
                            title: '已完成工单',
                            sref: 'app.fix.done'
                        }
                    ]
                }
            })
            
            // store routers
            .state('app.store', {
                url: '/store',
                templateUrl: '/static/views/store/base.html',
            })

            .state('app.store.list', {
                url: '/store/list',
                views: {
                    store: {
                        templateUrl: '/static/views/store/list.html',
                    }
                }
            })

            .state('app.fix.search', {
                url: '/search',
                data: {title: 'Search Fix'},
                params: {search_q: null},
                views: {
                    pending: {
                        templateUrl: '/static/views/fix/datatable.html',
                        controller: function ($scope, $stateParams) {
                            $scope.search_q = $stateParams.search_q;
                        }
                    }
                }

            })

            .state('app.fix.pending', {
                url: '/pending',
                data: {title: 'Pending Fix'},
                views: {
                    pending: {
                        templateUrl: '/static/views/fix/datatable.html',
                        controller: function ($scope) {
                            $scope.status = 'pending'
                        }
                    }
                }

            }).state('app.fix.working', {
            url: '/working',
            data: {title: 'Working Fix'},
            views: {
                working: {
                    templateUrl: '/static/views/fix/datatable.html',
                    controller: function ($scope) {
                        $scope.status = 'working'
                    }
                }
            }
        }).state('app.fix.done', {
            url: '/done',
            data: {title: 'Done Fix'},
            views: {
                done: {
                    templateUrl: '/static/views/fix/datatable.html',
                    controller: function ($scope) {
                        $scope.status = 'done'
                    }
                }
            }
        })
        .state('app.fixDetail', {
            url: '/fix-detail',
            data: {title: 'Fix Detail'},
            templateUrl: '/static/views/htmls/fix-details.html',
            controller: 'DetailCtrl'
        })

        // Fee routers
            .state('app.fee', {
                url: '/fee',
                template: '<div ui-view></div>'
            })
            .state('app.fee.pending', {
                url: '/pending',
                data: {title: 'Pending Fee'},
                templateUrl: '/static/views/fix/datatable.html'
            }).state('app.fee.working', {
            url: '/working',
            data: {title: 'Working Fee'},
            templateUrl: '/static/views/fix/datatable.html'
        }).state('app.fee.done', {
            url: '/done',
            data: {title: 'Done Fee'},
            templateUrl: '/static/views/fix/datatable.html'
        })

        // Settlement routers
            .state('app.settlement', {
                url: '/settlement',
                template: '<div ui-view></div>'
            })
            .state('app.settlement.pending', {
                url: '/pending',
                data: {title: 'Pending Settlement'},
                templateUrl: '/static/views/fix/datatable.html'
            }).state('app.settlement.working', {
            url: '/working',
            data: {title: 'Working Settlement'},
            templateUrl: '/static/views/fix/datatable.html'
        }).state('app.settlement.done', {
            url: '/done',
            data: {title: 'Done Settlement'},
            templateUrl: '/static/views/fix/datatable.html'
        })

            .state('404', {
                url: '/404',
                templateUrl: '/static/views/misc/404.html'
            })

        ;

        function load(srcs, callback) {
            return {
                deps: ['$ocLazyLoad', '$q',
                    function ($ocLazyLoad, $q) {
                        var deferred = $q.defer();
                        var promise = false;
                        srcs = angular.isArray(srcs) ? srcs : srcs.split(/\s+/);
                        if (!promise) {
                            promise = deferred.promise;
                        }
                        angular.forEach(srcs, function (src) {
                            promise = promise.then(function () {
                                angular.forEach(MODULE_CONFIG, function (module) {
                                    if (module.name == src) {
                                        src = module.module ? module.name : module.files;
                                    }
                                });
                                console.log(src);
                                return $ocLazyLoad.load(src);
                            });
                        });
                        deferred.resolve();
                        return callback ? promise.then(function () {
                            return callback();
                        }) : promise;
                    }]
            }
        }

        function getParams(name) {
            name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
            var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
                results = regex.exec(location.search);
            return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
        }
    }
})();
