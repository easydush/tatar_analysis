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
                            ref="text"
                            v-model="text"
                            type="textarea"
                            placeholder="Введите текст"
                            clearable
                        />
                    </el-col>
                </el-row>
                <el-row justify="end" style="margin: 20px 0">
                    <el-col :span="4">
                        <el-upload
                            ref="upload"
                            name="upload"
                            id="upload"
                            accept=".pdf,.txt,.doc,.docx"
                            :limit="1"
                            @change="handleFile"
                            :auto-upload="false"
                            :on-exceed="handleExceed"
                        >
                            <el-button type="secondary">Прикрепить файл</el-button>
                        </el-upload>
                    </el-col>
                    <el-col :span="4">
                        <el-button type="primary" @click="check(text)">Отправить</el-button>
                    </el-col>
                    <el-col :span="2"></el-col>
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
import { ElContainer, ElHeader, ElMain, ElInput, genFileId } from 'element-plus';
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
            checkFile: 'checkFile',
        }),
        check(text) {
            this.checkText(text);
        },
        handleFile(file) {
            this.$refs.text.clear();
            if (file['status'] === 'ready') this.checkFile(file.raw);
        },
        handleExceed(files) {
            this.$refs.upload?.clearFiles();
            const file = files[0];
            file.uid = genFileId();
            this.$refs.upload?.handleStart(file);
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
