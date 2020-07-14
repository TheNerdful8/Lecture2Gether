module.exports = {
    lintOnSave: false,
    css: {
        loaderOptions: {
            sass: {
                sassOptions: {
                    includePaths: [
                        '/home/ftsell/Projects/Lecture2Gether/lecture2gether-vue/node_modules',
                        '/home/ftsell/Projects/Lecture2Gether/lecture2gether-vue',
                    ],
                },
            },
        },
    },
    pwa: {
        themeColor: '#083358',
    },
    transpileDependencies: [
        'vuetify',
    ],

    configureWebpack: {
        devServer: {
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
                'Access-Control-Allow-Headers': 'X-Requested-With, content-type, Authorization',
            },
        },
    },
};
