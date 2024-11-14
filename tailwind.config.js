/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
        "./app/templates/**/*.html",
    "./InForFit/templates/**/*.html",

    // Escanea los archivos CSS en el directorio estático para aplicar purgado de CSS
    "./app/static/css/*.css"
  ],
  theme: {
    extend: {},
  },
  plugins: [
       require('flowbite/plugin')
  ],
}

