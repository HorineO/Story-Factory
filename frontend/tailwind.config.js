/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ['./src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#14b8a6',
        success: '#22c55e',
        warning: '#facc15',
        danger: '#ef4444',
      },
    },
  },
  plugins: [],
}

