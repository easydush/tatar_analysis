<template>
    <div class="common-layout">
        <el-container>
            <el-header>
                <Header msg="tattext" />
            </el-header>

            <el-main>
                <el-row justify="center">
                    <el-col :span="18">
                        <el-input
                            v-model="text"
                            type="textarea"
                            placeholder="Введите текст"
                            clearable
                        />
                    </el-col>
                </el-row>
                <el-row justify="end" style="margin: 20px">
                    <el-col :span="9">
                        <el-button type="secondary" @click="check(text)">Прикрепить файл</el-button>
                        <el-button type="primary" @click="check(text)">Отправить</el-button>
                    </el-col>
                </el-row>
                <el-row
                    justify="center"
                    style="margin: 20px 0"
                    v-for="(key, value) in results"
                    :key="key"
                >
                    <el-col :span="6" :style="`text-align: left`">{{ value }}</el-col>
                    <el-col :span="16">{{ key }}</el-col>
                </el-row>
            </el-main>
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

textarea {
    height: 50vh;
}
</style>
