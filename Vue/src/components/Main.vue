<script src="../main.js"></script>
<template>
    <div>
        <el-header style="margin-top: 0px; ">
<!--            <img src="../assets/hhh.jpg"  style = "width:200px;, heigh:200px"  class ="image" />-->
            <h1>
                腰椎分割诊断系统
            </h1>
            <el-button
                    @click = "refresh()"
                    type="success"
                    size = "small"
                    style="margin-right: 500px">
                刷新</el-button>
            <el-button
                    @click="dialogFormVisible = true; "
                    type="primary"
                    size = "small"
                    round>
                添加病人</el-button>
        </el-header>
        <el-container style="margin-top: 100px">
        <el-aside style=" width:200px">
            <img src="../assets/head.png"  style = "width:200px;, heigh:200px"  class ="image" />
            <h2>ID：{{doctor_id}}</h2>
            <h2>姓名：{{doctor_name}}</h2>
            <h2>性别：{{sex}}</h2>
            <h2>部门：{{department}}</h2>
            <h2>职位：{{job}}</h2>
            <h2>联系方式：{{tel}}</h2>
        </el-aside>
        <el-main>
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
                <el-table-column
                        label="操作"
                        width="300">
                    <template slot-scope="scope">
                        <el-button
                                @click = "open(scope.$index, scope.row)"
                                type="danger"
                                size = "small">
                            删除</el-button>
                        <el-button
                                type="warning"
                                size ="small"
                                @click="checkPatient(scope.$index, scope.row)">
                            查看</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-main>
            <el-dialog title="添加病人" :visible.sync="dialogFormVisible" >
                <el-form :model="form" :rules="rules"  ref="form">
                    <el-form-item label="姓名" :label-width="formLabelWidth" prop="name">
                        <el-input v-model="form.name" style="width: 220px" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="性别" :label-width="formLabelWidth" prop="sex">
                        <el-select v-model="form.sex" placeholder="请选择性别">
                            <el-option label="男" value="男"></el-option>
                            <el-option label="女" value="女"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="年龄" :label-width="formLabelWidth" prop="age">
                        <el-select v-model="form.age" placeholder="请选择年龄">
                            <el-option
                                    v-for="item in 90"
                                    :key = "item"
                                    :value="item"
                                    :disabled="item.disabled">
                            </el-option>
                        </el-select>
                        </el-form-item>
                    <el-form-item label="出生日期" :label-width="formLabelWidth" prop="born">
                        <div class="block">
                            <span class="demonstration"></span>
                            <el-date-picker
                                    v-model=form.born
                                    type="date"
                                    placeholder="选择日期">
                            </el-date-picker>
                        </div>
                    </el-form-item>
                    <el-form-item label="民族" :label-width="formLabelWidth" prop="nation">
                        <el-input v-model="form.nation" style="width: 220px" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="职业" :label-width="formLabelWidth" prop="job">
                        <el-input v-model="form.job"  style="width: 220px" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="住址" :label-width="formLabelWidth" prop="address">
                        <el-input v-model="form.address" style="width: 220px" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="过敏史" :label-width="formLabelWidth" @keydown.enter.native="add_patient" prop="allergy">
                        <el-input v-model="form.allergy" style="width: 300px" autocomplete="off"></el-input>
                    </el-form-item>
<!--                    <el-form-item label="医生ID" :label-width="formLabelWidth">-->
<!--                        <el-input v-model="form.doc_id" style="width: 220px"  autocomplete="off" ></el-input>-->
<!--                    </el-form-item>-->
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="dialogFormVisible = false; resetForm('form')" >取 消</el-button>
                    <el-button type="primary" @click="dialogFormVisible = false; add_patient()">确 定</el-button>
                </div>
            </el-dialog>
        </el-container>
    </div>
</template>

