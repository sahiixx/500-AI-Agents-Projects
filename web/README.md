# Vercel Speed Insights Integration

This directory contains the Vercel Speed Insights integration for the 500 AI Agent Projects repository. Speed Insights provides real-time performance monitoring and Core Web Vitals tracking for web applications.

## 📋 Overview

Vercel Speed Insights is a lightweight, privacy-focused real user monitoring (RUM) solution that tracks:
- **LCP** (Largest Contentful Paint) - when the main content loads
- **FID** (First Input Delay) - responsiveness to user input
- **CLS** (Cumulative Layout Shift) - visual stability
- Additional metrics like FCP, TTFB, and page load time

## 📦 Installation

The package has already been installed via npm:

```bash
npm install @vercel/speed-insights
```

Check `package.json` to verify `@vercel/speed-insights` is listed as a dependency.

## 🚀 Quick Start

### For Plain HTML Sites

Add this script tag directly to your HTML file before the closing `</body>` tag:

```html
<script defer src="https://cdn.vercel-analytics.com/v1/speed-insights/script.js"></script>
```

**Example:** See `index.html` for a complete example.

### For JavaScript Frameworks (React, Next.js, Vue, Angular, Svelte)

1. **Import the module** in your app's entry point:

```javascript
import { injectSpeedInsights } from '@vercel/speed-insights'
```

2. **Call the initialization function** on the client side:

```javascript
injectSpeedInsights()
```

3. **Important:** Ensure it only runs on the client side (not during server-side rendering)

## 🔧 Framework-Specific Implementations

### Next.js (App Router - Next.js 13+)

```typescript
// app.tsx or app.jsx
'use client'

import { useEffect } from 'react'
import { injectSpeedInsights } from '@vercel/speed-insights'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  useEffect(() => {
    injectSpeedInsights()
  }, [])

  return (
    <html>
      <body>{children}</body>
    </html>
  )
}
```

### Next.js (Pages Router - Next.js 12 and earlier)

```typescript
// pages/_app.tsx
import { useEffect } from 'react'
import { injectSpeedInsights } from '@vercel/speed-insights'

function MyApp({ Component, pageProps }) {
  useEffect(() => {
    injectSpeedInsights()
  }, [])

  return <Component {...pageProps} />
}

export default MyApp
```

### React

```typescript
// src/App.tsx
import { useEffect } from 'react'
import { injectSpeedInsights } from '@vercel/speed-insights'

function App() {
  useEffect(() => {
    injectSpeedInsights()
  }, [])

  return <div>Your app content</div>
}

export default App
```

### Vue 3

```typescript
// src/main.ts
import { createApp } from 'vue'
import { injectSpeedInsights } from '@vercel/speed-insights'
import App from './App.vue'

const app = createApp(App)

injectSpeedInsights()
app.mount('#app')
```

### Angular

```typescript
// src/main.ts
import { injectSpeedInsights } from '@vercel/speed-insights'
import { bootstrapApplication } from '@angular/platform-browser'
import { AppComponent } from './app/app.component'

injectSpeedInsights()
bootstrapApplication(AppComponent)
```

### Svelte

```svelte
<!-- src/App.svelte -->
<script>
  import { onMount } from 'svelte'
  import { injectSpeedInsights } from '@vercel/speed-insights'

  onMount(() => {
    injectSpeedInsights()
  })
</script>

<div>Your app content</div>
```

## 📊 Dashboard & Monitoring

Once integrated, view your performance metrics:

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Navigate to **Analytics** → **Speed Insights**
4. Monitor real-time Core Web Vitals
5. Analyze performance trends over time

## 🔒 Privacy & Data

- **No PII Collected:** Vercel Speed Insights doesn't collect personally identifiable information
- **Privacy-Respecting:** Complies with GDPR and other privacy regulations
- **User Control:** Users can opt-out through browser privacy settings
- **Transparent:** All data is aggregated and anonymized

## ⚙️ Configuration

### Environment-Specific Loading

Only enable Speed Insights in production:

```javascript
import { useEffect } from 'react'

export default function App() {
  useEffect(() => {
    if (process.env.NODE_ENV === 'production') {
      import('@vercel/speed-insights').then(({ injectSpeedInsights }) => {
        injectSpeedInsights()
      })
    }
  }, [])

  return <div>Your app</div>
}
```

### Route-Specific Exclusion

To exclude specific routes from monitoring, conditionally call `injectSpeedInsights()`:

```javascript
useEffect(() => {
  // Only inject on specific routes
  if (location.pathname === '/dashboard') {
    injectSpeedInsights()
  }
}, [])
```

## 🐛 Troubleshooting

### Speed Insights Not Appearing in Dashboard

1. **Ensure it's deployed:** Speed Insights only works on deployed Vercel projects
2. **Check initialization:** Verify `injectSpeedInsights()` is called
3. **Client-side only:** Make sure it's not running during server-side rendering
4. **Wait for data:** Allow 5-10 minutes for initial data to appear

### Reduce Bundle Size Impact

The Speed Insights package is extremely lightweight (~2KB gzipped):

```bash
npm ls @vercel/speed-insights
```

The impact on your bundle size is minimal.

## 📚 Example Files

- **`index.html`** - Plain HTML example with integration instructions
- **`speed-insights-setup.js`** - Detailed setup module with framework patterns
- **`app.jsx.example`** - Next.js and React implementation examples

## 🔗 Resources

- [Vercel Speed Insights Documentation](https://vercel.com/docs/speed-insights)
- [Web Vitals Guide](https://web.dev/vitals/)
- [Vercel Analytics](https://vercel.com/docs/analytics)
- [GitHub Repository](https://github.com/vercel/speed-insights)

## 📝 Notes

- **Must run on client side:** Uses browser APIs to collect performance data
- **Automatic collection:** No manual metric reporting needed
- **Real user data:** Monitors actual user experience, not synthetic tests
- **Framework agnostic:** Works with any JavaScript framework
- **Zero configuration:** Works out of the box once called

## 🤝 Contributing

For improvements or issues with the Speed Insights integration, please refer to the main repository's contribution guidelines.

---

**Happy monitoring!** 🚀 Keep your AI agent projects running fast and smooth with Vercel Speed Insights.
