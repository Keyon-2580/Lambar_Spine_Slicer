module.exports = {
    // 作用很明显，就是导出一个对象，NODE_ENV是一个环境变量，指定production环境
    NODE_ENV: '"production"'
}
new HtmlWebpackPlugin({
    filename: 'index.html',
    template: 'index.html',
    favicon:'../src/img/favicon.ico',
    inject: true
})