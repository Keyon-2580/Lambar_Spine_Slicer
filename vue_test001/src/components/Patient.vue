<template>
    <div>
        <el-button style="margin-top: 0%" type="success"
                   icon="el-icon-refresh-left"  circle
                    @click="refresh"></el-button>
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
                            :readonly="this.readonly"
                            :rows="5"
                            placeholder="诊断结果"
                            style="font-size: 25px"
                            v-model="textarea">
                    </el-input>
                    <el-input
                            type="textarea"
                            :rows="5"
                            :readonly="this.readonly"
                            style="font-size: 25px"
                            placeholder="治疗建议"
                            v-model="textarea2">
                    </el-input>
                    <el-button @click="submit()">
                        提交病历
                    </el-button>
                    <el-button @click="edit()">
                        编辑病历
                    </el-button>
                    <el-upload
                            class="upload-demo"
                            action="https://jsonplaceholder.typicode.com/posts/"
                            ref="upload"
                            :on-remove="handleRemove"
                            :auto-upload="true"
                            :before-upload="handleUpload"
                            :on-exceed="handleExceed"
                            :on-success="uploadSuccess"
                            :on-error="uploadError"
                            :show-file-list = "true"
                            multiple
                            accept = ""
                            :limit="5"
                            :file-list="fileList">
                        <el-button size="small" type="primary" >上传CT文件</el-button>
                        <el-upload-list ref="upload_list">
                        </el-upload-list>
                        <div slot="tip" class="el-upload__tip"> 添加病人CT文件</div>
                    </el-upload>
                    <el-tag type="success">已经上传图像：{{record_slicer_file}}</el-tag>

                    <el-button size="small" type="primary"  @click="diagnosis">查看分割图像</el-button>

                </template>
            </el-main>
<!--            <img src="../assets/head.png"  style = "width:200px;, heigh:200px ;margin-left: 20%"  class ="image" />-->
        </el-container>
    </div>

</template>

<script>

    export default {
        name: "Patient",


        activated(){
            this.refresh()
            console.log("已经刷新123")
        },
        methods:{
            //刷新界面
            refresh(){
                this.axios.get("/record?patient_id=" + sessionStorage.getItem("patient_id") )
                    .then(res =>{
                        this.table = res.data
                        this.textarea = this.table[0]['record_condition']
                        this.textarea2 = this.table[0]['record_opinion']
                        this.record_slicer_file= this.table[0]['record_slicer_file']

                        console.log( this.fileList)
                    })
            },
            //上传文件
            handleUpload(file){
                let fd_file = new FormData()
                fd_file.append('file',file)
                fd_file.append("patient_id", this.table[0]['patient_id'])
                console.log(this.table[0]['patient_id'])
                this.axios.post("/postfile/",fd_file,{
                    headers:{
                        'Content-Type': 'multipart/form-data'
                    },


                }).then(res=>{
                    if(res.data.code === 200 ){
                        console.log("上传成功")
                        this.slicer_file = res.data.data

                        this.filenum += 1
                        this.$message({
                            type: 'success',
                            message: '上传成功'
                        });
                        this.refresh()
                    }else{
                        this.$message({
                            type: 'error',
                            message: '上传失败，请重新上传'
                        });
                    }
                }).catch(error => {
                    this.$message({
                        type: 'info',
                        message: '网络异常请重新上传'
                    });
                    // eslint-disable-next-line no-console
                    console.log(error);
                })

            },
            //取消上传
            handleRemove(file) {
                this.$refs.upload.abort();
                this.$message({
                    type: 'success',
                    message: '移除文件' +
                        file.name
                });

            },
            handleExceed(files, fileList) {
                this.$message.warning(`The limit is 3, you selected ${files.length} files this time, add up to ${files.length + fileList.length} totally`);
            },
            uploadSuccess(){
                this.$message({
                    type: 'success',
                    message: '上传成功'
                });
            },

            
            diagnosis(){
                if(this.record_slicer_file == ''){
                    this.$message({
                        type: 'info',
                        message: '请上传CT文件.'
                    });

                }else{
                    this.$router.push('diagnosis')
                }
            },
            submit() {
                this.readonly = true
                if (this.record_slicer_file == '') {
                    this.$message({
                        type: 'info',
                        message: '请上传CT文件并诊断.'
                    });

                } else {
                    this.record.patient_id = this.table[0]['patient_id']
                    this.record.record_slicer_file = this.record_slicer_file
                    this.record.record_condition = this.textarea
                    this.record.record_opinion = this.textarea2
                    console.log(this.record)
                    this.axios.post('/opinion/', this.record, {
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded'
                        },

                    }).then(res => {
                        if (res.data.code === 200) {
                            this.$message({
                                type: 'success',
                                message: '提交成功'
                            });
                        }
                    })
                }
            },
            edit(){
                this.readonly = false
            }



        },
        data(){
            return {
                table: [],
                patient_name: sessionStorage.getItem("patient_name"),
                textarea: '',
                textarea2: '',
                fileList: [],
                filenum: 0,
                slicer_file: '',
                record: {
                    patient_id:'',
                    record_slicer_file:'',
                    record_condition:'',
                    record_opinion:''
            },
                record_slicer_file:'',
                readonly:true
            }

        }
    }
</script>

<style scoped>
    .el-header{
        background-color: #9d09ec;
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