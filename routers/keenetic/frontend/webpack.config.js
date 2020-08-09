const path = require('path')
const VueLoaderPlugin = require('vue-loader/lib/plugin')
const HTMLWebpackPlugin = require('html-webpack-plugin')

module.exports = {
	watch: true,
	mode: "none",
	entry: path.join(__dirname, 'sources', 'router.ts'),
	output: {path: path.join(__dirname, 'build'), filename: "code.js"},
	module: {rules: [
		{test: /\.vue$/, loader: 'vue-loader'},
		{test: /\.ts$/, loader: 'ts-loader', exclude: /node_modules/, options: { appendTsSuffixTo: [/\.vue$/]}},
		{test: /\.less$/, use: [ 'vue-style-loader', {loader: 'css-loader', options: {url: false}}, 'less-loader']},
	]},
	resolve: {extensions: ['.ts', '.js', '.vue', '.json'], alias: {'vue$': 'vue/dist/vue.esm.js'}},
	plugins: [ new VueLoaderPlugin(), new HTMLWebpackPlugin({
		title: 'AURA Keenetic Router',
		template: path.join(__dirname, 'sources', 'viewport.html'),
		filename: "index.html",
		inject: 'head',
	})],
}