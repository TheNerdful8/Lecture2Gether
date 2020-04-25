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
};
