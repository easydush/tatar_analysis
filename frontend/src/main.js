import { createApp } from 'vue';
import App from './App.vue';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import Vuex from 'vuex';
import axios from 'axios';

const app = createApp(App);
const store = new Vuex.Store({
    state: {
        results: {},
    },
    actions: {
        // eslint-disable-next-line no-unused-vars
        checkText: function ({ commit }, text) {
            axios.post(`http://localhost:8000/check/`, text).then(
                (response) => {
                    commit('SET_RESULTS', { results: response.data });
                },
                (err) => {
                    console.log(err);
                },
            );
        },
    },
    mutations: {
        SET_RESULTS: (state, { results }) => {
            state.results = results;
        },
    },
    getters: {
        results: (state) => {
            return state.results;
        },
    },
});

app.use(store);
app.use(ElementPlus);
app.mount('#app');
