/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bgWhite: '#F8F9F9',
        bgGray: '#EEEEEE',
        primary: '#D6EFF8',
        mainText: '#000000',
        ligneModale: "#BDBDBD",
        startGradientLegend: '#f42a2d',
        endGradientLegend: '#3d83f5'
      },
    },
  },
  plugins: [],
}

