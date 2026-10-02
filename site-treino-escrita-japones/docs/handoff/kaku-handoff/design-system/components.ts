// Kaku Design System — variantes dos componentes com class-variance-authority (CVA).
// Todas as classes vêm da escala padrão do Tailwind + aliases de tailwind.config.js.
import { cva, type VariantProps } from 'class-variance-authority';

const focusRing = 'focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary';
const disabled = 'disabled:cursor-not-allowed disabled:opacity-50 aria-disabled:cursor-not-allowed aria-disabled:opacity-50';

// ---------------------------------------------------------------- tipografia
export const text = cva('', {
  variants: {
    role: {
      display: 'font-serif text-6xl leading-none font-bold text-text-primary',
      h1: 'font-serif text-5xl leading-none font-bold text-text-primary',
      h2: 'font-serif text-3xl leading-9 font-bold text-text-primary',
      h3: 'text-xl leading-7 font-bold text-text-primary',
      h4: 'text-lg leading-7 font-bold text-text-primary',
      body: 'text-base leading-6 text-text-secondary',
      small: 'text-sm leading-5 text-text-secondary',
      label: 'text-sm leading-5 font-bold text-text-primary',
      caption: 'text-xs leading-4 text-text-muted',
      overline: 'text-xs leading-4 font-bold uppercase tracking-widest text-text-muted',
    },
  },
  defaultVariants: { role: 'body' },
});

// ---------------------------------------------------------------- layout
export const page = cva('mx-auto w-full max-w-7xl px-5 sm:px-6 lg:px-12 xl:px-20 pt-10 pb-12');
export const section = cva('flex flex-col', { variants: { spacing: { md: 'gap-6', lg: 'gap-8 lg:gap-12' } }, defaultVariants: { spacing: 'md' } });
export const stack = cva('flex flex-col', { variants: { gap: { related: 'gap-2', group: 'gap-3', component: 'gap-4', block: 'gap-6' } }, defaultVariants: { gap: 'component' } });

// ---------------------------------------------------------------- botões
export const button = cva(
  `inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg font-bold transition active:scale-95 ${focusRing} ${disabled}`,
  {
    variants: {
      variant: {
        primary: 'bg-primary text-white hover:bg-primary-hover active:bg-primary-active',
        secondary: 'bg-secondary text-white hover:bg-secondary-hover active:bg-secondary-active',
        outline: 'border border-border bg-surface font-medium text-text-primary hover:bg-background-subtle active:bg-surface-muted',
        ghost: 'bg-transparent font-medium text-text-primary hover:bg-surface-muted active:bg-border',
        danger: 'bg-error text-white hover:bg-red-800 active:bg-red-900',
        link: 'bg-transparent p-0 text-primary underline-offset-4 hover:text-primary-hover hover:underline',
      },
      size: { sm: 'h-9 px-3 text-sm', md: 'h-11 px-4 text-sm', lg: 'h-12 px-6 text-base', icon: 'size-11' },
      loading: { true: 'pointer-events-none', false: '' },
    },
    compoundVariants: [{ variant: 'link', className: 'h-auto px-0' }],
    defaultVariants: { variant: 'primary', size: 'md', loading: false },
  },
);
export type ButtonProps = VariantProps<typeof button>;
export const spinner = cva('animate-spin', { variants: { size: { sm: 'size-4', md: 'size-5' } }, defaultVariants: { size: 'sm' } });

// ---------------------------------------------------------------- campos
const fieldBase = `w-full rounded-lg border bg-surface px-4 text-base text-text-primary placeholder:text-text-placeholder transition
  hover:border-stone-400 focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary-muted
  disabled:cursor-not-allowed disabled:bg-surface-muted disabled:text-text-disabled`;
export const input = cva(`${fieldBase} h-11`, {
  variants: { state: { default: 'border-border-strong', error: 'border-primary bg-error-subtle focus:ring-error-bg' } },
  defaultVariants: { state: 'default' },
});
export const select = cva(`${fieldBase} h-11 appearance-none pr-10`, { variants: { state: { default: 'border-border-strong', error: 'border-primary' } }, defaultVariants: { state: 'default' } });
export const textarea = cva(`${fieldBase} min-h-24 py-3 leading-6`, { variants: { state: { default: 'border-border-strong', error: 'border-primary' } }, defaultVariants: { state: 'default' } });
export const fieldLabel = cva('text-sm leading-5 font-bold text-text-primary');
export const fieldMessage = cva('flex items-start gap-1.5 text-xs leading-4', { variants: { tone: { help: 'text-text-muted', error: 'text-error' } }, defaultVariants: { tone: 'help' } });
export const formStack = cva('flex flex-col gap-4'); // entre campos; rótulo→campo = gap-2

export const checkbox = cva(`size-5 rounded-md border-2 border-border-strong text-primary checked:border-primary checked:bg-primary ${focusRing} ${disabled}`);
export const radio = cva(`size-5 rounded-full border-2 border-border-strong checked:border-primary ${focusRing} ${disabled}`);
export const switchTrack = cva(`relative h-6 w-11 rounded-full transition ${focusRing} ${disabled}`, { variants: { on: { true: 'bg-primary', false: 'bg-stone-300' } }, defaultVariants: { on: false } });

