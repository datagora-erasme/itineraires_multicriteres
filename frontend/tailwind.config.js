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
        secondary: '#0C3745',
        mainText: '#000000',
        ligneModale: "#BDBDBD",
        startGradientLegend: '#f42a2d',
        endGradientLegend: '#3d83f5',
        startGradientLegendPollen: '#C20003',
        endGradientLegendPollen: '#FEED72',
        startGradientLegendBruit: '#96CC8F',
        endGradientLegendBruit: '#845B86',
      },
    },
  },
  plugins: [],
}

