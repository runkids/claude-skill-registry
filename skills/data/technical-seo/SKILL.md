---
name: technical-seo
description: Final SEO audit and technical implementation. Use at the END of a project to verify all pages, implement technical SEO (sitemap.xml, robots.txt, schema), and check for ranking readiness. Triggers on "SEO audit", "final SEO check", "verify SEO", "implement technical SEO".
---

# SEO Implementation & Audit

Final technical SEO implementation and comprehensive audit.

## Prerequisites

- All pages built and content optimized
- docs/sitemap.md and docs/seo-strategy.md exist

## Workflow

1. **Audit All Pages** - Check every page for SEO requirements
2. **Generate Technical Files** - sitemap.xml, robots.txt
3. **Add Schema.org** - JSON-LD structured data
4. **Configure Social** - Open Graph, Twitter cards
5. **Final Verification** - Comprehensive checklist

## Full Site Audit Checklist

### Per-Page Verification

For EACH page in docs/sitemap.md, verify:

**Content:**
- [ ] H1 contains primary keyword
- [ ] Only ONE H1 per page
- [ ] H2/H3 include secondary keywords
- [ ] Keyword density 1-2%
- [ ] Minimum 300 words content

**Meta Tags:**
- [ ] Title tag 50-60 characters
- [ ] Title contains primary keyword
- [ ] Meta description 150-160 characters
- [ ] Meta description has CTA

**Images:**
- [ ] All images have alt text
- [ ] Alt text is keyword-relevant
- [ ] Images are optimized (WebP)

**Links:**
- [ ] Internal links to key pages
- [ ] No broken links
- [ ] Anchor text is descriptive

### Technical SEO Files

#### sitemap.xml (app/sitemap.ts)

```typescript
import { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://domain.com'

  return [
    { url: baseUrl, lastModified: new Date(), changeFrequency: 'weekly', priority: 1 },
    { url: `${baseUrl}/leistungen`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.8 },
    // All pages from docs/sitemap.md
  ]
}
```

#### robots.txt (public/robots.txt)

```
User-agent: *
Allow: /
Disallow: /api/
Disallow: /_next/

Sitemap: https://domain.com/sitemap.xml
```

### Schema.org Structured Data

Add to layout or pages:

**LocalBusiness (Homepage):**
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Company Name",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Street",
    "addressLocality": "Zürich",
    "postalCode": "8000",
    "addressCountry": "CH"
  },
  "telephone": "+41 XX XXX XX XX",
  "url": "https://domain.com",
  "priceRange": "$$"
}
```

**Service (Service Pages):**
```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Webdesign",
  "provider": { "@type": "LocalBusiness", "name": "Company" },
  "areaServed": "Zürich",
  "description": "Service description"
}
```

**FAQPage (FAQ Sections):**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Question?",
    "acceptedAnswer": { "@type": "Answer", "text": "Answer" }
  }]
}
```

### Open Graph & Twitter

Add to page metadata:

```typescript
export const metadata: Metadata = {
  title: 'Page Title | Brand',
  description: 'Description with keyword',
  openGraph: {
    title: 'Page Title | Brand',
    description: 'Description',
    url: 'https://domain.com/page',
    siteName: 'Brand',
    images: [{ url: '/og-image.png', width: 1200, height: 630 }],
    locale: 'de_CH',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Page Title',
    description: 'Description',
    images: ['/og-image.png'],
  },
}
```

## Final Ranking Checklist

**Technical:**
- [ ] sitemap.xml generated and accessible
- [ ] robots.txt allows crawling
- [ ] SSL certificate active (HTTPS)
- [ ] Mobile responsive
- [ ] Page speed < 3 seconds
- [ ] No console errors

**Content:**
- [ ] All pages have unique title tags
- [ ] All pages have unique meta descriptions
- [ ] All H1s are unique and keyword-optimized
- [ ] No duplicate content
- [ ] No thin content (< 300 words)

**Structured Data:**
- [ ] LocalBusiness schema on homepage
- [ ] Service schema on service pages
- [ ] FAQPage schema on FAQ sections
- [ ] BreadcrumbList schema (optional)

**Social:**
- [ ] Open Graph images created (1200x630)
- [ ] OG tags on all pages
- [ ] Twitter card tags on all pages

## Output

- app/sitemap.ts created
- public/robots.txt created
- Schema.org components added
- OG images configured
- All pages verified for SEO compliance