// ---------------------------------------------------------------- superfícies
export const card = cva('rounded-xl border bg-surface', {
  variants: {
    padding: { none: '', sm: 'p-4', md: 'p-5', lg: 'p-6' },
    interactive: { true: 'transition hover:-translate-y-0.5 hover:shadow-lg', false: '' },
    selected: { true: 'border-primary ring-2 ring-primary-muted bg-accent-subtle', false: 'border-border' },
  },
  defaultVariants: { padding: 'lg', interactive: false, selected: false },
});
export const panel = cva('rounded-xl bg-surface-muted p-4');
export const modal = cva('w-full max-w-md rounded-xl bg-surface p-6 shadow-xl');
export const overlay = cva('fixed inset-0 bg-stone-950/40');
export const dropdown = cva('w-64 rounded-xl border border-border bg-surface p-2 shadow-lg');
export const menuItem = cva(`flex h-11 items-center gap-3 rounded-lg px-3 text-sm text-text-primary hover:bg-surface-muted ${focusRing}`, {
  variants: { tone: { default: '', danger: 'text-error' }, active: { true: 'bg-accent-subtle font-bold text-error', false: '' } },
  defaultVariants: { tone: 'default', active: false },
});
export const tooltip = cva('max-w-60 rounded-md bg-secondary px-2 py-2 text-xs leading-4 text-white shadow-md');

// ---------------------------------------------------------------- feedback
export const badge = cva('inline-flex h-6 items-center gap-1 rounded-md px-2 text-xs font-bold', {
  variants: {
    tone: {
      neutral: 'bg-surface-muted text-text-secondary', inverse: 'bg-secondary text-white',
      primary: 'bg-primary-muted text-error', success: 'bg-success-bg text-success', warning: 'bg-warning-bg text-warning',
      error: 'bg-error-bg text-error', info: 'bg-info-bg text-info',
      hiragana: 'bg-hiragana-bg text-hiragana', katakana: 'bg-katakana-bg text-katakana', kanji: 'bg-kanji-bg text-kanji',
    },
  },
  defaultVariants: { tone: 'neutral' },
});
export const alert = cva('flex items-start gap-3 rounded-lg border px-4 py-3 text-sm leading-5', {
  variants: { tone: { info: 'border-info-border bg-info-subtle text-info', success: 'border-success-border bg-success-subtle text-success', warning: 'border-warning-border bg-warning-subtle text-warning', error: 'border-error-border bg-error-subtle text-error' } },
  defaultVariants: { tone: 'info' },
});
export const skeleton = cva('animate-pulse rounded-md bg-border');
export const emptyState = cva('flex flex-col items-center gap-2 rounded-xl border border-dashed border-border-strong p-6 text-center');

// ---------------------------------------------------------------- navegação
export const tabs = cva('inline-flex gap-1 rounded-full bg-border p-1');
export const tab = cva(`h-9 rounded-full px-4 text-sm transition ${focusRing}`, {
  variants: { active: { true: 'bg-surface font-bold text-text-primary shadow-sm', false: 'font-medium text-text-secondary hover:text-text-primary' } },
  defaultVariants: { active: false },
});
export const chip = cva(`inline-flex h-9 items-center gap-2 rounded-full border px-3 text-sm transition ${focusRing} ${disabled}`, {
  variants: { selected: { true: 'border-secondary bg-secondary text-white', false: 'border-border bg-surface text-text-secondary hover:bg-background-subtle' } },
  defaultVariants: { selected: false },
});
export const navbar = cva('sticky top-0 z-30 flex h-16 items-center justify-between border-b border-border bg-background px-5 lg:px-12 xl:px-20');
export const navLink = cva(`flex h-11 items-center rounded-full px-5 text-sm transition ${focusRing}`, {
  variants: { active: { true: 'bg-surface font-bold text-primary ring-1 ring-border', false: 'font-medium text-text-secondary hover:bg-border hover:text-text-primary' } },
  defaultVariants: { active: false },
});
export const bottomNav = cva('fixed inset-x-0 bottom-0 flex h-20 border-t border-border bg-surface px-2 pb-4 pt-2 md:hidden');
export const sidebar = cva('flex w-64 flex-col gap-1 rounded-xl border border-border bg-surface p-3');
export const breadcrumb = cva('flex items-center gap-2 text-sm');
export const table = cva('w-full border-collapse text-sm');
export const th = cva('py-3 text-left text-xs font-bold uppercase tracking-wider text-text-muted');
export const td = cva('border-t border-border py-3 text-text-primary');
export const paginationItem = cva(`inline-flex h-9 min-w-9 items-center justify-center rounded-lg border px-2 text-sm ${focusRing} ${disabled}`, {
  variants: { current: { true: 'border-secondary bg-secondary font-bold text-white', false: 'border-border bg-surface text-text-secondary hover:bg-background-subtle' } },
  defaultVariants: { current: false },
});
export const progress = cva('h-2 overflow-hidden rounded-full bg-border');
