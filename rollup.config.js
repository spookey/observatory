import commonjs from 'rollup-plugin-commonjs';
import cssimport from 'postcss-import';
import cssprefixer from 'autoprefixer';
import json from '@rollup/plugin-json';
import postcss from 'rollup-plugin-postcss';
import resolve from 'rollup-plugin-node-resolve';
import typescript from 'rollup-plugin-typescript2';
import { terser } from 'rollup-plugin-terser';

const devel = () => [
    'dev', 'devel', 'development'
].includes(process.env.BUILD);


const assetStyle = {
  input: 'assets/style.css',
  output: {
    file: 'stats/static/style.css',
    format: 'system',
  },
  plugins: [
    postcss({
      plugins: [
        cssimport(),
        cssprefixer(),
      ],
      extract: true,
      minimize: !devel(),
      sourceMap: (devel() ? 'inline' : false),
    }),
  ],
};


const assetScript = {
  input: 'assets/script.ts',
  output: {
    file: 'stats/static/script.js',
    format: 'iife',
  },
  plugins: [
    resolve({
      browser: true,
    }),
    commonjs(),
    json(),
    typescript(),
    (devel() ? null : terser()),
  ],
};


export default [
  assetStyle,
  assetScript,
];
