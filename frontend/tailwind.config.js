/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['DM Sans', 'sans-serif'],
        heading: ['Outfit', 'sans-serif'],
      },
      colors: {
        school: {
          navy: '#0A0F1E',
          red: '#E11D48',
          grey: '#F0F4F8',
          darkGrey: '#424242',
          purple: '#6D28D9',
          'purple-l': '#7C3AED',
          'purple-ll': '#8B5CF6',
        }
      }
    },
  },
  plugins: [],
}
