const path = require('path');

module.exports = {
  entry: './src/index.jsx',
  output: { 
    path: path.resolve(__dirname, 'dist'), 
    filename: 'bundle.js',
    publicPath: '/'
  },
  module: {
    rules: [
      { 
        test: /\.jsx?$/, 
        exclude: /node_modules/, 
        use: { loader: 'babel-loader' } 
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }
    ]
  },
  resolve: { extensions: ['.js', '.jsx'] },
  devServer: { 
    static: path.join(__dirname, 'public'), 
    port: 3000, 
    historyApiFallback: true,
    hot: true
  },
};
