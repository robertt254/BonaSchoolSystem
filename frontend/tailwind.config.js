/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans:    ['DM Sans', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        heading: ['DM Sans', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },

      colors: {
        // Brand (violet)
        brand: {
          DEFAULT: '#6D28D9',
          light:   '#7C3AED',
          lighter: '#8B5CF6',
          dim:     'rgba(109,40,217,0.12)',
        },

        // Surfaces
        surface:         '#FFFFFF',
        'surface-muted': '#F8FAFC',
        'surface-hover': '#F1F5F9',

        // Borders
        border:          '#E2E8F0',
        'border-strong': '#CBD5E1',

        // Text hierarchy
        'text-primary':   '#0F172A',
        'text-secondary': '#475569',
        'text-muted':     '#94A3B8',
        'text-subtle':    '#64748B',

        // Semantic status
        success: { DEFAULT: '#059669', bg: '#F0FDF4', text: '#166534', border: '#BBF7D0' },
        warning: { DEFAULT: '#D97706', bg: '#FFFBEB', text: '#92400E', border: '#FDE68A' },
        danger:  { DEFAULT: '#E11D48', bg: '#FFF1F2', text: '#9F1239', border: '#FECDD3' },
        info:    { DEFAULT: '#2563EB', bg: '#EFF6FF', text: '#1E40AF', border: '#BFDBFE' },

        // Sidebar / primary container (deep navy)
        sidebar: '#161b2b',
        'sidebar-active': '#712edd',

        // Backward-compat school.* aliases
        school: {
          navy:       '#0A0F1E',
          red:        '#E11D48',
          grey:       '#F0F4F8',
          darkGrey:   '#424242',
          purple:     '#6D28D9',
          'purple-l': '#7C3AED',
          'purple-ll':'#8B5CF6',
        },
      },

      boxShadow: {
        card:         '0 1px 3px rgba(0,0,0,0.07), 0 1px 2px rgba(0,0,0,0.04)',
        'card-hover': '0 4px 14px rgba(0,0,0,0.10), 0 2px 4px rgba(0,0,0,0.05)',
        modal:        '0 20px 60px rgba(0,0,0,0.18)',
      },

      borderRadius: {
        // Design-system radius scale — squared "EduAdmin Pro" / Stitch spec
        sm:   '0.125rem',  //  2px — chips, checkboxes
        DEFAULT: '0.25rem',//  4px — buttons, inputs, cards (Tailwind 'rounded')
        md:   '0.375rem',  //  6px — medium surfaces
        card: '0.5rem',    //  8px — cards (alias used throughout codebase)
        lg:   '0.5rem',    //  8px — large widgets, featured panels
        xl:   '0.75rem',   // 12px — modals, full-bleed banners
        full: '9999px',    // pill buttons, badges
      },
    },
  },
  plugins: [],
}
