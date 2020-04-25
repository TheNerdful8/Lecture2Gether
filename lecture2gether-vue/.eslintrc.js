module.exports = {
    root: true,
    env: {
        node: true,
    },
    extends: [
        'plugin:vue/essential',
        '@vue/airbnb',
        '@vue/typescript/recommended',
    ],
    parserOptions: {
        ecmaVersion: 2020,
    },
    rules: {
        'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
        'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
        indent: ['warn', 4, {
            FunctionExpression: { parameters: 'first' },
        }],
        quotes: ['warn', 'single'],
        'max-len': ['warn', 120],
        '@typescript-eslint/ban-ts-ignore': 'off',
    },
};
