<script src='https://cdn.jsdelivr.net/npm/imagvue@0.0.5/dist/imagvue.min.js'></script>
<template>
<div>

    <el-header>
            <h1>
                查看病人CT及处理过的模型
            </h1>
    </el-header>
    <el-container>
        <el-main>
            <h2>
                读取图像
            </h2>
            <el-row>
                <el-col  :span="8">
                    <div class="block">
                        <el-slider
                                v-model="label_0"
                                :max="this.imgnum_x"
                                style="width: 400px"
                                show-input>
                        </el-slider>
                    </div>
                </el-col>
                <el-col  :span="8">
                    <div class="block">
                        <el-slider
                                v-model="label_1"
                                :max="this.imgnum_y"
                                style="width: 400px"
                                show-input>
                        </el-slider>
                    </div>
                </el-col>
                <el-col  :span="8">
                    <div class="block">
                        <el-slider
                                v-model="label_2"
                                :max="this.imgnum_z"
                                style="width: 400px"
                                show-input>
                        </el-slider>
                    </div>
                </el-col>
            </el-row>
            <el-row>
                <el-col  :span="8">
                    <div class="block"  >
<!--                        <span class="demonstration">{{ fit }}</span>-->
<!--                        <imagvue width: 400px height: 400px-->
<!--                                v-model="'http://211.87.234.165:8888/original_files/temporary/spine1_0_x/'+ this.label_0 +'.png'" :brightness="50"></imagvue>-->
                        <el-image
                                style="width: 400px; height: 400px ;margin-right: 50%"
                                :src="'http://211.87.234.165:8888/original_files/temporary/'+this.temporary_file+'x/'+ this.label_0 +'.png'"  ></el-image>
                        <el-col :span="8">
                            <el-button  style="margin-right: 50%" type="primary" @click="readImg" >
                                读取图片
                            </el-button>
                        </el-col>
                        <el-col :span="8">
                            <template>
                                <el-select v-model="value" placeholder="选择类型">
                                    <el-option
                                            v-for="item in options"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value">
                                    </el-option>
                                </el-select>
                            </template>
                        </el-col>
                        <el-col :span="8">
                            <el-upload
                                    class="upload-demo"
                                    action="https://jsonplaceholder.typicode.com/posts/"
                                    ref="upload"
                                    :on-remove="handleRemove"
                                    :auto-upload="true"
                                    :before-upload="handleUpload"
                                    :on-success="uploadSuccess"
                                    multiple
                                    :accept = 'this.value'
                                    :limit="5"
                                    >
                                <el-button size="small" type="primary" >上传CT文件</el-button>
                                <el-upload-list ref="upload_list">
                                </el-upload-list>
                            </el-upload>
                        </el-col>
                    </div>
                </el-col>
                <el-col  :span="8">
                    <el-image
                            style="width: 400px; height: 400px ;margin-right: 50%"
                            :src="'http://211.87.234.165:8888/original_files/temporary/'+this.temporary_file+'y/'+this.label_1+'.png'"  ></el-image>
                </el-col>
                <el-col  :span="8">
                    <el-image
                            style="width: 400px; height: 400px ;margin-right: 50%"
                            :src="'http://211.87.234.165:8888/original_files/temporary/'+this.temporary_file+'z/'+this.label_2+'.png'"  ></el-image>
                </el-col>
            </el-row>
<!---->
            <el-row>
                <h2>
                    分割之后图像
                </h2>
                <el-col  :span="8">
                    <div class="block">
                        <el-slider
                                v-model="label_3"
                                :max="this.imgnum_0x"
                                style="width: 400px"
                                show-input>
                        </el-slider>
                    </div>
                </el-col>
                <el-col  :span="8">
                    <div class="block">
                        <el-slider
                                v-model="label_4"
                                :max="this.imgnum_0y"
                                style="width: 400px"
                                show-input>
                        </el-slider>
                    </div>
                </el-col>
                <el-col  :span="8">
                    <div class="block">
                        <el-slider
                                v-model="label_5"
                                :max="this.imgnum_0z"
                                style="width: 400px"
                                show-input>
                        </el-slider>
                    </div>
                </el-col>
            </el-row>
            <el-row>
                <el-col  :span="8">
                    <div class="block"  >
                        <!--                        <span class="demonstration">{{ fit }}</span>-->
                        <el-image
                                style="width: 400px; height: 400px ;margin-right: 50%"
                                :src="'http://211.87.234.165:8888/original_files/'+ this.patient_id +
                                '/sliced_file'+'x/'+this.label_3+'.png'"   ></el-image>
                        <el-button  style="margin-right: 50%" type="primary" @click="Segmentation()" >
                            分割图像
                        </el-button>
                    </div>
                </el-col>
                <el-col  :span="8">
                    <el-image
                            style="width: 400px; height: 400px ;margin-right: 50%"
                            :src="'http://211.87.234.165:8888/original_files/'+ this.patient_id +
                                '/sliced_file'+'y/'+this.label_4+'.png'"  ></el-image>
                    <el-button  style="margin-right: 50%" type="primary" @click="readSplitedImg()" >
                        读取分割图片
                    </el-button>
                </el-col>
                <el-col  :span="8">
                    <el-image
                            style="width: 400px; height: 400px ;margin-right: 50%"
                            :src="'http://211.87.234.165:8888/original_files/'+ this.patient_id +
                                '/sliced_file'+'z/'+this.label_5+'.png'"  ></el-image>
                    <el-button  style="margin-right: 50%" type="primary" @click="edit()" >
                        套索编辑
                    </el-button>
                </el-col>
            </el-row>
        </el-main>
        <el-footer>
            <el-button
                    @click = "models()"
                    type="success"
                    size = "large"
                    >
                查看模型
            </el-button>
        </el-footer>
    </el-container>
