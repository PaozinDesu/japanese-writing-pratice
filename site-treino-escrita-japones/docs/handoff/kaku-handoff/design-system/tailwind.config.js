// Kaku Design System — configuração do Tailwind CSS (v3)
// Apenas aliases semânticos para a paleta padrão do Tailwind: nenhum hex arbitrário.
const colors = require('tailwindcss/colors');

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx,html}'],
  theme: {
    extend: {
      colors: {
        // 60% — dominante
        background: { DEFAULT: colors.stone[100], subtle: colors.stone[50] },
        surface: { DEFAULT: colors.white, muted: colors.stone[100], sunken: colors.stone[50], inverse: colors.stone[900] },
        // 30% — secundária
        secondary: { DEFAULT: colors.stone[900], hover: colors.stone[800], active: colors.stone[700], subtle: colors.stone[100], disabled: colors.stone[300] },
        border: { DEFAULT: colors.stone[200], strong: colors.stone[300], divider: colors.stone[200] },
        // 10% — destaque
        primary: { DEFAULT: colors.red[600], hover: colors.red[700], active: colors.red[800], subtle: colors.red[50], muted: colors.red[100], disabled: colors.red[300] },
        accent: { DEFAULT: colors.red[600], subtle: colors.red[50], muted: colors.red[100], border: colors.red[200] },
        // texto
        'text-primary': colors.stone[900],
        'text-secondary': colors.stone[700],
        'text-muted': colors.stone[600],
        'text-placeholder': colors.stone[500],
        'text-disabled': colors.stone[400],
        // status
        success: { DEFAULT: colors.green[700], bg: colors.green[100], subtle: colors.green[50], border: colors.green[200], solid: colors.green[600] },
        warning: { DEFAULT: colors.amber[800], bg: colors.amber[100], subtle: colors.amber[50], border: colors.amber[200], solid: colors.amber[600] },
        error: { DEFAULT: colors.red[700], bg: colors.red[100], subtle: colors.red[50], border: colors.red[200], solid: colors.red[600] },
        info: { DEFAULT: colors.blue[800], bg: colors.blue[100], subtle: colors.blue[50], border: colors.blue[200], solid: colors.blue[600] },
        // sistemas de escrita (sempre acompanhados de rótulo)
        hiragana: { DEFAULT: colors.blue[800], bg: colors.blue[100] },
        katakana: { DEFAULT: colors.amber[800], bg: colors.amber[100] },
        kanji: { DEFAULT: colors.red[700], bg: colors.red[100] },
      },
      fontFamily: {
        sans: ['"Zen Kaku Gothic New"', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        serif: ['"Shippori Mincho"', 'ui-serif', 'Georgia', 'serif'],
        jp: ['"Klee One"', '"Hiragino Mincho ProN"', '"Yu Mincho"', 'serif'],
      },
      maxWidth: { page: '80rem' }, // = max-w-7xl
    },
  },
  plugins: [],
};
