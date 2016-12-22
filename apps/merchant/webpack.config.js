const path = require('path')
const webpack = require('webpack')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const config = require('./config/')
const IS_ENV = process.env.NODE_ENV == 'production'


var plugins = []
if (IS_ENV) { //生产环境
    plugins.push(new webpack.DefinePlugin({
        'process.env': { //设置成生产环境
            NODE_ENV: 'production'
        }
    }))
    plugins.push(new webpack.optimize.UglifyJsPlugin({ //压缩代码
        compress: {
            warnings: false
        }
    }))
}

plugins.push(
    new HtmlWebpackPlugin({ //根据模板插入css/js等生成最终HTML
        filename: './index.html', //生成的html存放路径，相对于 path
        template: './src/template/index.html', //html模板路径
    })
)

plugins.push(
    new webpack.ProvidePlugin({
        $: "jquery",
        jQuery: "jquery",
        'window.jQuery': "jquery",
        tether: "tether",
        'window.Tether': "tether",
        _: "underscore",
        jqStorage: "jqStorage",
        uiLoad: "uiLoad",
        toastr: "toastr",
        moment: "moment",
        global: "global",
        MyUtils: "MyUtils",
        app: "app",
    })
)

module.exports = {
    entry: ['./src/main.js'], //编译入口文件
    output: {
        publicPath: config.publicPath, //服务器的路径
        path: path.resolve(__dirname + config.publicPath), //编译到app目录
        filename: '[name].js' //编译后的文件名
    },
    externals: {
        "window.BMap": "BMap",
    },
    module: {
        loaders: [
            {
                test: /\.js(x)*$/,
                exclude: /^node_modules$/,
                loader: 'babel'
            },
            {
                test: /\.vue$/,
                loader: 'vue'
            },
            {
                test: /\.css/,
                exclude: /^node_modules$/,
                loader: `style-loader!css-loader!autoprefixer-loader?{ browsers: ['last 100 versions'] }!`
            },
            {
                test: /\.less/,
                exclude: /^node_modules$/,
                loader: `style-loader!css-loader!autoprefixer-loader?{ browsers: ['last 100 versions'] }!less-loader`
            },
            {
                test: /\.(png|jpg)$/,
                exclude: /^node_modules$/,
                loader: 'url?limit=2000&name=[name].[ext]' //注意后面那个limit的参数，当你图片大小小于这个限制的时候，会自动启用base64编码图片
            },
            {
                test: /\.(eot|woff|svg|ttf|woff2|gif|appcache)(\?|$)/,
                exclude: /^node_modules$/,
                loader: 'file-loader?name=[name].[ext]'
            }
        ]
    },
    resolve: {
        extensions: ['', '.js', '.vue', '.jsx'], //后缀名自动补全
        alias: {
            vue: 'vue/dist/vue.js', //webpack打包时，需要设置别名
            jquery: path.resolve(__dirname, './src/libs/jquery/jquery/dist/jquery.js'),
            tether: path.resolve(__dirname, './src/libs/jquery/tether/dist/js/tether.min.js'),
            underscore: path.resolve(__dirname, './src/libs/jquery/underscore/underscore-min.js'),
            jqStorage: path.resolve(__dirname, './src/libs/jquery/jQuery-Storage-API/jquery.storageapi.min.js'),
            uiLoad: path.resolve(__dirname, './src/js/ui-load.js'),
            toastr: path.resolve(__dirname, './src/libs/jquery/toastr/toastr.min.js'),
            moment: path.resolve(__dirname, './src/libs/js/moment/moment.js'),
            global: path.resolve(__dirname, './src/config/global.js'),
            MyUtils: path.resolve(__dirname, './src/js/base.js'),
            app: path.resolve(__dirname, './src/js/app.js'),
        }
    },
    plugins,
    global: {
        MODULE_CONFIG: './js/config.lazyload.js',
        uiLoad: './js/ui-load.js',
        // import './libs/jquery/jquery.twbsPagination.js'
    },
    vue: {
        postcss: [
            require('autoprefixer')({
                browsers: ['last 100 versions']
            })
        ]
    },
    devServer: {
        historyApiFallback: true,
        hot: true,
        inline: true,
        progress: true,
        port: config.devPort,
    },
}