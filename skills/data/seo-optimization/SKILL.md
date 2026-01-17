# 🔍 SEO Optimization Skill

---
name: seo-optimization
description: Optimize web applications for search engines with meta tags, structured data, and performance
---

## 🎯 Purpose

Optimize เว็บไซต์สำหรับ search engines ด้วย meta tags, structured data, และ performance

## 📋 When to Use

- Launch new website
- Improve search rankings
- Audit existing site
- Content updates
- Performance optimization

## 🔧 Core SEO Elements

### Meta Tags
```html
<head>
  <title>Page Title - Site Name</title>
  <meta name="description" content="Description under 160 chars" />
  <meta name="keywords" content="keyword1, keyword2" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://example.com/page" />
  
  <!-- Open Graph -->
  <meta property="og:title" content="Title" />
  <meta property="og:description" content="Description" />
  <meta property="og:image" content="https://example.com/image.jpg" />
  <meta property="og:url" content="https://example.com/page" />
  
  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Title" />
</head>
```

### Next.js Implementation
```typescript
// app/layout.tsx
export const metadata = {
  title: {
    template: '%s | My Site',
    default: 'My Site',
  },
  description: 'Site description',
  openGraph: {
    title: 'My Site',
    description: 'Description',
    url: 'https://example.com',
    siteName: 'My Site',
    images: [{ url: '/og-image.jpg' }],
  },
};
```

### Structured Data
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "author": {
    "@type": "Person",
    "name": "Author Name"
  },
  "datePublished": "2024-01-15"
}
</script>
```

## 📊 SEO Checklist

### Technical
- [ ] Fast loading (<3s)
- [ ] Mobile-friendly
- [ ] HTTPS enabled
- [ ] XML sitemap
- [ ] robots.txt
- [ ] No broken links

### Content
- [ ] Unique titles per page
- [ ] Meta descriptions
- [ ] Header hierarchy (H1-H6)
- [ ] Alt text on images
- [ ] Internal linking
- [ ] Quality content

### Performance
- [ ] Image optimization
- [ ] Lazy loading
- [ ] Minified CSS/JS
- [ ] CDN usage
- [ ] Core Web Vitals pass

## 📝 Sitemap Template
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2024-01-15</lastmod>
    <priority>1.0</priority>
  </url>
</urlset>
```

## 🛠️ Tools

- Google Search Console
- Lighthouse
- PageSpeed Insights
- Schema Markup Validator

## ✅ Audit Checklist

- [ ] Title tags optimized
- [ ] Meta descriptions unique
- [ ] Images have alt text
- [ ] URLs are clean
- [ ] Page speed acceptable
- [ ] Mobile responsive
- [ ] Structured data valid

## 🔗 Related Skills

- `performance-optimization` - Speed improvements
- `accessibility-audit` - A11y helps SEO
- `documentation` - Content creation
