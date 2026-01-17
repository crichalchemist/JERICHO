# TechFlow Design System

A comprehensive design system for TechFlow's developer-focused SaaS platform, emphasizing clarity, precision, and modern aesthetics while maintaining exceptional accessibility standards.

---

## 1. Design Tokens

### CSS Custom Properties

```css
:root {
  /* === Base Unit System === */
  --tf-base-unit: 4px;
  --tf-border-radius-sm: calc(var(--tf-base-unit) * 1); /* 4px */
  --tf-border-radius-md: calc(var(--tf-base-unit) * 2); /* 8px */
  --tf-border-radius-lg: calc(var(--tf-base-unit) * 3); /* 12px */
  --tf-border-radius-xl: calc(var(--tf-base-unit) * 4); /* 16px */

  /* === Color System === */

  /* Primary - Tech Blue */
  --tf-primary-50: #eff6ff;
  --tf-primary-100: #dbeafe;
  --tf-primary-200: #bfdbfe;
  --tf-primary-300: #93c5fd;
  --tf-primary-400: #60a5fa;
  --tf-primary-500: #3b82f6; /* Brand color */
  --tf-primary-600: #2563eb;
  --tf-primary-700: #1d4ed8;
  --tf-primary-800: #1e40af;
  --tf-primary-900: #1e3a8a;

  /* Secondary - Tech Purple */
  --tf-secondary-50: #faf5ff;
  --tf-secondary-100: #f3e8ff;
  --tf-secondary-200: #e9d5ff;
  --tf-secondary-300: #d8b4fe;
  --tf-secondary-400: #c084fc;
  --tf-secondary-500: #a855f7; /* Accent color */
  --tf-secondary-600: #9333ea;
  --tf-secondary-700: #7c3aed;
  --tf-secondary-800: #6b21a8;
  --tf-secondary-900: #581c87;

  /* Success */
  --tf-success-50: #f0fdf4;
  --tf-success-100: #dcfce7;
  --tf-success-500: #22c55e;
  --tf-success-600: #16a34a;
  --tf-success-700: #15803d;

  /* Warning */
  --tf-warning-50: #fffbeb;
  --tf-warning-100: #fef3c7;
  --tf-warning-500: #f59e0b;
  --tf-warning-600: #d97706;
  --tf-warning-700: #b45309;

  /* Error */
  --tf-error-50: #fef2f2;
  --tf-error-100: #fee2e2;
  --tf-error-500: #ef4444;
  --tf-error-600: #dc2626;
  --tf-error-700: #b91c1c;

  /* Neutral Palette */
  --tf-neutral-50: #fafafa;
  --tf-neutral-100: #f5f5f5;
  --tf-neutral-200: #e5e5e5;
  --tf-neutral-300: #d4d4d4;
  --tf-neutral-400: #a3a3a3;
  --tf-neutral-500: #737373;
  --tf-neutral-600: #525252;
  --tf-neutral-700: #404040;
  --tf-neutral-800: #262626;
  --tf-neutral-900: #171717;

  /* === Typography === */
  --tf-font-sans:
    'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --tf-font-mono: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace;

  /* Type Scale - Minor Third (1.2) Scale */
  --tf-text-xs: 0.75rem; /* 12px */
  --tf-text-sm: 0.875rem; /* 14px */
  --tf-text-base: 1rem; /* 16px */
  --tf-text-lg: 1.125rem; /* 18px */
  --tf-text-xl: 1.25rem; /* 20px */
  --tf-text-2xl: 1.5rem; /* 24px */
  --tf-text-3xl: 1.875rem; /* 30px */
  --tf-text-4xl: 2.25rem; /* 36px */
  --tf-text-5xl: 3rem; /* 48px */

  /* Font Weights */
  --tf-font-regular: 400;
  --tf-font-medium: 500;
  --tf-font-semibold: 600;
  --tf-font-bold: 700;

  /* Line Heights */
  --tf-leading-tight: 1.25;
  --tf-leading-normal: 1.5;
  --tf-leading-relaxed: 1.625;

  /* === Spacing Scale === */
  --tf-space-0: 0;
  --tf-space-1: calc(var(--tf-base-unit) * 1); /* 4px */
  --tf-space-2: calc(var(--tf-base-unit) * 2); /* 8px */
  --tf-space-3: calc(var(--tf-base-unit) * 3); /* 12px */
  --tf-space-4: calc(var(--tf-base-unit) * 4); /* 16px */
  --tf-space-5: calc(var(--tf-base-unit) * 5); /* 20px */
  --tf-space-6: calc(var(--tf-base-unit) * 6); /* 24px */
  --tf-space-8: calc(var(--tf-base-unit) * 8); /* 32px */
  --tf-space-10: calc(var(--tf-base-unit) * 10); /* 40px */
  --tf-space-12: calc(var(--tf-base-unit) * 12); /* 48px */
  --tf-space-16: calc(var(--tf-base-unit) * 16); /* 64px */
  --tf-space-20: calc(var(--tf-base-unit) * 20); /* 80px */
  --tf-space-24: calc(var(--tf-base-unit) * 24); /* 96px */

  /* === Shadows === */
  --tf-shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --tf-shadow-md:
    0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --tf-shadow-lg:
    0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --tf-shadow-xl:
    0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);

  /* === Transitions === */
  --tf-transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  --tf-transition-normal: 250ms cubic-bezier(0.4, 0, 0.2, 1);
  --tf-transition-slow: 350ms cubic-bezier(0.4, 0, 0.2, 1);

  /* === Z-Index Scale === */
  --tf-z-dropdown: 1000;
  --tf-z-sticky: 1020;
  --tf-z-fixed: 1030;
  --tf-z-modal-backdrop: 1040;
  --tf-z-modal: 1050;
  --tf-z-popover: 1060;
  --tf-z-tooltip: 1070;
  --tf-z-toast: 1080;

  /* === Breakpoints === */
  --tf-breakpoint-sm: 640px;
  --tf-breakpoint-md: 768px;
  --tf-breakpoint-lg: 1024px;
  --tf-breakpoint-xl: 1280px;
  --tf-breakpoint-2xl: 1536px;
}

/* Dark Theme Support */
@media (prefers-color-scheme: dark) {
  :root {
    --tf-neutral-50: #171717;
    --tf-neutral-100: #262626;
    --tf-neutral-200: #404040;
    --tf-neutral-300: #525252;
    --tf-neutral-400: #737373;
    --tf-neutral-500: #a3a3a3;
    --tf-neutral-600: #d4d4d4;
    --tf-neutral-700: #e5e5e5;
    --tf-neutral-800: #f5f5f5;
    --tf-neutral-900: #fafafa;
  }
}
```

