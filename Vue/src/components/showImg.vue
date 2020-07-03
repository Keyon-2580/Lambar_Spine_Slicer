<template>
    <div>
        <el-button @click="c1">查看原始图像</el-button>
        <el-button @click="c2">查看预测结果</el-button>
        <el-button @click="test"></el-button>
        <el-dialog title="选择图像处理方式" :visible.sync="digvis">
            <el-select v-model="value4" placeholder="请选择" @change="selectch">
                <el-option
                        v-for="item in options"
                        :key="item.value"
                        :value="item.value"
                        :label="item.label"
                >
                </el-option>
            </el-select>
            <div slot="footer">
                <el-button @click="digclick">确定</el-button>

            </div>
        </el-dialog>
        <el-table
                :data="tableData"
                style="width: 100%"
                :row-class-name="tableRowClassName"
                @row-click="handleclick">
            <el-table-column
                    label=""
                    width="500">
                <template slot-scope="scope">
                    <img :src="scope.row.img" />
                </template>
            </el-table-column>
            <el-table-column
                    label=""
                    width="500">
                <template slot-scope="scope">
                    <img :src="scope.row.img1"/>
                </template>
            </el-table-column>

        </el-table>

    </div>

</template>

<script>

    export default
    {
        name : "ImageShow",
        props : ["msg"],
        data()
        {
            return {ln : "", tableData : [],
                options : [{value:"1", label:"1"}, {value:"2", label:"2"}, {value:"3", label:"3"},{value:"4",label:"4"}], value4 : "1", digvis : false, isse : 1, selrow : 0}
        },

        created : function()
        {
            /*
            this.$axios.get('apis/ajax/data?id=' + this.msg).then(function(r)
            {
            })
            */
        },
        methods :
            {
                c1()
                {
                    //var temp = []
                    var t = this
                    console.log(this.msg)
                    this.$axios.get('ajax/data/?id=' + this.msg).then(function(r)
                    {
                        console.log("yes")
                        var i = 0
                        var temp = []
                        var l = r.data.imgs.length
                        for(; i < l; ++i)
                        {
                            var t1 = new Array()
                            t1['img'] = "http://211.87.234.165:9988/" + r.data.imgs[i]
                            temp.push(t1)
                        }
                        t.tableData = temp
                        console.log("length" + t.tableData.length)
                        t.ln = r.data.label_names
                        console.log(t.ln)
                    })
                },

                test()
                {
                    console.log("test")
                    this.tableData.push({img : "http://211.87.234.165:9988/media/1592190984.5149817.png"})
                    this.tableData.push({img : "https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1592189663&di=74710b06b56db95d71bb0e9a4e0d7f5e&src=http://ztd00.photos.bdimg.com/ztd/w=700;q=50/sign=0dc763f872cb0a46852289395b588719/c8177f3e6709c93d71fb8ff5963df8dcd10054a2.jpg"})

                },

                c2()
                {
                   // var temp = []
                    var t = this
                    console.log("NO")
                    this.$axios.get('ajax/label/?file_id='+this.msg + '&label_name=' + this.ln).then(function(r)
                    {
                        console.log("yes")
                        var i = 0
                        var l = t.tableData.length
                        var temp = []
                        for(; i < l; ++i)
                        {
                            var t1 = new Array()
                            t1['img'] = t.tableData[i].img
                            t1['img1'] = "http://211.87.234.165:9988/" + r.data.imgs[i]
                            temp.push(t1)
                        }
                        t.tableData = temp
                    })
                },

                tableRowClassName({row, rowIndex})
                {
                    row.index = rowIndex
                },

                // handleclick(r, c, e)
                // {
                //     this.digvis = true
                //     this.selrow = r.index
                // },
                //
                // selectch(e, p)
                // {
                //     this.isse = e
                // },

                digclick()
                {
                    var l = this.tableData[this.selrow].img
                    this.digvis = false
                    console.log(l)
                    var t = l.substring(l.indexOf("/", l.indexOf("/" ,l.indexOf("/") + 1) + 1) + 1)
                    var u = "ajax/pro/?name=" + t + "&type=" + this.isse
                    var t1 = this
                    this.$axios.get(u).then(function(r)
                    {
                        console.log(r.data.new_name)
                        var ttt1 = "http://211.87.234.165:9988/" + r.data.new_name
                        t1.$set(t1.tableData, t1.selrow,  {img : ttt1})
                        //t1.tableData.push({img : ttt1})
                        console.log(ttt1)
                        //tableData[t1.selrow].splice(0, 1, ttt1)
                    })
                    this.tableData.push({img : "https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1592189663&di=74710b06b56db95d71bb0e9a4e0d7f5e&src=http://ztd00.photos.bdimg.com/ztd/w=700;q=50/sign=0dc763f872cb0a46852289395b588719/c8177f3e6709c93d71fb8ff5963df8dcd10054a2.jpg"})
                    console.log(this.tableData.length)
                    //this.tableData.push({img : "http://211.87.234.165:9988/media/1592190984.5149817.png"})

                    this.tableData.push({img : "https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1592189663&di=74710b06b56db95d71bb0e9a4e0d7f5e&src=http://ztd00.photos.bdimg.com/ztd/w=700;q=50/sign=0dc763f872cb0a46852289395b588719/c8177f3e6709c93d71fb8ff5963df8dcd10054a2.jpg"})
                    console.log(this.tableData.length)
                    console.log("####################################")

                }

            }
    }

</script>
