/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#e74c3c',
        secondary: '#3498db',
        success: '#27ae60',
        danger: '#c0392b',
      },
    },
  },
  plugins: [],
}
