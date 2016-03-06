var ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
    entry: {
        app: [
            './src/static/app.js'
        ],
    },
    output: {
        path: './src/static',
        filename: 'bundle.js'
    },
    node: {
        child_process: 'empty',
        global: false
    },
    module: {
      loaders: [
            {
                test: /\.css$/,
                loader: ExtractTextPlugin.extract("style-loader", "css-loader")
            }
        ]
    },
    plugins: [
        new ExtractTextPlugin('style.css', {
            allChunks: true
        })
    ]
};
