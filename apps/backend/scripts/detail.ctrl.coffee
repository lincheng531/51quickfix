angular
    .module('app')
    .controller('DetailCtrl', ($scope, $location, $rootScope)->
        $scope.breads = [
            {
                title: '首页',
                sref: 'app'
            },
            {
                title: '维修',
                sref: 'app.fix'
            },
            {
                title: '未接的工单',
                sref: 'app.fix.pending'
            }
        ]
        $scope.infoTable = [{
                label: '设备',
                text: '三亚的是多个'
            }, {
                label: '固定资产编号',
                text: 'sdfgesgdfgsdfg'
            }, {
                label: '故障现象',
                text: 'sdfgsergsdfg'
            }]

        $scope.images = [
            '/static/images/c1.jpg',
            '/static/images/c2.jpg',
            '/static/images/c3.jpg',
            '/static/images/c4.jpg'
        ]

        $scope.fixer = {
            screen_name: "Li Wang",
            avatar_img: '/static/images/a1.jpg',
            mobile: '18601828651'
        }

        $scope.reporter = {
            screen_name: "Mr. Bing",
            avatar_img: '/static/images/b2.jpg',
            mobile: '15925612586'
        }

        $scope.store = {
            code: '22344754'
            title: '汉堡王 江苏路店'
            number: '027-888888'
            address: '江苏路100bms'
            store_logo: '/static/images/c9.jpg'
        }

        $scope.timeline = {
            '2015-09-01': [
                {
                    label: 'Report',
                    user: 'Mr David',
                    mobile: '18721349873',
                    time: '10: 27'
                },
                {
                    label: 'Push',
                    user: 'Mr bing',
                    title: 'Chairman',
                    mobile: '18721349854',
                    time: '10: 30'
                },
                {
                    label: 'Received',
                    user: 'Mr Bang',
                    title: 'Goodman',
                    mobile: '18721349843',
                    time: '10: 40'
                },
                {
                    label: 'Got',
                    user: 'Mr Bang',
                    title: 'Goodman',
                    mobile: '18721349843',
                    time: '10: 20'
                }
            ],
            '2015-09-02': [
                {
                    label: 'Report',
                    user: 'Mr David',
                    mobile: '18721349873',
                    time: '10: 27'
                },
                {
                    label: 'Push',
                    user: 'Mr bing',
                    title: 'Chairman',
                    mobile: '18721349854',
                    time: '10: 30'
                },
                {
                    label: 'Received',
                    user: 'Mr Bang',
                    title: 'Goodman',
                    mobile: '18721349843',
                    time: '10: 40'
                },
                {
                    label: 'Got',
                    user: 'Mr Bang',
                    title: 'Goodman',
                    mobile: '18721349843',
                    time: '10: 20'
                }
            ],
            'Present': [
                {
                    text: 'charging'
                }
            ]
        }

    )
