---
name: vue
description: Vue.js and Nuxt development patterns and best practices
license: MIT
compatibility: opencode
---

# Vue Skill

Comprehensive patterns and best practices for Vue.js 3 and Nuxt development.

## What I Know

### Composition API (Preferred)

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

// Reactive state
const count = ref(0)
const message = ref('Hello')

// Computed properties
const doubled = computed(() => count.value * 2)

// Methods
function increment() {
  count.value++
}

// Lifecycle hooks
onMounted(() => {
  console.log('Component mounted')
})
</script>

<template>
  <div>{{ message }}: {{ count }}</div>
  <button @click="increment">Increment</button>
</template>
```

### Options API (Legacy)

```vue
<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'MyComponent',
  props: {
    value: String
  },
  data() {
    return {
      count: 0
    }
  },
  computed: {
    doubled() {
      return this.count * 2
    }
  },
  methods: {
    increment() {
      this.count++
    }
  }
})
</script>
```

### Nuxt 3 Specifics

**Auto-imports**
```vue
<script setup>
// No imports needed for ref, computed, onMounted, etc.
const count = ref(0)

// useFetch, useAsyncData also auto-imported
const { data } = await useFetch('/api/items')
</script>
```

**Server vs Client Components**
```vue
<!-- Client component (default) -->
<script setup>
const clientData = ref('client only')
</script>

<!-- Server component -->
<script setup>
serverData.value = 'server only'
</script>

<!-- Hybrid with defineComponent -->
<script setup>
const { data } = await useFetch('/api/data') // Server only
const clientState = ref('client') // Client only
</script>
```

**API Routes**
```ts
// server/api/hello.ts
export default defineEventHandler(async (event) => {
  const query = getQuery(event)
  const body = await readBody(event)
  return { hello: 'world' }
})
```

### TypeScript Patterns

**Props Typing**
```vue
<script setup lang="ts">
interface Props {
  title: string
  count?: number
  items: string[]
}

// withDefaults for optional props
const props = withDefaults(defineProps<Props>(), {
  count: 0
})

// Emits typing
const emit = defineEmits<{
  update: [value: string]
  delete: [id: number]
}>()
</script>
```

**Reactive Types**
```ts
import { ref, reactive, computed } from 'vue'

interface User {
  id: number
  name: string
}

// Ref with type
const user = ref<User | null>(null)

// Reactive with type
const state = reactive<{
  users: User[]
  loading: boolean
}>({ users: [], loading: true })

// Computed return type
const userCount = computed((): number => state.users.length)
```

### Pinia State Management

**Store Definition**
```ts
// stores/user.ts
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User | null,
    isAuthenticated: false
  }),

  getters: {
    userId: (state) => state.user?.id ?? null
  },

  actions: {
    async login(credentials) {
      const user = await api.login(credentials)
      this.user = user
      this.isAuthenticated = true
    },
    logout() {
      this.user = null
      this.isAuthenticated = false
    }
  }
})
```

**Using Store**
```vue
<script setup>
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
</script>

<template>
  <div v-if="userStore.isAuthenticated">
    {{ userStore.user.name }}
  </div>
</template>
```

### Components

**Props and Emits**
```vue
<script setup lang="ts">
interface Props {
  modelValue: string
  placeholder?: string
}

interface Emits {
  'update:modelValue': [value: string]
  'submit': []
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

function update(value: string) {
  emit('update:modelValue', value)
}
</script>

<template>
  <input
    :value="modelValue"
    :placeholder="placeholder"
    @input="update($event.target.value)"
  />
</template>
```

**Slots**
```vue
<!-- Parent -->
<template>
  <MyComponent>
    <template #default="{ item }">
      {{ item.name }}
    </template>
    <template #header>
      <h1>Header</h1>
    </template>
  </MyComponent>
</template>

<!-- Child -->
<script setup>
defineSlots<{
  default?: (props: { item: Item }) => any
  header?: () => any
}>()
</script>

<template>
  <div>
    <slot name="header" />
    <slot v-for="item in items" :item="item" />
  </div>
</template>
```

### Composables

**Custom Composable**
```ts
// composables/useFetch.ts
export function useFetch<T>(url: string) {
  const data = ref<T | null>(null)
  const error = ref<Error | null>(null)
  const loading = ref(false)

  async function fetch() {
    loading.value = true
    try {
      data.value = await $fetch<T>(url)
    } catch (e) {
      error.value = e as Error
    } finally {
      loading.value = false
    }
  }

  fetch()

  return { data, error, loading, refetch: fetch }
}
```

**Using Composable**
```vue
<script setup>
const { data, loading, error } = useFetch<User>('/api/user')
</script>
```

### Directives

**Custom Directives**
```ts
// directives/clickOutside.ts
export const vClickOutside = {
  mounted(el, binding) {
    el.clickOutsideEvent = (event: Event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event)
      }
    }
    document.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent)
  }
}
```

### Routing (Vue Router)

```ts
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: () => import('@/views/Home.vue') },
  { path: '/about', component: () => import('@/views/About.vue') },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})
```

### Nuxt File Routing

```
pages/
├── index.vue           # /
├── about.vue           # /about
├── users/
│   ├── index.vue       # /users
│   └── [id].vue        # /users/:id
└── [...slug].vue       # /users/:slug(maybe)
```

### Styling

**Scoped Styles**
```vue
<style scoped>
.container {
  padding: 1rem;
}
</style>
```

**CSS Modules**
```vue
<template>
  <div :class="$style.container">Content</div>
</template>

<style module>
.container {
  padding: 1rem;
}
</style>
```

**UnoCSS / Tailwind**
```vue
<template>
  <div class="flex items-center justify-between p-4">
    Content
  </div>
</template>
```

### Common Pitfalls

1. **Mutating props directly** → Use emit to update parent
2. **Not using `key` in v-for** → Always use unique keys
3. **Deep reactivity issues** → Use `reactive()` carefully with objects
4. **Async setup** → Use `<Suspense>` for async components
5. **Missing `v-bind` shorthand** → Use `:` for bindings

### File Conventions

```
src/
├── components/       # Auto-imported components
├── composables/      # Auto-imported composables
├── pages/            # File-based routing (Nuxt)
├── server/           # Server routes (Nuxt)
├── stores/           # Pinia stores (auto-imported)
├── types/            # TypeScript types
├── utils/            # Utility functions (auto-imported)
└── assets/           # Static assets
```

---

*Part of SuperAI GitHub - Centralized OpenCode Configuration*
