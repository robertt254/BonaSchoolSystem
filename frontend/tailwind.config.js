/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        school: {
          navy: '#0A192F',
          red: '#D32F2F',
          grey: '#F5F5F5',
          darkGrey: '#424242',
        }
      }
    },
  },
  plugins: [],
}
