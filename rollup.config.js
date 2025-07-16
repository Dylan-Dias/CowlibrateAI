// rollup.config.js
export default {
  input: 'src/main.js',  // your app entry point
  output: {
    file: 'public/bundle.js',
    format: 'iife',  // Immediately Invoked Function Expression for browsers
    name: 'app',
  },
  plugins: [
    // add plugins like svelte here if you want
  ],
};
