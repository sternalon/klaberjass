var path = require("path");
//var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  context: __dirname,
  entry: {
          lobby: './src/components/lobby/index',
          hello: './src/components/hello/index',
    },
    output: {
      path: path.resolve('./static/frontend/'),
      filename: "[name].js"
  },

  plugins: [
    //new webpack.HotModuleReplacementPlugin(),
    //new webpack.NoErrorsPlugin(), // don't reload if there is an error
//    new BundleTracker({path: __dirname, filename: './webpack-stats.json'})

  ],

  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      }
    ]
  },


  resolve: {
    modules: ['node_modules'],
    extensions: ['.js', '.jsx']
  },
};