<script>
    export default {
        name:"Main",
        created(){
            this.refresh()
        },
        methods: {
            handleDelete(index,row){
                console.log('patient_id 是', row['patient_id'])
                this.axios.get("/delete?patient_id=" + row.patient_id)
                    .then(res =>{
                        console.log(res)
                        this.refresh()
                    })
                console.log(index,row)
            },
            checkPatient(index, row){
                sessionStorage.removeItem('patient_id', row.patient_id)
                sessionStorage.setItem('patient_id', row.patient_id);
                sessionStorage.setItem('patient_name', row.patient_name);
                sessionStorage.setItem('patient_sex', row.patient_sex);
                sessionStorage.setItem('patient_age', row.patient_age);
                sessionStorage.setItem('patient_date', row.patient_date);
                sessionStorage.setItem('patient_nation', row.patient_nation);
                sessionStorage.setItem('patient_address', row.patient_address);
                sessionStorage.setItem('patient_job', row.patient_job);
                sessionStorage.setItem('patient_allergy', row.patient_allergy);
                console.log("bingrenshi :" + sessionStorage.getItem('patient_name'))
                this.$router.push('patient')
            },
            refresh(){
                this.axios.get("/refresh?doctor_id=" + sessionStorage.getItem("doctor_id") )
                    .then(res =>{
                        console.log(res.data),
                        this.table = res.data
                    })
            },
            add_patient(){
                this.form['doc_id'] = sessionStorage.getItem('doctor_id')
                this.axios.post("/add_patient/" ,this.form,{
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },

                }).then(res=> {
                    if(res.data.code === 200){
                        this.form={brand_right:0}
                        console.log(res);
                        this.refresh();
                        this.$message({
                            type: 'success',
                            message: '新建成功'
                        });
                        resetForm(this.form)
                        {
                            this.$refs[this.form].resetFields();
                        }
                    }else{
                        this.$message({
                            type: 'info',
                            message: '创建失败'
                        });
                        resetForm(this.form)
                        {
                            this.$refs[this.form].resetFields();
                        }
                    }

                }).catch(function (error) {
                        console.log(error);
                    });
            },

            resetForm(form) {
                this.$refs[form].resetFields();
            },
            open(index,row) {
                this.$confirm('This will permanently delete the file. Continue?', 'Warning', {
                    confirmButtonText: 'OK',
                    cancelButtonText: 'Cancel',
                    type: 'warning'
                }).then(() => {
                    this.handleDelete(index,row)
                    this.$message({
                        type: 'success',
                        message: '删除成功'

                    });
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '取消删除'
                    });
                });
            }
        },

        data() {
            return {
                table:[],
                doctor_name:sessionStorage.getItem("user_name"),
                sex:sessionStorage.getItem('sex'),
                tel:sessionStorage.getItem('tel'),
                department:sessionStorage.getItem('department'),
                job:sessionStorage.getItem('job'),
                doctor_id:sessionStorage.getItem('doctor_id'),
                dialogFormVisible:false,
                form: {
                    doc_id: '',
                    name: '',
                    sex: '',
                    date1: '',
                    date2: '',
                    age: '',
                    nation: '',
                    address: '',
                    born: '',
                    job: '',
                    allergy: '',
                },
                rules: {
                    name: [{ required: true, message: 'Please input Activity name', trigger: 'blur' }],
                    sex: [{ required: true, message: 'Please input Activity sex', trigger: 'blur' }],
                    nation: [{ required: true, message: 'Please input Activity nation', trigger: 'blur' }],
                    age: [{ required: true, message: 'Please input Activity age', trigger: 'blur' }],
                    address: [{ required: true, message: 'Please input Activity address', trigger: 'blur' }],
                    born: [{ required: true, message: 'Please input Activity born', trigger: 'blur' }],
                    job: [{ required: true, message: 'Please input Activity job', trigger: 'blur' }],
                    allergy: [{ required: true, message: 'Please input Activity allergy', trigger: 'blur' }],
                },
                formLabelWidth: '120px'
            }
        }
    }
</script>
<style>
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