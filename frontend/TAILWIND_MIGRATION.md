# Tailwind Migration Guide

This project has migrated from component-scoped CSS files to Tailwind CSS utilities.

## Setup Summary

1. Installed `tailwindcss@3`, `postcss`, `autoprefixer` as dev dependencies.
2. Generated `tailwind.config.js` and `postcss.config.js` using `npx tailwindcss init -p`.
3. Added Tailwind directives at the top of `src/styles/index.css`:
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```
4. Configured content paths in `tailwind.config.js`:
   ```js
   module.exports = {
     content: ["./src/**/*.{js,jsx}"],
     theme: { extend: {} },
     plugins: [],
   };
   ```

## Component Guidelines

• Prefer inline utility classes for layout, spacing, colors, and states.
• Use conditional `className` strings or libraries like `clsx` when classes depend on props/state.
• For shared patterns, extract small React components rather than global CSS.
• Keep **all** old CSS imports commented (`// import './xxx.css'`) until fully removed.

## Theming

To customize colors, spacing, etc., edit `tailwind.config.js` under `theme.extend`:

```js
extend: {
  colors: {
    primary: '#14b8a6',
  },
  spacing: {
    '128': '32rem',
  },
}
```

## Plugins

If you need scrollbars, forms, or typography utilities, install official plugins, e.g.:

```
npm i -D @tailwindcss/forms
```

And add to `plugins` array.

## Purge & Build

`react-scripts build` or `npm run build` will tree-shake unused classes automatically via Tailwind JIT.

---

Happy hacking with Tailwind!
