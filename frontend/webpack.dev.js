/* eslint-disable @typescript-eslint/no-var-requires */
const { merge } = require('webpack-merge');
const path = require('path');
const { EnvironmentPlugin } = require('webpack');
const baseConfig = require('./webpack.base');

module.exports = merge(baseConfig, {
  mode: 'development',
  devtool: 'inline-source-map',
  devServer: {
    contentBase: path.join(__dirname, 'dist'),
    contentBasePublicPath: '/',
    historyApiFallback: true,
  },
  plugins: [...baseConfig.plugins, new EnvironmentPlugin({ NODE_ENV: 'development' })],
});
