import globals from 'globals';
import reactHooks from 'eslint-plugin-react-hooks';
import reactRefresh from 'eslint-plugin-react-refresh';

export default [
    { ignores: ['dist'] },
    {
        files: ['**/*.{js,jsx}'],
        languageOptions: {
            ecmaVersion: 2020,
            globals: globals.browser,
            parserOptions: {
                ecmaVersion: 'latest',
                ecmaFeatures: { jsx: true },
                sourceType: 'module',
            },
        },
        plugins: {
            'react-hooks': reactHooks,
             'react-refresh': reactRefresh,
            jsx: { rules: { 'uses-vars': { create(context) {
                return { JSXOpeningElement(node) {
                    const name = node.name.type === 'JSXMemberExpression' ? node.name.object.name : node.name.name;
                    if (name && /^[A-Z]/.test(name)) context.sourceCode.markVariableAsUsed(name);
                } };
            } } } },
        },
        rules: {
            ...reactHooks.configs.recommended.rules,
            'jsx/uses-vars': 'error',
            'react-refresh/only-export-components': [
                'warn',
                { allowConstantExport: true },
            ],
            'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
        },
    },
];
