/**
 * Vercel Speed Insights Integration Example
 * 
 * This module demonstrates how to properly integrate Vercel Speed Insights
 * in a JavaScript application for client-side performance monitoring.
 * 
 * Installation:
 *   npm install @vercel/speed-insights
 * 
 * Usage:
 *   import { injectSpeedInsights } from '@vercel/speed-insights'
 *   injectSpeedInsights()
 */

/**
 * Initialize Vercel Speed Insights
 * 
 * This function should be called as early as possible in your application's
 * initialization, ideally in your app's entry point (e.g., app.js, index.js, main.ts).
 * 
 * IMPORTANT: Must run on the client side only. Use browser detection if running
 * in a universal/isomorphic environment.
 * 
 * @example
 * // In your main app file (runs only in browser)
 * if (typeof window !== 'undefined') {
 *   const { injectSpeedInsights } = await import('@vercel/speed-insights')
 *   injectSpeedInsights()
 * }
 */
export async function setupSpeedInsights() {
  // Only run on client side
  if (typeof window === 'undefined') {
    console.warn('Vercel Speed Insights: Skipping initialization on server side')
    return
  }

  try {
    // Import the speed insights module
    const { injectSpeedInsights } = await import('@vercel/speed-insights')
    
    // Initialize Speed Insights
    injectSpeedInsights()
    
    console.log('✅ Vercel Speed Insights initialized successfully')
    console.log('📊 Now tracking Core Web Vitals and Real User Monitoring')
  } catch (error) {
    console.warn('⚠️ Failed to initialize Vercel Speed Insights:', error)
  }
}

/**
 * Alternative: Direct import pattern (for bundled applications)
 * 
 * This pattern is useful for modern frameworks that support ES modules.
 * 
 * @example
 * // In your React app (app.jsx or App.tsx)
 * import { injectSpeedInsights } from '@vercel/speed-insights'
 * 
 * // Call at app initialization
 * injectSpeedInsights()
 * 
 * // Or use a useEffect hook
 * import { useEffect } from 'react'
 * 
 * function App() {
 *   useEffect(() => {
 *     injectSpeedInsights()
 *   }, [])
 *   
 *   return <div>Your app content</div>
 * }
 */

/**
 * Framework-Specific Integration Patterns
 * 
 * NEXT.JS:
 * --------
 * // app.js or pages/_app.js (Next.js 12+)
 * import { injectSpeedInsights } from '@vercel/speed-insights'
 * 
 * export default function MyApp({ Component, pageProps }) {
 *   useEffect(() => {
 *     injectSpeedInsights()
 *   }, [])
 *   
 *   return <Component {...pageProps} />
 * }
 * 
 * REACT:
 * ------
 * // src/App.jsx or src/main.jsx
 * import { useEffect } from 'react'
 * import { injectSpeedInsights } from '@vercel/speed-insights'
 * 
 * function App() {
 *   useEffect(() => {
 *     injectSpeedInsights()
 *   }, [])
 *   
 *   return <div>Your app</div>
 * }
 * 
 * VUE:
 * ----
 * // src/main.js
 * import { createApp } from 'vue'
 * import { injectSpeedInsights } from '@vercel/speed-insights'
 * import App from './App.vue'
 * 
 * const app = createApp(App)
 * injectSpeedInsights()
 * app.mount('#app')
 * 
 * ANGULAR:
 * --------
 * // src/main.ts
 * import { injectSpeedInsights } from '@vercel/speed-insights'
 * import { bootstrapApplication } from '@angular/platform-browser'
 * import { AppComponent } from './app/app.component'
 * 
 * injectSpeedInsights()
 * bootstrapApplication(AppComponent)
 * 
 * SVELTE:
 * -------
 * // src/App.svelte
 * <script>
 *   import { onMount } from 'svelte'
 *   import { injectSpeedInsights } from '@vercel/speed-insights'
 *   
 *   onMount(() => {
 *     injectSpeedInsights()
 *   })
 * </script>
 */

/**
 * What Vercel Speed Insights Tracks
 * 
 * Core Web Vitals:
 * - LCP (Largest Contentful Paint): Time until largest content element renders
 * - FID (First Input Delay): Delay between user input and response
 * - CLS (Cumulative Layout Shift): Measure of visual stability
 * 
 * Additional Metrics:
 * - First Contentful Paint (FCP)
 * - Time to First Byte (TTFB)
 * - Page load time
 * - Resource timing information
 * 
 * The data is collected in real-time from actual user interactions
 * and aggregated in the Vercel dashboard for analysis.
 */

/**
 * Privacy and Data Collection
 * 
 * - Vercel Speed Insights respects user privacy
 * - No personally identifiable information (PII) is collected
 * - Data collection can be disabled through configuration
 * - GDPR and privacy regulations are respected
 * 
 * To disable analytics on a page:
 *   Remove the injectSpeedInsights() call from that page
 *   Or use environment variables for conditional loading
 */

// Export the setup function as default
export default setupSpeedInsights