---

## 2. CSS Utility Classes

### Typography Utilities

```css
.tf-font-sans {
  font-family: var(--tf-font-sans);
}
.tf-font-mono {
  font-family: var(--tf-font-mono);
}

.tf-text-xs {
  font-size: var(--tf-text-xs);
}
.tf-text-sm {
  font-size: var(--tf-text-sm);
}
.tf-text-base {
  font-size: var(--tf-text-base);
}
.tf-text-lg {
  font-size: var(--tf-text-lg);
}
.tf-text-xl {
  font-size: var(--tf-text-xl);
}
.tf-text-2xl {
  font-size: var(--tf-text-2xl);
}
.tf-text-3xl {
  font-size: var(--tf-text-3xl);
}
.tf-text-4xl {
  font-size: var(--tf-text-4xl);
}
.tf-text-5xl {
  font-size: var(--tf-text-5xl);
}

.tf-font-regular {
  font-weight: var(--tf-font-regular);
}
.tf-font-medium {
  font-weight: var(--tf-font-medium);
}
.tf-font-semibold {
  font-weight: var(--tf-font-semibold);
}
.tf-font-bold {
  font-weight: var(--tf-font-bold);
}

.tf-leading-tight {
  line-height: var(--tf-leading-tight);
}
.tf-leading-normal {
  line-height: var(--tf-leading-normal);
}
.tf-leading-relaxed {
  line-height: var(--tf-leading-relaxed);
}
```

### Color Utilities

```css
.tf-text-primary {
  color: var(--tf-primary-600);
}
.tf-text-secondary {
  color: var(--tf-secondary-600);
}
.tf-text-success {
  color: var(--tf-success-600);
}
.tf-text-warning {
  color: var(--tf-warning-600);
}
.tf-text-error {
  color: var(--tf-error-600);
}
.tf-text-neutral {
  color: var(--tf-neutral-700);
}

.tf-bg-primary {
  background-color: var(--tf-primary-500);
}
.tf-bg-secondary {
  background-color: var(--tf-secondary-500);
}
.tf-bg-success {
  background-color: var(--tf-success-500);
}
.tf-bg-warning {
  background-color: var(--tf-warning-500);
}
.tf-bg-error {
  background-color: var(--tf-error-500);
}
.tf-bg-neutral {
  background-color: var(--tf-neutral-50);
}
```

