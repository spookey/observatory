import commonjs from '@rollup/plugin-commonjs';
import cssdiscard from 'postcss-discard-comments';
import cssimport from 'postcss-import';
import cssprefixer from 'autoprefixer';
import cssurl from 'postcss-url';
import path from 'path';
import postcss from 'rollup-plugin-postcss';
import resolve from '@rollup/plugin-node-resolve';
import typescript from 'rollup-plugin-typescript2';
import { terser } from 'rollup-plugin-terser';

const DEVEL = process.env.BUILD === 'dev';
const VIEW = process.env.TARGET === 'view';
const CODE = process.env.TARGET === 'code';
const _ALL = (!VIEW && !CODE);

const NODE_M = path.normalize(path.join(
  __dirname, 'node_modules'
));
const ASSETS = path.normalize(path.join(
  __dirname, 'assets'
));
const STATIC = path.normalize(path.join(
  __dirname, 'observatory', 'static'
));


const assetView = {
  input: path.join(ASSETS, 'style.scss'),
  output: {
    file: path.join(STATIC, 'style.css'),
    format: 'system',
  },
  plugins: [
    postcss({
      plugins: [
        cssimport(),
        cssurl({
          url: 'copy',
          useHash: true,
          basePath: [
            path.join(NODE_M, 'remixicon', 'fonts'),
            path.join(NODE_M, 'source-code-pro'),
            path.join(NODE_M, 'source-sans-pro'),
          ],
          assetsPath: path.join(STATIC, 'fonts'),
        }),
        cssurl({
          url: (asset) => path.relative(STATIC, path.join(NODE_M, asset.url)),
        }),
        cssprefixer(),
        cssdiscard({
          removeAll: true,
        }),
      ],
      extract: true,
      minimize: !DEVEL,
      sourceMap: (DEVEL ? 'inline' : false),
    }),
  ],
};


const assetCode = {
  input: path.join(ASSETS, 'script.ts'),
  output: {
    file: path.join(STATIC, 'script.js'),
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


const jobs = [];
if (VIEW || _ALL) { jobs.push(assetView); }
if (CODE || _ALL) { jobs.push(assetCode); }
export default jobs;
