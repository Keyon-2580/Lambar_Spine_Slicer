<template>
    <div>
        <el-header>

            <h1>
                <p > {{patient_name}}的病历表</p>

            </h1>
        </el-header>
        <el-container>
            <el-main>
                <template>
                    <el-table
                            :data="table"
                            style="width: 100%">
                        <el-table-column
                                fixed
                                prop="patient_date"
                                label="日期"
                                width="150">
                        </el-table-column>
                        <el-table-column
                                prop="patient_name"
                                label="姓名"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="patient_sex"
                                label="性别"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="patient_age"
                                label="年龄"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="patient_allergy"
                                label="过敏史"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="patient_id"
                                label="编号"
                                width="120">
                        </el-table-column>
                        <el-table-column
                                prop="doctor_name"
                                label="主任医师"
                                width="300">
                        </el-table-column>
                    </el-table>
                    <el-input
                            type="textarea"
                            :rows="5"
                            placeholder="病情诊断"
                            v-model="textarea">
                    </el-input>
                    <el-input
                            type="textarea"
                            :rows="5"
                            placeholder="治疗说明"
                            v-model="textarea2">
                    </el-input>
                    <el-upload
                            class="upload-demo"
                            action="https://jsonplaceholder.typicode.com/posts/"
                            :on-preview="handlePreview"
                            :on-remove="handleRemove"
                            :before-remove="beforeRemove"
                            multiple
                            :limit="3"
                            :on-exceed="handleExceed"
                            :file-list="fileList">
                        <el-button size="small" type="primary" @click="hhh()">上传文件</el-button>
                        <div slot="tip" class="el-upload__tip"> files with a size less than 500kb</div>
                    </el-upload>
                </template>
            </el-main>
<!--            <img src="../assets/head.png"  style = "width:200px;, heigh:200px ;margin-left: 20%"  class ="image" />-->
        </el-container>
    </div>

</template>

<script>

    export default {
        name: "Patient",
        methods:{
            created(){
                //console.log('binghhhhhshi '+ sessionStorage.getItem("patient_id"))
                this.axios.get("http://127.0.0.1:8000/record?patient_id=" + sessionStorage.getItem("patient_id") )
                    .then(res =>{
                        this.table = res.data
                        console.log( res.data)

                    })

            },
            hhh(){
                console.log(this.fileList)
            }
        },
        data(){
            return{
                table:[],
                patient_name: sessionStorage.getItem("patient_name"),
                textarea: '',
                textarea2:'',
                fileList:''
            }

        }
    }
</script>

<style scoped>
    .el-header{
        background-color: #09ec91;
        color: #333;
        width: 60%;
        text-align: center;
        line-height: 50px;
        margin-right: 20%;
        margin-left: 20%;
    }
    .el-main {
        background-color: #E9EEF3;
        color: #333333;
        text-align: center;
        line-height: 100px;
        margin-right: 20%;
        margin-left: 20%;
    }
    .el-aside {
        font-size: 30px;
        background-color: #E9EEF3;
        color: #333333;
        text-align: center;
        line-height: 100px;
        margin-left: 20%;
    }
</style>