### Spacing Utilities

```css
.tf-p-0 {
  padding: var(--tf-space-0);
}
.tf-p-1 {
  padding: var(--tf-space-1);
}
.tf-p-2 {
  padding: var(--tf-space-2);
}
.tf-p-3 {
  padding: var(--tf-space-3);
}
.tf-p-4 {
  padding: var(--tf-space-4);
}
.tf-p-5 {
  padding: var(--tf-space-5);
}
.tf-p-6 {
  padding: var(--tf-space-6);
}
.tf-p-8 {
  padding: var(--tf-space-8);
}

.tf-m-0 {
  margin: var(--tf-space-0);
}
.tf-m-1 {
  margin: var(--tf-space-1);
}
.tf-m-2 {
  margin: var(--tf-space-2);
}
.tf-m-3 {
  margin: var(--tf-space-3);
}
.tf-m-4 {
  margin: var(--tf-space-4);
}
.tf-m-5 {
  margin: var(--tf-space-5);
}
.tf-m-6 {
  margin: var(--tf-space-6);
}
.tf-m-8 {
  margin: var(--tf-space-8);
}
```

---

## 3. Core Component Specifications

### Button Component

#### Variants

- **Primary**: Main action buttons
- **Secondary**: Alternative actions
- **Ghost**: Minimal emphasis
- **Danger**: Destructive actions

#### Sizes

- **Small (sm)**: 32px height, compact
- **Medium (md)**: 40px height, default
- **Large (lg)**: 48px height, high emphasis

#### Implementation

```css
.tf-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid transparent;
  border-radius: var(--tf-border-radius-md);
  font-family: var(--tf-font-sans);
  font-weight: var(--tf-font-medium);
  text-decoration: none;
  cursor: pointer;
  transition: all var(--tf-transition-fast);
  white-space: nowrap;
  user-select: none;
  position: relative;
  overflow: hidden;
}

.tf-btn:focus-visible {
  outline: 2px solid var(--tf-primary-500);
  outline-offset: 2px;
}

/* Sizes */
.tf-btn--sm {
  height: 32px;
  padding: 0 var(--tf-space-3);
  font-size: var(--tf-text-sm);
  gap: var(--tf-space-1);
}

.tf-btn--md {
  height: 40px;
  padding: 0 var(--tf-space-4);
  font-size: var(--tf-text-base);
  gap: var(--tf-space-2);
}

.tf-btn--lg {
  height: 48px;
  padding: 0 var(--tf-space-6);
  font-size: var(--tf-text-lg);
  gap: var(--tf-space-2);
}

/* Primary Variant */
.tf-btn--primary {
  background-color: var(--tf-primary-500);
  color: white;
  border-color: var(--tf-primary-500);
}

.tf-btn--primary:hover {
  background-color: var(--tf-primary-600);
  border-color: var(--tf-primary-600);
}

.tf-btn--primary:active {
  background-color: var(--tf-primary-700);
  border-color: var(--tf-primary-700);
}

/* Secondary Variant */
.tf-btn--secondary {
  background-color: transparent;
  color: var(--tf-primary-600);
  border-color: var(--tf-primary-500);
}

.tf-btn--secondary:hover {
  background-color: var(--tf-primary-50);
  border-color: var(--tf-primary-600);
}

/* Ghost Variant */
.tf-btn--ghost {
  background-color: transparent;
  color: var(--tf-neutral-600);
  border-color: var(--tf-neutral-300);
}

.tf-btn--ghost:hover {
  background-color: var(--tf-neutral-50);
  color: var(--tf-neutral-700);
  border-color: var(--tf-neutral-400);
}

/* Danger Variant */
.tf-btn--danger {
  background-color: var(--tf-error-500);
  color: white;
  border-color: var(--tf-error-500);
}

.tf-btn--danger:hover {
  background-color: var(--tf-error-600);
  border-color: var(--tf-error-600);
}

/* Disabled State */
.tf-btn:disabled,
.tf-btn--disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

/* Loading State */
.tf-btn--loading {
  color: transparent;
  pointer-events: none;
}

.tf-btn--loading::after {
  content: '';
  position: absolute;
  width: 16px;
  height: 16px;
  border: 2px solid currentColor;
  border-radius: 50%;
  border-top-color: transparent;
  animation: tf-spin 0.8s linear infinite;
}

@keyframes tf-spin {
  to {
    transform: rotate(360deg);
  }
}
```

