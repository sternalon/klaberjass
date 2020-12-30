var path = require("path");
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  context: __dirname,
  entry: {
          lobby: './src/components/lobby/index.jsx',
          hello: './src/components/hello/index.js',
          game: './src/components/game/index.jsx',
          card: './src/components/card/index.jsx',
    },
    output: {
      path: path.resolve('./static/bundles/'),
      filename: "[name].js"
  },

  plugins: [
    //new webpack.HotModuleReplacementPlugin(),
    //new webpack.NoErrorsPlugin(), // don't reload if there is an error
    new BundleTracker({path: __dirname, filename: './webpack-stats.json'})

  ],

  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      },
      { test: /\.css$/, use: [
          // style-loader
          { loader: 'style-loader' },
          // css-loader
          {
            loader: 'css-loader',
            options: {
              modules: true
            }
          },
        ] },
        {
            test: /\.svg$/,
            use: [
              {
                loader: 'svg-url-loader',
//                options: {
//                  limit: 10000,
//                },
              },
            ],
        },
//        {
//        test: /\.svg$/,
//        loader: 'svg-inline-loader'
//    },
    ]
  },


  resolve: {
    modules: ['node_modules'],
    extensions: ['.js', '.jsx']
  },
};