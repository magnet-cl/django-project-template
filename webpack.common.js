/* eslint-disable import/no-extraneous-dependencies */
const webpack = require('webpack');

const BundleTracker = require('webpack-bundle-tracker');
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

const path = require('path');

module.exports = {
  context: __dirname,
  entry: './assets/js/index',

  output: {
    path: path.resolve('./assets/bundles/')
  },

  plugins: [
    new webpack.ProvidePlugin({
      'window.jQuery': 'jquery',
      jQuery: 'jquery',
      $: 'jquery'
    }),
    new BundleTracker({ filename: './webpack-stats.json' }),
    new BundleAnalyzerPlugin({ analyzerMode: 'assets', openAnalyzer: false })
  ],

  module: {
    rules: [
      {
        test: /\.m?js$/,
        include: path.resolve('./assets/js'),
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      },
      {
        test: /.(jpg|png|woff(2)?|eot|ttf|svg)$/,
        loader: 'file-loader'
      }
    ]
  },

  externals: { jquery: 'jQuery' },

  resolve: {
    modules: ['./node_modules'],
    extensions: ['*', '.js']
  }
};
