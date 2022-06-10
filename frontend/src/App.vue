<template>
    <div class="common-layout">
        <el-container>
            <el-header>
                <Header msg="tattext" />
            </el-header>

            <el-main>
                <el-input
                    v-model="input"
                    autosize
                    type="textarea"
                    placeholder="Введите текст"
                    clearable
                />
            </el-main>

            <el-row class="mb-4" justify="end">
                <el-button type="primary">Отправить</el-button>
            </el-row>
        </el-container>
    </div>
</template>

<script>
import { ElContainer, ElHeader, ElMain, ElInput } from 'element-plus';
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
            input: null,
        };
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