#### Usage Examples

```html
<!-- Primary Actions -->
<button class="tf-btn tf-btn--primary tf-btn--md">
  <span>Deploy to Production</span>
</button>

<!-- Secondary Actions -->
<button class="tf-btn tf-btn--secondary tf-btn--sm">Cancel</button>

<!-- Ghost Actions -->
<button class="tf-btn tf-btn--ghost tf-btn--md">
  <svg><!-- icon --></svg>
  View Documentation
</button>

<!-- Danger Actions -->
<button class="tf-btn tf-btn--danger tf-btn--md">Delete Resource</button>

<!-- Loading State -->
<button class="tf-btn tf-btn--primary tf-btn--md tf-btn--loading">
  Processing
</button>
```

### Input Component

#### Variants

- **Text**: Single-line text input
- **Password**: Password field with toggle
- **Search**: Search input with icon
- **Textarea**: Multi-line input

#### States

- **Default**: Ready for input
- **Focus**: Active input
- **Error**: Validation error
- **Disabled**: Not available

#### Implementation

```css
.tf-input {
  width: 100%;
  font-family: var(--tf-font-sans);
  font-size: var(--tf-text-base);
  line-height: var(--tf-leading-normal);
  color: var(--tf-neutral-900);
  background-color: var(--tf-neutral-50);
  border: 1px solid var(--tf-neutral-300);
  border-radius: var(--tf-border-radius-md);
  padding: var(--tf-space-3) var(--tf-space-4);
  transition: all var(--tf-transition-fast);
}

.tf-input::placeholder {
  color: var(--tf-neutral-500);
}

.tf-input:hover {
  border-color: var(--tf-neutral-400);
}

.tf-input:focus {
  outline: none;
  border-color: var(--tf-primary-500);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.tf-input:disabled {
  background-color: var(--tf-neutral-100);
  color: var(--tf-neutral-400);
  cursor: not-allowed;
}

.tf-input--error {
  border-color: var(--tf-error-500);
}

.tf-input--error:focus {
  border-color: var(--tf-error-500);
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

/* Textarea Specific */
.tf-textarea {
  resize: vertical;
  min-height: 120px;
}

/* Search Input */
.tf-search-wrapper {
  position: relative;
}

.tf-search-input {
  padding-left: var(--tf-space-10);
}

.tf-search-icon {
  position: absolute;
  left: var(--tf-space-3);
  top: 50%;
  transform: translateY(-50%);
  color: var(--tf-neutral-400);
  pointer-events: none;
}
```

#### Usage Examples

```html
<!-- Standard Input -->
<input class="tf-input" type="text" placeholder="Enter your API key" />

<!-- Error State -->
<input
  class="tf-input tf-input--error"
  type="email"
  placeholder="Email address"
/>
<div class="tf-error-message">Please enter a valid email address</div>

<!-- Search Input -->
<div class="tf-search-wrapper">
  <svg class="tf-search-icon" width="16" height="16"><!-- search icon --></svg>
  <input
    class="tf-input tf-search-input"
    type="search"
    placeholder="Search documentation..."
  />
</div>

<!-- Textarea -->
<textarea
  class="tf-input tf-textarea"
  placeholder="Enter your code review notes..."
></textarea>
```

### Card Component

#### Types

- **Default**: Standard content card
- **Interactive**: Clickable card
- **Status**: Visual status indicators

#### Implementation

```css
.tf-card {
  background-color: var(--tf-neutral-50);
  border: 1px solid var(--tf-neutral-200);
  border-radius: var(--tf-border-radius-lg);
  box-shadow: var(--tf-shadow-sm);
  transition: all var(--tf-transition-normal);
}

.tf-card:hover {
  box-shadow: var(--tf-shadow-md);
}

.tf-card--interactive {
  cursor: pointer;
}

.tf-card--interactive:hover {
  transform: translateY(-2px);
  box-shadow: var(--tf-shadow-lg);
}

.tf-card--interactive:active {
  transform: translateY(0);
}

.tf-card-header {
  padding: var(--tf-space-6);
  border-bottom: 1px solid var(--tf-neutral-200);
}

.tf-card-body {
  padding: var(--tf-space-6);
}

.tf-card-footer {
  padding: var(--tf-space-6);
  border-top: 1px solid var(--tf-neutral-200);
  background-color: var(--tf-neutral-100);
  border-radius: 0 0 var(--tf-border-radius-lg) var(--tf-border-radius-lg);
}

/* Status Variants */
.tf-card--success {
  border-left: 4px solid var(--tf-success-500);
}

.tf-card--warning {
  border-left: 4px solid var(--tf-warning-500);
}

.tf-card--error {
  border-left: 4px solid var(--tf-error-500);
}
```

