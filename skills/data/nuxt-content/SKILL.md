---
name: nuxt-content
description: Expert knowledge for @nuxt/content module in Nuxt 4. Activate when working with content directory, markdown files, frontmatter, or ContentRenderer.
---

# Nuxt Content Expertise (Nuxt 4)

## Activation Triggers
- Creating/editing files in `content/` directory
- Working with markdown frontmatter
- Using `queryContent()` composable
- Rendering content with `<ContentRenderer>`
- Building navigation from content

## Nuxt 4 Specifics

Nuxt 4 uses the `app/` directory structure:
```
project/
├── app/
│   ├── components/
│   ├── pages/
│   └── ...
├── content/           # Content stays at root level
│   └── ...
└── nuxt.config.ts
```

## Content Directory Structure

```
content/
├── 1.phase-1-sdlc/
│   ├── _dir.yml                  # Directory metadata (optional)
│   ├── 1.sdlc-models/
│   │   ├── _dir.yml
│   │   ├── 1.waterfall-model.md
│   │   ├── 2.agile-methodology.md
│   │   └── 3.scrum-framework.md
│   └── 2.sdlc-phases/
│       └── ...
└── 2.phase-2-foundations/
    └── ...
```

**Naming Convention**: 
- Numeric prefixes (1., 2.) control ordering
- Prefixes are stripped from URLs
- Use kebab-case for slugs

## Frontmatter Schema

```yaml
---
title: "Lesson Title"
description: "Brief description for SEO and previews"
estimatedMinutes: 15
difficulty: beginner | intermediate | advanced
learningObjectives:
  - "Objective 1"
  - "Objective 2"
quiz:
  passingScore: 70
  questions:
    - question: "Question text"
      type: single | multiple | true-false
      options: ["A", "B", "C", "D"]
      correctAnswer: "A"
      explanation: "Why this is correct"
---

# Content starts here
```

## Nuxt Config

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  compatibilityVersion: 4,
  modules: ['@nuxt/content', '@nuxt/ui'],
  
  content: {
    highlight: {
      theme: 'github-dark',
      langs: ['bash', 'typescript', 'javascript', 'python', 'yaml', 'dockerfile', 'json', 'sql']
    },
    markdown: {
      toc: {
        depth: 3,
        searchDepth: 3
      }
    }
  }
})
```

## Querying Content

### Get Single Document
```typescript
const route = useRoute()

// Using path from route
const { data: lesson } = await useAsyncData(
  `lesson-${route.path}`,
  () => queryContent(route.path).findOne()
)

// Explicit path
const { data: lesson } = await useAsyncData('waterfall', () =>
  queryContent('phase-1-sdlc/sdlc-models/waterfall-model').findOne()
)
```

### Get All Documents in Directory
```typescript
const { data: lessons } = await useAsyncData('sdlc-lessons', () =>
  queryContent('phase-1-sdlc/sdlc-models')
    .where({ _extension: 'md' })
    .sort({ _path: 1 })
    .find()
)
```

### Get Navigation Tree
```typescript
const { data: navigation } = await useAsyncData('navigation', () =>
  fetchContentNavigation()
)

// Or for specific path
const { data: phaseNav } = await useAsyncData('phase-nav', () =>
  fetchContentNavigation(queryContent('phase-1-sdlc'))
)
```

### Previous/Next Navigation
```typescript
const { data: surround } = await useAsyncData('surround', () =>
  queryContent()
    .only(['_path', 'title'])
    .sort({ _path: 1 })
    .findSurround(route.path)
)

const [prev, next] = surround.value || [null, null]
```

### Query with Filters
```typescript
// By difficulty
const { data: beginnerLessons } = await useAsyncData('beginner', () =>
  queryContent()
    .where({ difficulty: 'beginner' })
    .find()
)

// By field existence
const { data: withQuiz } = await useAsyncData('with-quiz', () =>
  queryContent()
    .where({ 'quiz': { $exists: true } })
    .find()
)

// Count documents
const count = await queryContent('phase-1-sdlc').count()
```

## Rendering Content

### Basic Rendering
```vue
<template>
  <div v-if="lesson" class="prose prose-invert">
    <ContentRenderer :value="lesson" />
  </div>
</template>
```

### With ContentDoc Component
```vue
<template>
  <ContentDoc :path="path">
    <template #default="{ doc }">
      <article>
        <h1>{{ doc.title }}</h1>
        <div class="prose prose-invert">
          <ContentRenderer :value="doc" />
        </div>
      </article>
    </template>
    
    <template #not-found>
      <div>Lesson not found</div>
    </template>
    
    <template #empty>
      <div>No content available</div>
    </template>
  </ContentDoc>
</template>
```

### Table of Contents
```vue
<template>
  <nav v-if="lesson?.body?.toc?.links">
    <ul>
      <li v-for="link in lesson.body.toc.links" :key="link.id">
        <a :href="`#${link.id}`">{{ link.text }}</a>
        <ul v-if="link.children">
          <li v-for="child in link.children" :key="child.id">
            <a :href="`#${child.id}`">{{ child.text }}</a>
          </li>
        </ul>
      </li>
    </ul>
  </nav>
</template>
```

## Prose Styling

Use Tailwind Typography for content styling:

```vue
<div class="prose prose-invert prose-lg max-w-none">
  <ContentRenderer :value="lesson" />
</div>
```

Customize prose in Tailwind config if needed:
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      typography: {
        invert: {
          css: {
            '--tw-prose-body': 'var(--color-gray-300)',
            '--tw-prose-headings': 'var(--color-gray-100)',
            // ... more customizations
          }
        }
      }
    }
  }
}
```

## Common Patterns

### Loading State
```vue
<template>
  <div v-if="pending">
    <USkeleton class="h-8 w-64 mb-4" />
    <USkeleton class="h-4 w-full mb-2" />
    <USkeleton class="h-4 w-3/4" />
  </div>
  <div v-else-if="error">
    <p>Error loading content</p>
  </div>
  <div v-else-if="lesson">
    <ContentRenderer :value="lesson" />
  </div>
</template>
```

### Dynamic Routes
```
app/pages/[phase]/[topic]/[subtopic].vue
```

```typescript
const route = useRoute()
const { phase, topic, subtopic } = route.params as {
  phase: string
  topic: string
  subtopic: string
}

const contentPath = `${phase}/${topic}/${subtopic}`
```

## Key Differences from Nuxt 3

1. App directory is `app/` not root
2. Use `compatibilityVersion: 4` in config
3. Content module works the same way
4. Query syntax unchanged
5. ContentRenderer unchanged

## Gotchas

- Use `_path` not `path` for internal content paths
- Numeric prefixes are stripped from URLs (1.topic becomes /topic)
- Use `_dir.yml` for directory-level metadata
- Always use `useAsyncData` for SSR compatibility
- The `$exists` filter checks if a field exists