</div>
</template>

<script>

    export default {
        name: "Diagnosis",
        data() {
            return {
                patient_id:sessionStorage.getItem('patient_id'),
                label_0: 0,
                label_1: 0,
                label_2: 0,
                label_3: 0,
                label_4: 0,
                label_5: 0,
                imgnum:0,
                imgnum_x:0,
                imgnum_y:0,
                imgnum_z:0,
                imgnum_0x:0,
                imgnum_0y:0,
                imgnum_0z:0,
                options: [{
                    value: '.nii',
                    label: 'nii文件'
                }, {
                    value: '.nrrd',
                    label: 'nrrd文件'
                }, {
                    value: '.zip',
                    label: 'dicom文件'
                },{
                    value: '.gz',
                    label: 'gz文件'
                }, ],
                value:"",
                temporary_file:'0',

            }
        },

        activated(){
            readSplitedImg()
        },

        methods:{
            readImg() {
                this.$axios.post('/read_img/',  {'patient_id':sessionStorage.getItem('patient_id'),
                                                            'code':111, 'file_name':this.temporary_file},{
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded'
                        },
                        responseType: 'image/png'
                }
                ).then(res=>{
                    console.log(this.temporary_file)
                    console.log(res)
                    this.imgnum_x = res.data['x'] - 1
                    this.imgnum_y = res.data['y'] - 1
                    this.imgnum_z = res.data['z'] - 1

                })
            },
            Segmentation(){
                console.log(sessionStorage.getItem('patient_id')+'sss')
                this.$axios.post('/segmentation/', {'patient_id':sessionStorage.getItem('patient_id'),
                                            },

                ).then(res=>{
                    console.log(sessionStorage.getItem('patient_id'))
                    console.log(res)
                   if(res.data.code == 200){
                       this.$message({
                           type: 'success',
                           message: '分割成功'
                       });
                   }
                    else if(res.data.code == 500){
                        this.$message({
                            type: 'info',
                            message: '分割失败，请重新上传'
                        });
                    }


                })
            },
            //读取分割后的图像
            readSplitedImg(){
                this.$axios.post('/read_img/', {'patient_id':sessionStorage.getItem('patient_id'),
                                                                'code':222,'file_name':''
                    },{
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded'
                        },


                    }

                ).then(res=>{
                    console.log(sessionStorage.getItem('patient_id'))
                    console.log(res)
                    this.imgnum_0x = res.data['x'] - 1
                    this.imgnum_0y = res.data['y'] - 1
                    this.imgnum_0z = res.data['z'] - 1

                })
            },
            edit() {
                window.open("http://211.87.234.165:8888/taosuo/?patient_id="+sessionStorage.getItem('patient_id')
                            + '&number='+this.label_5)
            },

            handleUpload(file){
                let fd_file = new FormData()
                fd_file.append('file',file)
                fd_file.append("patient_id", sessionStorage.getItem('patient_id'))
                console.log(sessionStorage.getItem('patient_id'))
                this.axios.post("/temporaryfile/",fd_file,{
                    headers:{
                        'Content-Type': 'multipart/form-data'
                    },
                }).then(res=>{
                    if(res.data.code === 200 ){
                        console.log("上传成功")
                        this.temporary_file = res.data.data

                        this.$message({
                            type: 'success',
                            message: '上传成功'
                        });

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
            uploadSuccess(){
                this.$message({
                    type: 'success',
                    message: '上传成功'
                });
            },

            models(){
                console.log('sss0+'+sessionStorage.getItem('patient_id'))
                window.open("http://211.87.234.165:8888/models/?patient_id="+sessionStorage.getItem('patient_id'))
            }
            }
    }
</script>
<style scoped>
    .el-header, .el-footer {
        background-color: #9d09ec;
        color: #333;
        text-align: center;
        line-height: 50px;
    }

    .el-aside {
        background-color: #D3DCE6;
        color: #333;
        text-align: center;
        line-height: 20px;
        font-size: 12px;
        text-align: left;
    }

    .el-main {
        background-color: #E9EEF3;
        color: #333;
        text-align: center;
        line-height: 100px;
    }
</style>