module.exports = {
  devServer: {
    proxy: {
        '^/api|^/media': {
            target: 'http://backend:8000',
            secure: false,
            changeOrigin: false
        }
    }
  },
  transpileDependencies: [
    "vuetify"
  ]
}

