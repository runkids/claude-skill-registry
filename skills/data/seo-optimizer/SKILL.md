---
name: seo-optimizer
description: "Optimize SEO, metadata, structured data, and search engine visibility. Use this when the user asks about meta tags, Open Graph, Twitter Cards, Schema.org markup, sitemap.xml, robots.txt, social media previews, or improving search engine rankings."
allowed-tools: Read, Edit, Write, Grep, Glob
---

# SEO Optimizer Skill

This Skill helps optimize search engine visibility, metadata, and structured data for the IsLeapYear application.

## When to Use

- Adding or updating meta tags
- Configuring Open Graph and Twitter Cards
- Implementing Schema.org structured data
- Updating sitemap.xml configuration
- Modifying robots.txt rules
- Optimizing page titles and descriptions
- Improving social media previews

## SEO Configuration Files

### Root Layout (`src/app/layout.tsx`)

Base metadata configuration for the entire application:

```typescript
export const metadata: Metadata = {
  title: {
    default: "IsLeapYear - High-Performance Leap Year Detection API",
    template: "%s | IsLeapYear"
  },
  description: "Enterprise-grade leap year detection API...",
  keywords: ["leap year", "calendar", "API", "gregorian calendar"],
  authors: [{ name: "IsLeapYear Team" }],
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://isleapyear.app",
    siteName: "IsLeapYear",
    images: [{ url: "/og-image.png", width: 1200, height: 630 }]
  },
  twitter: {
    card: "summary_large_image",
    title: "IsLeapYear",
    description: "...",
    images: ["/twitter-image.png"]
  }
};
```

### Dynamic Sitemap (`src/app/sitemap.ts`)

Generates XML sitemap automatically:

```typescript
export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: 'https://isleapyear.app',
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 1,
    },
    // ... more routes
  ];
}
```

**Properties:**
- `url` - Full URL of the page
- `lastModified` - Last update date
- `changeFrequency` - How often the page changes
- `priority` - 0.0 to 1.0 (importance relative to other pages)

### Robots Configuration (`src/app/robots.ts`)

Controls search engine crawling:

```typescript
export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
      disallow: '/private/',
    },
    sitemap: 'https://isleapyear.app/sitemap.xml',
  };
}
```

### Web App Manifest (`src/app/manifest.ts`)

PWA configuration for mobile devices:

```typescript
export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'IsLeapYear',
    short_name: 'IsLeapYear',
    description: 'Leap year detection API',
    start_url: '/',
    display: 'standalone',
    background_color: '#ffffff',
    theme_color: '#000000',
    icons: [/* ... */],
  };
}
```

## Structured Data (Schema.org)

Located in `src/components/structured-data.tsx`

### Usage Pattern

```typescript
import { StructuredData } from "@/components/structured-data";
import type { WebPage, Organization } from "schema-dts";

const pageSchema: WebPage = {
  "@type": "WebPage",
  name: "Page Title",
  description: "Page description",
  url: "https://isleapyear.app/page",
};

// In your component:
<StructuredData data={pageSchema} />
```

### Common Schema Types

**WebPage:**
```typescript
{
  "@type": "WebPage",
  name: "Page Title",
  description: "Description",
  url: "https://isleapyear.app/page"
}
```

**Organization:**
```typescript
{
  "@type": "Organization",
  name: "IsLeapYear",
  url: "https://isleapyear.app",
  logo: "https://isleapyear.app/logo.png",
  sameAs: ["https://twitter.com/...", "https://github.com/..."]
}
```

**WebAPI:**
```typescript
{
  "@type": "WebAPI",
  name: "IsLeapYear API",
  description: "Leap year detection API",
  documentation: "https://isleapyear.app/docs"
}
```

**FAQPage:**
```typescript
{
  "@type": "FAQPage",
  mainEntity: [
    {
      "@type": "Question",
      name: "What is a leap year?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "A leap year is..."
      }
    }
  ]
}
```

## Page-Specific Metadata

Each page can export its own metadata:

```typescript
// src/app/docs/page.tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "API Documentation",
  description: "Complete API documentation for IsLeapYear",
  openGraph: {
    title: "API Documentation | IsLeapYear",
    description: "...",
  },
};
```

## SEO Best Practices

### 1. Title Tags
- Keep under 60 characters
- Include primary keyword
- Make it compelling for clicks
- Use template syntax for consistency

### 2. Meta Descriptions
- Keep between 150-160 characters
- Include call-to-action
- Use primary and secondary keywords naturally
- Unique for each page

### 3. Open Graph Images
- Dimensions: 1200 x 630 pixels
- File size: Under 1MB
- Format: PNG or JPEG
- Include branding and text overlay

### 4. Twitter Cards
- Use `summary_large_image` for rich previews
- Provide card-specific images (1200 x 628 pixels)
- Test with Twitter Card Validator

### 5. Structured Data
- Use schema-dts for type safety
- Validate with Google's Rich Results Test
- Include Organization schema on homepage
- Add WebAPI schema on API documentation

### 6. Sitemap
- Update `lastModified` when content changes
- Set appropriate `priority` (homepage = 1.0)
- Use realistic `changeFrequency`
- Include all public pages

## Testing SEO

### Tools
- **Google Search Console** - Monitor search performance
- **Google Rich Results Test** - Validate structured data
- **PageSpeed Insights** - Check Core Web Vitals
- **Twitter Card Validator** - Test Twitter previews
- **LinkedIn Post Inspector** - Test LinkedIn previews

### Local Testing

```bash
# View sitemap
curl http://localhost:3000/sitemap.xml

# View robots.txt
curl http://localhost:3000/robots.txt

# View manifest
curl http://localhost:3000/manifest.webmanifest

# Check meta tags
curl http://localhost:3000 | grep "<meta"
```

## Common Tasks

### 1. Adding a New Page to Sitemap

Edit `src/app/sitemap.ts`:

```typescript
{
  url: 'https://isleapyear.app/new-page',
  lastModified: new Date(),
  changeFrequency: 'weekly',
  priority: 0.8,
}
```

### 2. Updating Page Metadata

Create or update metadata in the page file:

```typescript
export const metadata: Metadata = {
  title: "New Page Title",
  description: "New description",
};
```

### 3. Adding Structured Data

1. Import types from schema-dts
2. Create schema object
3. Use StructuredData component

```typescript
import { StructuredData } from "@/components/structured-data";
import type { WebPage } from "schema-dts";

const schema: WebPage = { /* ... */ };

<StructuredData data={schema} />
```

## Important Notes

- All metadata uses Next.js built-in Metadata API
- Structured data uses schema-dts for type safety
- Images should be optimized (WebP format preferred)
- Test all changes with SEO validation tools
- Update sitemap when adding/removing pages
- Keep the satirical brand tone even in meta descriptions
- Domain: https://isleapyear.app (production)
