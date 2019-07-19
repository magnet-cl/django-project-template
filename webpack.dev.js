/* eslint-disable import/no-extraneous-dependencies */
const webpack = require('webpack');
const path = require('path');
const glob = require('glob');
const autoprefixer = require('autoprefixer');
const merge = require('webpack-merge');
const sass = require('sass');

const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const common = require('./webpack.common');


module.exports = merge(common, {
  mode: 'development',

  output: {
    filename: '[name].js',
    publicPath: 'http://localhost:3000/'
  },

  plugins: [
    new MiniCssExtractPlugin({
      filename: '[name].css',
      chunkFilename: '[id].css'
    }),
    new webpack.NoEmitOnErrorsPlugin(),
    new webpack.HotModuleReplacementPlugin()
  ],

  devtool: 'cheap-eval-source-map',

  devServer: {
    hot: true,
    quiet: false,
    port: 3000,
    headers: { 'Access-Control-Allow-Origin': '*' }
  },

  module: {
    rules: [
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          'css-hot-loader',
          'style-loader',
          {
            loader: 'css-loader',
            options: { sourceMap: true }
          },
          {
            loader: 'postcss-loader',
            options: {
              sourceMap: true,
              plugins: () => [autoprefixer()]
            }
          },
          {
            loader: 'sass-loader',
            options: {
              sourceMap: true,
              implementation: sass,
              includePaths: glob.sync('node_modules').map(d => path.join(__dirname, d))
            }
          }
        ]
      }
    ]
  }
});
