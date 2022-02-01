/* eslint-disable import/no-extraneous-dependencies */
const path = require('path');

// Packages
const webpack = require('webpack');

// Plugins
const BundleTracker = require('webpack-bundle-tracker');
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

// Config
module.exports = {
  context: __dirname,

  entry: {
    main: './assets/js/index',
    status: './assets/js/status'
  },

  output: {
    path: path.resolve('./assets/bundles/')
  },

  plugins: [
    new webpack.ProvidePlugin({
      'window.jQuery': 'jquery',
      jQuery: 'jquery',
      $: 'jquery'
    }),
    new BundleTracker({
      filename: './webpack-stats.json'
    }),
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      openAnalyzer: false
    })
  ],

  optimization: {
    splitChunks: {
      cacheGroups: {
        commons: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all'
        }
      }
    }
  },

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
        exclude: /node_modules/,
        use: {
          loader: 'file-loader'
        }
      }
    ]
  },

  externals: { jquery: 'jQuery' },

  resolve: {
    modules: ['./node_modules'],
    extensions: ['*', '.js']
  }
};