#### Usage Examples

```html
<!-- Default Card -->
<div class="tf-card">
  <div class="tf-card-header">
    <h3 class="tf-text-xl tf-font-semibold">Project Overview</h3>
  </div>
  <div class="tf-card-body">
    <p>Card content goes here...</p>
  </div>
</div>

<!-- Interactive Card -->
<a href="#" class="tf-card tf-card--interactive">
  <div class="tf-card-body">
    <h4>Quick Deploy</h4>
    <p>Deploy your latest changes with one click</p>
  </div>
</a>

<!-- Status Card -->
<div class="tf-card tf-card--success">
  <div class="tf-card-body">
    <h4>Build Status: Success</h4>
    <p>All tests passed successfully</p>
  </div>
</div>
```

### Modal Component

#### Implementation

```css
.tf-modal-backdrop {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: var(--tf-z-modal-backdrop);
  opacity: 0;
  visibility: hidden;
  transition: all var(--tf-transition-normal);
}

.tf-modal-backdrop--open {
  opacity: 1;
  visibility: visible;
}

.tf-modal {
  background-color: var(--tf-neutral-50);
  border-radius: var(--tf-border-radius-lg);
  box-shadow: var(--tf-shadow-xl);
  max-width: 90vw;
  max-height: 90vh;
  overflow: auto;
  z-index: var(--tf-z-modal);
  transform: scale(0.95);
  transition: all var(--tf-transition-normal);
}

.tf-modal-backdrop--open .tf-modal {
  transform: scale(1);
}

.tf-modal-header {
  padding: var(--tf-space-6);
  border-bottom: 1px solid var(--tf-neutral-200);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.tf-modal-title {
  font-size: var(--tf-text-xl);
  font-weight: var(--tf-font-semibold);
  color: var(--tf-neutral-900);
  margin: 0;
}

.tf-modal-close {
  background: none;
  border: none;
  padding: var(--tf-space-2);
  border-radius: var(--tf-border-radius-md);
  cursor: pointer;
  color: var(--tf-neutral-500);
  transition: all var(--tf-transition-fast);
}

.tf-modal-close:hover {
  background-color: var(--tf-neutral-100);
  color: var(--tf-neutral-700);
}

.tf-modal-body {
  padding: var(--tf-space-6);
}

.tf-modal-footer {
  padding: var(--tf-space-6);
  border-top: 1px solid var(--tf-neutral-200);
  display: flex;
  gap: var(--tf-space-3);
  justify-content: flex-end;
}
```

#### Usage Example

```html
<div class="tf-modal-backdrop tf-modal-backdrop--open">
  <div class="tf-modal" role="dialog" aria-labelledby="modal-title">
    <div class="tf-modal-header">
      <h2 id="modal-title" class="tf-modal-title">Confirm Deployment</h2>
      <button class="tf-modal-close" aria-label="Close modal">
        <svg width="24" height="24"><!-- close icon --></svg>
      </button>
    </div>
    <div class="tf-modal-body">
      <p>Are you sure you want to deploy to production?</p>
    </div>
    <div class="tf-modal-footer">
      <button class="tf-btn tf-btn--secondary tf-btn--md">Cancel</button>
      <button class="tf-btn tf-btn--primary tf-btn--md">Deploy</button>
    </div>
  </div>
</div>
```

---

## 4. Implementation Guide

### File Structure Recommendations

```
styles/
├── tokens/
│   ├── colors.css
│   ├── typography.css
│   ├── spacing.css
│   └── shadows.css
├── utilities/
│   ├── layout.css
│   ├── typography.css
│   └── colors.css
├── components/
│   ├── buttons.css
│   ├── inputs.css
│   ├── cards.css
│   └── modals.css
└── main.css
```

### Integration Steps

1. **Include Design Tokens**: Import token definitions first
2. **Add Utilities**: Include utility classes for rapid development
3. **Import Components**: Load component-specific styles
4. **Customize**: Override tokens for theme variations

### Best Practices

