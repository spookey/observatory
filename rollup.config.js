import commonjs from '@rollup/plugin-commonjs';
import cssimport from 'postcss-import';
import cssprefixer from 'autoprefixer';
import cssurl from 'postcss-url';
import path from 'path';
import postcss from 'rollup-plugin-postcss';
import resolve from '@rollup/plugin-node-resolve';
import typescript from 'rollup-plugin-typescript2';
import { terser } from 'rollup-plugin-terser';

const DEVEL = [
    'dev', 'devel', 'development'
].includes(process.env.BUILD);


const assetStyle = {
  input: 'assets/style.css',
  output: {
    file: 'observatory/static/style.css',
    format: 'system',
  },
  plugins: [
    postcss({
      plugins: [
        cssimport(),
        cssurl({
          url: 'copy',
          useHash: true,
          assetsPath: 'observatory/static/fonts',
        }),
        cssurl({
          url: (asset) => path.relative('observatory/static', asset.url),
        }),
        cssprefixer(),
      ],
      extract: true,
      minimize: !DEVEL,
      sourceMap: (DEVEL ? 'inline' : false),
    }),
  ],
};


const assetScript = {
  input: 'assets/script.ts',
  output: {
    file: 'observatory/static/script.js',
    format: 'iife',
  },
  plugins: [
    resolve({
      browser: true,
    }),
    commonjs(),
    typescript(),
    (DEVEL ? null : terser()),
  ],
};


export default [
  assetStyle,
  assetScript,
];
