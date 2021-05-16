/* eslint-disable @typescript-eslint/no-var-requires */
const { merge } = require('webpack-merge');
const { EnvironmentPlugin } = require('webpack');
const baseConfig = require('./webpack.base');

module.exports = merge(baseConfig, {
  mode: 'production',
  devtool: 'source-map',
  plugins: [...baseConfig.plugins, new EnvironmentPlugin({ NODE_ENV: 'production' })],
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
