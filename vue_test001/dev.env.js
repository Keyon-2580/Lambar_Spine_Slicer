// 首先引入的是webpack的merge插件，该插件是用来合并对象，也就是配置文件用的，相同的选项会被覆盖，至于这里为什么多次一举，可能另有他图吧
var merge = require('webpack-merge')
// 导入prod.env.js配置文件
var prodEnv = require('./prod.env')
// 将两个配置对象合并，最终结果是 NODE_ENV: '"development"'
module.exports = merge(prodEnv, {
    NODE_ENV: '"development"'
})
new HtmlWebpackPlugin({
    filename: 'index.html',
    template: 'index.html',
    favicon:'../vue_test001/src/img/favicon.ico',
    inject: true
})
