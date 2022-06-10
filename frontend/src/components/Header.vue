<template>
    <div class="header">
        <el-row class="row-bg" justify="space-between">
            <el-col :span="6">
                <img alt="tulip logo" src="../assets/logo.png" />
                <span :style="`font-size: var(--el-font-size-extra-large);`">
                    {{ msg }}
                </span>
            </el-col>
        </el-row>
    </div>
</template>

<script>
export default {
    name: 'HeaderComponent',
    props: {
        msg: String,
    },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
    margin: 40px 0 0;
}

ul {
    list-style-type: none;
    padding: 0;
}

li {
    display: inline-block;
    margin: 0 10px;
}

a {
    color: #42b983;
}
</style>
