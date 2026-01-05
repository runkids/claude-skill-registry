---
name: technical-seo
description: Implements Schema.org structured data for AndesRC articles. Adds ExercisePlan, HowTo, and FAQPage markup. Optimizes meta titles and descriptions. Use before publication.
metadata:
  author: AndesRC
  version: "1.0"
---

# Technical SEO

## Purpose
Implement structured data, optimize meta tags, and ensure technical SEO compliance for maximum search visibility and AI Overview eligibility.

## Meta Tag Optimization

### Title Tag
- **Length**: 50-60 characters
- **Format**: `[Primary Keyword] | [Benefit/Modifier] - Andes`
- **Example**: `Plan 10K Principiantes | 8 Semanas para tu Primera Carrera`

### Meta Description
- **Length**: 150-160 characters
- **Format**: `[Primary keyword]. [Key benefit]. [Call to action].`
- **Example**: `Plan de entrenamiento 10K para principiantes. Programa de 8 semanas con progresión gradual. ¡Descarga gratis y empieza hoy!`

### Frontmatter Checklist

```yaml
---
title: "Plan 10K Principiantes: Guía Completa 2025"  # 50-60 chars
description: "Plan de entrenamiento 10K para principiantes. 8 semanas de progresión gradual con consejos de nutrición. ¡Empieza hoy!"  # 150-160 chars
canonical: /es/blog/plan-10k-principiantes  # Full path
hreflang:
  es: /es/blog/plan-10k-principiantes
  en: /blog/10k-training-plan-beginners
---
```

## Schema.org Structured Data

### ExercisePlan (Training Plans)

```json
{
  "@context": "https://schema.org",
  "@type": "ExercisePlan",
  "name": "Plan de Entrenamiento 10K para Principiantes - AndesRC",
  "description": "Programa de 12 semanas diseñado para corredores novatos en CDMX, con énfasis en prevención de lesiones y adaptación a la altura.",
  "exerciseType": "Running",
  "activityDuration": "P12W",
  "activityFrequency": "3 days per week",
  "intensity": "Beginner",
  "audience": {
    "@type": "PeopleAudience",
    "audienceType": "Corredores principiantes",
    "geographicArea": {
      "@type": "Place",
      "name": "Mexico"
    }
  },
  "isAccessibleForFree": "True",
  "provider": {
    "@type": "Organization",
    "name": "AndesRC",
    "url": "https://andesrunners.com"
  }
}
```

### HowTo (Tutorials)

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "Cómo realizar un calentamiento dinámico para correr",
  "description": "Guía paso a paso para calentar correctamente antes de correr.",
  "step": [
    {
      "@type": "HowToStep",
      "name": "Caminata activa",
      "text": "Camina 2-3 minutos a paso ligero para elevar la temperatura corporal."
    },
    {
      "@type": "HowToStep",
      "name": "Rodillas altas",
      "text": "Realiza 20 repeticiones de rodillas altas alternando piernas."
    }
  ]
}
```

### FAQPage (BOFU/Sales Pages)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "¿Es un bot o una persona real?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Tu coach de AndesRC es una persona real apoyada por IA. Recibes respuestas rápidas gracias a la tecnología, pero siempre hay un humano supervisando tu progreso y ajustando tu plan."
      }
    },
    {
      "@type": "Question",
      "name": "¿Puedo cancelar cuando quiera?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí, puedes cancelar en cualquier momento directamente desde WhatsApp. Sin compromisos, sin penalizaciones."
      }
    }
  ]
}
```

## Internal Linking

### Requirements
- Minimum 2-3 internal links per article
- Link from satellite → pillar page
- Cross-link between related clusters

### Link Placement Strategy
1. **In introduction**: Link to pillar page
2. **In body**: Link to related satellite articles
3. **In conclusion**: Link to CTA (pricing, WhatsApp)

## Technical Checklist

- [ ] Meta title: 50-60 characters with primary keyword
- [ ] Meta description: 150-160 characters with CTA
- [ ] H1 matches title, contains primary keyword
- [ ] Schema.org JSON-LD added (ExercisePlan/HowTo/FAQPage as appropriate)
- [ ] Canonical URL set correctly
- [ ] Hreflang tags for bilingual content
- [ ] 2-3 internal links included
- [ ] Images have descriptive alt text with keywords
- [ ] URL slug is clean and keyword-rich

## Output

The article markdown with:
1. Optimized frontmatter
2. Schema.org JSON-LD script block
3. Internal links verified
