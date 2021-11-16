/* eslint-disable import/no-extraneous-dependencies */
const glob = require('glob');
const path = require('path');

// Packages
const autoprefixer = require('autoprefixer');
const { merge } = require('webpack-merge');

// Plugins
const CSSMinimizerPlugin = require('css-minimizer-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

// Config files
const common = require('./webpack.common');

// Config
module.exports = merge(common, {
  mode: 'production',

  output: {
    filename: '[name]-[contenthash].js'
  },

  plugins: [
    new MiniCssExtractPlugin({
      filename: '[name]-[contenthash].css',
      chunkFilename: '[id]-[contenthash].css'
    }),
    new CleanWebpackPlugin()
  ],

  devtool: 'source-map',

  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin(),
      new CSSMinimizerPlugin()
    ]
  },

  module: {
    rules: [
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
            options: {
              sourceMap: true
            }
          },
          {
            loader: 'postcss-loader',
            options: {
              sourceMap: true,
              postcssOptions: {
                plugins: () => [autoprefixer()]
              }
            }
          },
          {
            loader: 'sass-loader',
            options: {
              sourceMap: true,
              sassOptions: {
                includePaths: glob.sync('node_modules').map((d) => path.join(__dirname, d))
              }
            }
          }
        ]
      }
    ]
  }
});
