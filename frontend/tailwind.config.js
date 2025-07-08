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
        darkbg: '#1a1a1a',
        panelbg: '#2a2a2a',
        surfacebg: '#333333',
        borderdark: '#444444',
        borderlight: '#555555',
        'flow-grid': '#cccccc',
      },
    },
  },
  plugins: [],
}

