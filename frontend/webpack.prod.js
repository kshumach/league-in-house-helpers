/* eslint-disable @typescript-eslint/no-var-requires */
const { merge } = require('webpack-merge');
// eslint-disable-next-line import/no-extraneous-dependencies
const Dotenv = require('dotenv-webpack');
const baseConfig = require('./webpack.base');

module.exports = merge(baseConfig, {
  mode: 'production',
  devtool: 'source-map',
  plugins: [...baseConfig.plugins, new Dotenv({ path: './secrets.env' })],
  optimization: {
    moduleIds: 'deterministic',
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
      },
    },
    usedExports: true,
  },
});
