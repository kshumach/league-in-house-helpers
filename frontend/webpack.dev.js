/* eslint-disable @typescript-eslint/no-var-requires */
const { merge } = require('webpack-merge');
const path = require('path');
// eslint-disable-next-line import/no-extraneous-dependencies
const Dotenv = require('dotenv-webpack');
const baseConfig = require('./webpack.base');

module.exports = merge(baseConfig, {
  mode: 'development',
  devtool: 'inline-source-map',
  devServer: {
    contentBase: path.join(__dirname, 'dist'),
    contentBasePublicPath: '/',
    historyApiFallback: true,
  },
  plugins: [
    ...baseConfig.plugins,
    new Dotenv(),
  ]
});
