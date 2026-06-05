import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'Landing',
        component: () => import('@/views/LandingView.vue'),
        meta: { title: '城市名片' }
    },
    {
        path: '/home',
        name: 'Home',
        component: () => import('@/views/HomeView.vue'),
        meta: { title: '首页概览' }
    },
    {
        path: '/population',
        name: 'Population',
        component: () => import('@/views/PopulationView.vue'),
        meta: { title: '人口分布' }
    },
    {
        path: '/economy',
        name: 'Economy',
        component: () => import('@/views/EconomyView.vue'),
        meta: { title: '经济产业' }
    },
    {
        path: '/tourism',
        name: 'Tourism',
        component: () => import('@/views/TourismView.vue'),
        meta: { title: '文化旅游' }
    },
    {
        path: '/meizhou',
        name: 'Meizhou',
        component: () => import('@/views/MeizhouView.vue'),
        meta: { title: '走进湄洲岛' }
    },
    {
        path: '/environment',
        name: 'Environment',
        component: () => import('@/views/EnvironmentView.vue'),
        meta: { title: '生态环境' }
    },
    {
        path: '/transport',
        name: 'Transport',
        component: () => import('@/views/TransportView.vue'),
        meta: { title: '交通概况' }
    },
    {
        path: '/service',
        name: 'Service',
        component: () => import('@/views/ServiceView.vue'),
        meta: { title: '公共服务' }
    },
    {
        path: '/yearbook',
        name: 'Yearbook',
        component: () => import('@/views/YearbookView.vue'),
        meta: { title: '统计年鉴' }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// 路由守卫 - 更新页面标题
router.beforeEach((to, from, next) => {
    document.title = `${to.meta.title || '莆田市市情'} - 莆田市市情WebGIS系统`
    next()
})

export default router
