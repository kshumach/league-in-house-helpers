module.exports = {
  presets: ['@babel/env', '@babel/react', '@babel/preset-typescript'],
  plugins: [
    'const-enum',
    [
      '@babel/plugin-transform-typescript',
      {
        isTSX: true,
        allExtensions: true,
        allowDeclareFields: true,
      },
    ],
    '@babel/plugin-transform-runtime',
    '@babel/plugin-proposal-nullish-coalescing-operator',
    '@babel/plugin-proposal-optional-chaining',
    [
      'babel-plugin-import',
      {
        libraryName: '@material-ui/core',
        camel2DashComponentName: false,
      },
      'core',
    ],
    [
      'babel-plugin-import',
      {
        libraryName: '@material-ui/icons',
        camel2DashComponentName: false,
      },
      'icons',
    ],
    [
      'babel-plugin-transform-imports',
      {
        '@material-ui/core': {
          preventFullImport: true,
        },
        '@material-ui/icons': {
          preventFullImport: true,
        },
      },
    ],
  ],
};
