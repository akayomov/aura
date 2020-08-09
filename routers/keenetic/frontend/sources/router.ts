import './design.less'
import Vue from 'vue';
import VueX, {Store} from 'vuex';
import VueRouter from 'vue-router';
import routerConfig from "./store";

import Dashboard from './views/dashboard.vue';
import TestComponents from "./views/test_components.vue";

document.addEventListener("DOMContentLoaded", () => {
    const body = document.getElementsByTagName('body')[0]
    body.innerHTML = "<div id=\"application\"><router-view></router-view></div>"

    Vue.use(VueRouter)
    Vue.use(VueX)

    document.application = new Vue({
        router: new VueRouter({
            routes: [
                {path: '/', component: Dashboard},
                {path: '/ui-test', component: TestComponents},
            ]
        }), store: new Store(routerConfig)
    }).$mount('div#application')
    console.log("Vue Initialized")
});