1. **Use Tokens**: Always reference design tokens, never hard-code values
2. **Semantic Naming**: Use semantic color names (tf-text-primary) not literal ones (tf-text-blue)
3. **Responsive Design**: Utilize breakpoint tokens for responsive layouts
4. **State Management**: Use consistent state patterns across components
5. **Accessibility First**: Always include focus states and ARIA attributes

---

## 5. Accessibility Guidelines

### WCAG 2.1 AA Compliance Checklist

#### Color Contrast

✅ All text meets minimum 4.5:1 contrast ratio
✅ Large text (18px+) meets 3:1 contrast ratio
✅ Interactive elements have sufficient contrast

#### Keyboard Navigation

✅ All interactive elements are keyboard accessible
✅ Tab order follows logical sequence
✅ Focus indicators are clearly visible
✅ No keyboard traps

#### Screen Reader Support

✅ Semantic HTML elements used appropriately
✅ ARIA labels provided where needed
✅ Form elements properly labeled
✅ Dynamic content announcements included

#### Motion & Animation

✅ Respect prefers-reduced-motion
✅ No auto-playing animations >5 seconds
✅ Sufficient contrast for animated content

### Testing Procedures

1. **Automated Testing**: Use axe-core or similar tools
2. **Keyboard Testing**: Navigate interface using only keyboard
3. **Screen Reader Testing**: Test with NVDA, JAWS, or VoiceOver
4. **Color Contrast**: Verify with contrast checker tools
5. **User Testing**: Include users with disabilities

### Common Accessibility Patterns

#### Focus Management

```css
.tf-skip-link {
  position: absolute;
  top: -40px;
  left: 6px;
  background: var(--tf-primary-500);
  color: white;
  padding: 8px;
  text-decoration: none;
  border-radius: 4px;
  z-index: 9999;
}

.tf-skip-link:focus {
  top: 6px;
}
```

#### Screen Reader Only Content

```css
.tf-sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

---

## 6. Usage Guidelines

### Design Principles

1. **Clarity Over Decoration**: Every element should have a clear purpose
2. **Consistency**: Use established patterns repeatedly
3. **Developer Efficiency**: Design for implementation speed
4. **Performance**: Optimize for fast loading and smooth interactions
5. **Inclusivity**: Design for all users and abilities

### Do's and Don'ts

#### Typography

✅ Do maintain consistent hierarchy with type scale
✅ Do use appropriate line heights for readability
❌ Don't use more than 3 font weights in one interface
❌ Don't set text sizes smaller than 14px for body text

#### Colors

✅ Do use semantic color names in code
✅ Do ensure sufficient contrast for accessibility
❌ Don't rely on color alone to convey meaning
❌ Don't use too many bright colors in one view

#### Spacing

✅ Do use the spacing scale consistently
✅ Do align elements to the grid
❌ Don't create arbitrary spacing values
❌ Don't sacrifice breathing room for density

### Component Usage Guidelines

#### Buttons

- Use primary buttons for the main action in a view
- Limit to one primary button per view to maintain emphasis
- Use ghost buttons for secondary actions
- Ensure minimum 44px touch target for mobile

#### Inputs

- Always provide clear labels
- Use appropriate input types for validation
- Show error messages inline with the field
- Provide helpful placeholder text but not as a replacement for labels

#### Cards

- Use cards to group related information
- Maintain consistent card heights in grids
- Include clear actions or navigation
- Don't nest cards too deeply

---

## 7. Dark Theme Support

The design system includes comprehensive dark theme tokens. To implement dark mode:

```css
/* Theme Toggle */
[data-theme='dark'] {
  --tf-neutral-50: #171717;
  --tf-neutral-100: #262626;
  /* ... other dark mode token overrides */
}

/* Auto-detect user preference */
@media (prefers-color-scheme: dark) {
  :root {
    --tf-neutral-50: #171717;
    --tf-neutral-100: #262626;
    /* ... other dark mode token overrides */
  }
}
```

---

## 8. Browser Support

- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **CSS Custom Properties**: Supported in all modern browsers
- **Grid & Flexbox**: Widely supported
- **Fallbacks**: Include for IE11 if required

---

## 9. Performance Considerations

- **CSS Size**: Use PostCSS to purge unused utilities
- **Font Loading**: Use font-display: swap for better perceived performance
- **Critical CSS**: Inline critical styles for faster initial render
- **Animation**: Use transform and opacity for smooth 60fps animations

---

This design system provides a solid foundation for building consistent, accessible, and modern interfaces for TechFlow. All components are designed with developer experience in mind and include comprehensive accessibility support.
