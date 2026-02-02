# Getting started with Speed Insights

This guide will help you get started with using Vercel Speed Insights on your project, showing you how to enable it, add the package to your project, deploy your app to Vercel, and view your data in the dashboard.

To view instructions on using the Vercel Speed Insights in your project for your framework, use the **Choose a framework** dropdown on the right (at the bottom in mobile view).

## Prerequisites

- A Vercel account. If you don't have one, you can [sign up for free](https://vercel.com/signup).
- A Vercel project. If you don't have one, you can [create a new project](https://vercel.com/new).
- The Vercel CLI installed. If you don't have it, you can install it using the following command:

### Install Vercel CLI

**Using pnpm:**
```bash
pnpm i vercel
```

**Using yarn:**
```bash
yarn add vercel
```

**Using npm:**
```bash
npm i vercel
```

**Using bun:**
```bash
bun add vercel
```

## Setup Steps

### 1. Enable Speed Insights in Vercel

On the [Vercel dashboard](https://vercel.com/dashboard), select your Project followed by the **Speed Insights** tab. You can also select the button below to be taken there. Then, select **Enable** from the dialog.

> **💡 Note:** Enabling Speed Insights will add new routes (scoped at `/_vercel/speed-insights/*`) after your next deployment.

### 2. Add `@vercel/speed-insights` to your project

Using the package manager of your choice, add the `@vercel/speed-insights` package to your project:

**Using pnpm:**
```bash
pnpm i @vercel/speed-insights
```

**Using yarn:**
```bash
yarn add @vercel/speed-insights
```

**Using npm:**
```bash
npm i @vercel/speed-insights
```

**Using bun:**
```bash
bun add @vercel/speed-insights
```

> **💡 Note:** When using the HTML implementation, there is no need to install the `@vercel/speed-insights` package.

## Framework-Specific Integration

### Next.js (Pages Router)

The `SpeedInsights` component is a wrapper around the tracking script, offering more seamless integration with Next.js.

Add the following component to your main app file:

**TypeScript (`pages/_app.tsx`):**
```tsx
import type { AppProps } from 'next/app';
import { SpeedInsights } from '@vercel/speed-insights/next';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
      <Component {...pageProps} />
      <SpeedInsights />
    </>
  );
}

export default MyApp;
```

**JavaScript (`pages/_app.jsx`):**
```jsx
import { SpeedInsights } from "@vercel/speed-insights/next";

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Component {...pageProps} />
      <SpeedInsights />
    </>
  );
}

export default MyApp;
```

#### For Next.js versions older than 13.5

Import the `<SpeedInsights>` component from `@vercel/speed-insights/react` and pass it the pathname of the route:

**TypeScript (`pages/example-component.tsx`):**
```tsx
import { SpeedInsights } from "@vercel/speed-insights/react";
import { useRouter } from "next/router";

export default function Layout() {
  const router = useRouter();

  return <SpeedInsights route={router.pathname} />;
}
```

**JavaScript (`pages/example-component.jsx`):**
```jsx
import { SpeedInsights } from "@vercel/speed-insights/react";
import { useRouter } from "next/router";

export default function Layout() {
  const router = useRouter();

  return <SpeedInsights route={router.pathname} />;
}
```

### Next.js (App Router)

The `SpeedInsights` component is a wrapper around the tracking script, offering more seamless integration with Next.js.

Add the following component to the root layout:

**TypeScript (`app/layout.tsx`):**
```tsx
import { SpeedInsights } from "@vercel/speed-insights/next";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <title>Next.js</title>
      </head>
      <body>
        {children}
        <SpeedInsights />
      </body>
    </html>
  );
}
```

**JavaScript (`app/layout.jsx`):**
```jsx
import { SpeedInsights } from "@vercel/speed-insights/next";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <title>Next.js</title>
      </head>
      <body>
        {children}
        <SpeedInsights />
      </body>
    </html>
  );
}
```

#### For Next.js versions older than 13.5

Import the `<SpeedInsights>` component from `@vercel/speed-insights/react`.

Create a dedicated component to avoid opting out from SSR on the layout and pass the pathname of the route to the `SpeedInsights` component:

**TypeScript (`app/insights.tsx`):**
```tsx
"use client";

import { SpeedInsights } from "@vercel/speed-insights/react";
import { usePathname } from "next/navigation";

export function Insights() {
  const pathname = usePathname();

  return <SpeedInsights route={pathname} />;
}
```

**JavaScript (`app/insights.jsx`):**
```jsx
"use client";

import { SpeedInsights } from "@vercel/speed-insights/react";
import { usePathname } from "next/navigation";

export function Insights() {
  const pathname = usePathname();

  return <SpeedInsights route={pathname} />;
}
```

Then, import the `Insights` component in your layout:

**TypeScript (`app/layout.tsx`):**
```tsx
import type { ReactNode } from "react";
import { Insights } from "./insights";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <head>
        <title>Next.js</title>
      </head>
      <body>
        {children}
        <Insights />
      </body>
    </html>
  );
}
```

**JavaScript (`app/layout.jsx`):**
```jsx
import { Insights } from "./insights";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <title>Next.js</title>
      </head>
      <body>
        {children}
        <Insights />
      </body>
    </html>
  );
}
```

### Create React App

The `SpeedInsights` component is a wrapper around the tracking script, offering more seamless integration with React.

Add the following component to the main app file:

**TypeScript (`App.tsx`):**
```tsx
import { SpeedInsights } from '@vercel/speed-insights/react';

export default function App() {
  return (
    <div>
      {/* ... */}
      <SpeedInsights />
    </div>
  );
}
```

**JavaScript (`App.jsx`):**
```jsx
import { SpeedInsights } from "@vercel/speed-insights/react";

export default function App() {
  return (
    <div>
      {/* ... */}
      <SpeedInsights />
    </div>
  );
}
```

### Remix

The `SpeedInsights` component is a wrapper around the tracking script, offering a seamless integration with Remix.

Add the following component to your root file:

**TypeScript (`app/root.tsx`):**
```tsx
import { SpeedInsights } from '@vercel/speed-insights/remix';

export default function App() {
  return (
    <html lang="en">
      <body>
        {/* ... */}
        <SpeedInsights />
      </body>
    </html>
  );
}
```

**JavaScript (`app/root.jsx`):**
```jsx
import { SpeedInsights } from "@vercel/speed-insights/remix";

export default function App() {
  return (
    <html lang="en">
      <body>
        {/* ... */}
        <SpeedInsights />
      </body>
    </html>
  );
}
```

### SvelteKit

Add the following component to your root file:

**TypeScript (`src/routes/+layout.ts`):**
```typescript
import { injectSpeedInsights } from "@vercel/speed-insights/sveltekit";

injectSpeedInsights();
```

**JavaScript (`src/routes/+layout.js`):**
```javascript
import { injectSpeedInsights } from "@vercel/speed-insights/sveltekit";

injectSpeedInsights();
```

### Vue.js

The `SpeedInsights` component is a wrapper around the tracking script, offering more seamless integration with Vue.

Add the following component to the main app template:

**TypeScript (`src/App.vue`):**
```vue
<script setup lang="ts">
import { SpeedInsights } from '@vercel/speed-insights/vue';
</script>

<template>
  <SpeedInsights />
</template>
```

**JavaScript (`src/App.vue`):**
```vue
<script setup>
import { SpeedInsights } from '@vercel/speed-insights/vue';
</script>

<template>
  <SpeedInsights />
</template>
```

### Nuxt

The `SpeedInsights` component is a wrapper around the tracking script, offering more seamless integration with Nuxt.

Add the following component to the default layout:

**TypeScript (`layouts/default.vue`):**
```vue
<script setup lang="ts">
import { SpeedInsights } from '@vercel/speed-insights/vue';
</script>

<template>
  <SpeedInsights />
</template>
```

**JavaScript (`layouts/default.vue`):**
```vue
<script setup>
import { SpeedInsights } from '@vercel/speed-insights/vue';
</script>

<template>
  <SpeedInsights />
</template>
```

### Astro

Speed Insights is available for both [static](https://docs.vercel.com/docs/frameworks/astro#static-rendering) and [SSR](https://docs.vercel.com/docs/frameworks/astro#server-side-rendering) Astro apps.

To enable this feature, declare the `<SpeedInsights />` component from `@vercel/speed-insights/astro` near the bottom of one of your layout components, such as `BaseHead.astro`:

**TypeScript (`BaseHead.astro`):**
```astro
---
import SpeedInsights from '@vercel/speed-insights/astro';
const { title, description } = Astro.props;
---
<title>{title}</title>
<meta name="title" content={title} />
<meta name="description" content={description} />

<SpeedInsights />
```

**JavaScript (`BaseHead.astro`):**
```astro
---
import SpeedInsights from '@vercel/speed-insights/astro';
const { title, description } = Astro.props;
---
<title>{title}</title>
<meta name="title" content={title} />
<meta name="description" content={description} />

<SpeedInsights />
```

#### Optional: Remove sensitive information from URL

You can remove sensitive information from the URL by adding a `speedInsightsBeforeSend` function to the global `window` object. The `<SpeedInsights />` component will call this method before sending any data to Vercel:

**TypeScript (`BaseHead.astro`):**
```astro
---
import SpeedInsights from '@vercel/speed-insights/astro';
const { title, description } = Astro.props;
---
<title>{title}</title>
<meta name="title" content={title} />
<meta name="description" content={description} />

<script is:inline>
  function speedInsightsBeforeSend(data){
    console.log("Speed Insights before send", data)
    return data;
  }
</script>
<SpeedInsights />
```

**JavaScript (`BaseHead.astro`):**
```astro
---
import SpeedInsights from '@vercel/speed-insights/astro';
const { title, description } = Astro.props;
---
<title>{title}</title>
<meta name="title" content={title} />
<meta name="description" content={description} />

<script is:inline>
  function speedInsightsBeforeSend(data){
    console.log("Speed Insights before send", data)
    return data;
  }
</script>
<SpeedInsights />
```

[Learn more about `beforeSend`](https://vercel.com/docs/speed-insights/package#beforesend).

### Plain HTML

Add the following scripts before the closing tag of the `<body>`:

**HTML (`index.html`):**
```html
<script>
  window.si = window.si || function () { (window.siq = window.siq || []).push(arguments); };
</script>
<script defer src="/_vercel/speed-insights/script.js"></script>
```

### Other Frameworks

Import the `injectSpeedInsights` function from the package, which will add the tracking script to your app. **This should only be called once in your app, and must run in the client**.

Add the following code to your main app file:

**TypeScript (`main.ts`):**
```typescript
import { injectSpeedInsights } from "@vercel/speed-insights";

injectSpeedInsights();
```

**JavaScript (`main.js`):**
```javascript
import { injectSpeedInsights } from "@vercel/speed-insights";

injectSpeedInsights();
```

## Deploy to Vercel

### 3. Deploy your app to Vercel

You can deploy your app to Vercel's global [CDN](https://vercel.com/docs/cdn) by running the following command from your terminal:

```bash
vercel deploy
```

Alternatively, you can [connect your project's git repository](https://vercel.com/docs/git#deploying-a-git-repository), which will enable Vercel to deploy your latest pushes and merges to main.

Once your app is deployed, it's ready to begin tracking performance metrics.

> **💡 Note:** If everything is set up correctly, you should be able to find the `/_vercel/speed-insights/script.js` script inside the body tag of your page.

### 4. View your data in the dashboard

Once your app is deployed, and users have visited your site, you can view the data in the dashboard.

To do so, go to your [dashboard](https://vercel.com/dashboard), select your project, and click the **Speed Insights** tab.

After a few days of visitors, you'll be able to start exploring your metrics. For more information on how to use Speed Insights, see [Using Speed Insights](https://vercel.com/docs/speed-insights/using-speed-insights).

## Privacy and Compliance

Learn more about how Vercel supports [privacy and data compliance standards](https://vercel.com/docs/speed-insights/privacy-policy) with Vercel Speed Insights.

## Next steps

Now that you have Vercel Speed Insights set up, you can explore the following topics to learn more:

- [Learn how to use the `@vercel/speed-insights` package](https://vercel.com/docs/speed-insights/package)
- [Learn about metrics](https://vercel.com/docs/speed-insights/metrics)
- [Read about privacy and compliance](https://vercel.com/docs/speed-insights/privacy-policy)
- [Explore pricing](https://vercel.com/docs/speed-insights/limits-and-pricing)
- [Troubleshooting](https://vercel.com/docs/speed-insights/troubleshooting)

## Implementation Checklist

When implementing Vercel Speed Insights in your project:

1. ✅ Install dependencies using the project's package manager (npm, pnpm, yarn, or bun) to update lock files
2. ✅ Verify the build completes successfully
3. ✅ Run the linter to ensure no errors are introduced
4. ✅ Run tests if available to verify nothing breaks
5. ✅ Ensure all lock files (package-lock.json, pnpm-lock.yaml, yarn.lock, or bun.lockb) are updated
6. ✅ Preserve existing code structure and only add the necessary changes

## Additional Resources

- [Vercel Speed Insights Documentation](https://vercel.com/docs/speed-insights)
- [Vercel Speed Insights Package on npm](https://www.npmjs.com/package/@vercel/speed-insights)
- [Vercel Analytics Documentation](https://vercel.com/docs/analytics)
