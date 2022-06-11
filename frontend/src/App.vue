<template>
    <div class="common-layout">
        <el-container>
            <el-header>
                <Header msg="tattext" />
            </el-header>

            <el-main>
                <el-input
                    v-model="text"
                    autosize
                    type="textarea"
                    placeholder="Введите текст"
                    clearable
                />
            </el-main>

            <el-row class="mb-4" justify="end">
                <el-button type="primary" @click="check(text)">Отправить</el-button>
            </el-row>
        </el-container>
    </div>
</template>

<script>
import { ElContainer, ElHeader, ElMain, ElInput } from 'element-plus';
import { mapActions, mapGetters } from 'vuex';
import HeaderComponent from './components/Header';

export default {
    name: 'App',
    components: {
        ElContainer,
        ElHeader,
        ElMain,
        ElInput,
        Header: HeaderComponent,
    },
    data() {
        return {
            text: null,
        };
    },
    computed: {
        ...mapGetters(['results']),
    },
    methods: {
        ...mapActions({
            checkText: 'checkText',
        }),
        check(text) {
            this.checkText(text);
        },
    },
};
</script>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
}
</style>
