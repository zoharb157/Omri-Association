// Chart Theme System - Uses design tokens and RTL-safe configurations
export const chartTheme = {
  // Colors from our design system
  colors: {
    primary: "var(--accent)",
    success: "var(--success)", 
    warning: "var(--warning)",
    danger: "var(--danger)",
    info: "var(--info)",
    muted: "var(--muted)",
    text: "var(--text)",
    surface: "var(--surface)",
    border: "var(--border)"
  },
  
  // Chart-specific colors
  chart: {
    axisColor: "var(--muted)",
    labelColor: "var(--text)",
    grid: "var(--border)",
    bar: "var(--accent)",
    line: "var(--accent)",
    pie: [
      "var(--accent)",
      "var(--success)", 
      "var(--warning)",
      "var(--danger)",
      "var(--info)",
      "#8B5CF6", // purple
      "#F59E0B", // amber
      "#10B981"  // emerald
    ]
  },
  
  // Typography
  typography: {
    fontSize: {
      xs: "var(--text-xs)",
      sm: "var(--text-sm)", 
      base: "var(--text-md)",
      lg: "var(--text-lg)"
    },
    fontFamily: "Rubik, Assistant, system-ui, sans-serif"
  },
  
  // Spacing
  spacing: {
    padding: "var(--space-4)",
    margin: "var(--space-2)"
  }
};

// Hebrew currency formatter
export const fmtCurrency = (n: number) => 
  new Intl.NumberFormat("he-IL", { 
    style: "currency", 
    currency: "ILS", 
    maximumFractionDigits: 0 
  }).format(n);

// Hebrew date formatter
export const fmtDate = (date: Date) =>
  new Intl.DateTimeFormat("he-IL", {
    year: "numeric",
    month: "short",
    day: "numeric"
  }).format(date);

// RTL-safe chart configurations
export const rtlConfig = {
  // RTL layout adjustments
  layout: {
    direction: "rtl" as const
  },
  
  // Responsive breakpoints
  responsive: {
    mobile: 320,
    tablet: 768,
    desktop: 1440
  }
};



