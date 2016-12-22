import App from '../app'

export default [
    {
        path: '/',
        component: App,
        children: [
            {
                path: '/login',
                meta: {auth: false},
                component: resolve => require(['../pages/login/'], resolve)
            },
            {
                path: '/home',
                component: resolve => require(['../pages/home/'], resolve),
                children: [
                    {
                        path: '/overview',
                        component: resolve => require(['../pages/home/overview.vue'], resolve),
                    },
                    {
                        path: '/maintenances/:type',
                        component: resolve => require(['../pages/home/maintenance-list.vue'], resolve),
                    },
                    {
                        path: '/maintenance/call',
                        component: resolve => require(['../pages/home/maintenance-call.vue'], resolve),
                    },
                    {
                        path: '/maintenance/call/users',
                        component: resolve => require(['../pages/home/maintenance-call-users.vue'], resolve),
                    },
                    {
                        path: '/maintenance/:id',
                        component: resolve => require(['../pages/home/maintenance-detail.vue'], resolve),
                    },
                ],
            },
            {
                path: '/',
                component: resolve => require(['../pages/index/'], resolve)
            },
            {
                path: '*',
                redirect: '/login'
            }
        ]
    }
]