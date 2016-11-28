module.exports = {
    devTest: { //部署到测试服务器上
        remotePath: '/app/', //部署到服务器的路径
        host: '127.0.0.1', //ip地址
        user: 'root', //帐号
        pass: '', //密码
        port: 22 //端口
    },
    devDist: { //部署正式服务器上
        remotePath: '/app/', //部署到服务器的路径
        host: '127.0.0.1', //ip地址
        user: 'root', //帐号
        pass: '', //密码
        port: 22 //端口
    },
    devPort: 8003, //开发时服务器使用的端口号
    publicPath: '/merchant/', //程序在服务器的根路径地址
    target: 'http://127.0.0.1:'+this.devPort, //连接的服务器地址
}