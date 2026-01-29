---
name: store
description: Generate Zustand stores following established patterns. Use when creating state management, global stores, persisted stores, or managing app-wide data.
---

# Store Generator

Generate Zustand stores with AsyncStorage persistence following established patterns.

## Directory Structure

```
src/
├── store/
│   ├── index.ts              # Store exports
│   ├── useMyStore.ts         # Domain store
│   ├── useAppSettingsStore.ts
│   └── useBiometricAuthStore.ts
├── types/
│   └── store.ts              # Store types
└── lib/
    └── store-utils.ts        # Migrations & preprocessing
```

## Basic Store Pattern

```tsx
// src/store/useItemStore.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface Item {
  id: string;
  title: string;
  createdAt: string;
}

interface ItemStore {
  // State
  items: Record<string, Item>;
  isLoading: boolean;

  // Actions
  createItem: (title: string) => string;
  updateItem: (id: string, updates: Partial<Item>) => void;
  deleteItem: (id: string) => void;
  getItem: (id: string) => Item | undefined;
}

export const useItemStore = create<ItemStore>()(
  persist(
    (set, get) => ({
      items: {},
      isLoading: false,

      createItem: (title) => {
        const id = `item_${Date.now()}`;
        const newItem: Item = {
          id,
          title,
          createdAt: new Date().toISOString(),
        };

        set((state) => ({
          items: { ...state.items, [id]: newItem },
        }));

        return id;
      },

      updateItem: (id, updates) => {
        set((state) => ({
          items: {
            ...state.items,
            [id]: { ...state.items[id], ...updates },
          },
        }));
      },

      deleteItem: (id) => {
        set((state) => {
          const { [id]: removed, ...rest } = state.items;
          return { items: rest };
        });
      },

      getItem: (id) => get().items[id],
    }),
    {
      name: 'item-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
```

## Store with Migrations

```tsx
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

const STORE_VERSION = 3;

// Migration functions
const migrateFromV1ToV2 = (state: any) => {
  // Add new field with default value
  return {
    ...state,
    items: Object.fromEntries(
      Object.entries(state.items).map(([id, item]: [string, any]) => [
        id,
        { ...item, newField: 'default' },
      ])
    ),
  };
};

const migrateFromV2ToV3 = (state: any) => {
  // Rename field
  return {
    ...state,
    items: Object.fromEntries(
      Object.entries(state.items).map(([id, item]: [string, any]) => {
        const { oldField, ...rest } = item;
        return [id, { ...rest, renamedField: oldField }];
      })
    ),
  };
};

const migrationMap = new Map<number, (state: any) => any>([
  [2, migrateFromV1ToV2],
  [3, migrateFromV2ToV3],
]);

export const useItemStore = create<ItemStore>()(
  persist(
    (set, get) => ({
      // ... state and actions
    }),
    {
      name: 'item-storage',
      version: STORE_VERSION,
      storage: createJSONStorage(() => AsyncStorage),
      migrate: (persistedState, version) => {
        let state = persistedState as any;
        for (let v = version + 1; v <= STORE_VERSION; v++) {
          if (migrationMap.has(v)) {
            state = migrationMap.get(v)!(state);
          }
        }
        return state;
      },
      onRehydrateStorage: () => (state) => {
        if (state) {
          // Preprocess data after rehydration
          state.items = preprocessItems(state.items);
        }
      },
    }
  )
);
```

## App Settings Store

```tsx
// src/store/useAppSettingsStore.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface AppSettingsStore {
  // State
  hasCompletedOnboarding: boolean;
  hasAcceptedTerms: boolean;
  acceptedTermsVersion: string | null;
  mainCurrency: string;
  hasSeenRateAppPrompt: boolean;

  // Actions
  setHasCompletedOnboarding: (value: boolean) => void;
  setHasAcceptedTerms: (value: boolean, version: string) => void;
  setMainCurrency: (currency: string) => void;
  setHasSeenRateAppPrompt: (value: boolean) => void;
}

export const useAppSettingsStore = create<AppSettingsStore>()(
  persist(
    (set) => ({
      hasCompletedOnboarding: false,
      hasAcceptedTerms: false,
      acceptedTermsVersion: null,
      mainCurrency: 'USD',
      hasSeenRateAppPrompt: false,

      setHasCompletedOnboarding: (value) => set({ hasCompletedOnboarding: value }),
      setHasAcceptedTerms: (value, version) =>
        set({ hasAcceptedTerms: value, acceptedTermsVersion: version }),
      setMainCurrency: (currency) => set({ mainCurrency: currency }),
      setHasSeenRateAppPrompt: (value) => set({ hasSeenRateAppPrompt: value }),
    }),
    {
      name: 'app-settings-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
```

## Biometric Auth Store

```tsx
// src/store/useBiometricAuthStore.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as LocalAuthentication from 'expo-local-authentication';

type BiometricType = 'fingerprint' | 'facial' | 'iris';

interface BiometricAuthStore {
  isAuthenticated: boolean;
  isBiometricAvailable: boolean;
  biometricType: BiometricType | null;
  biometricEnabled: boolean;

  authenticate: () => Promise<void>;
  setBiometricEnabled: (enabled: boolean) => void;
  checkAndSetBiometricAvailability: () => Promise<void>;
  setIsAuthenticated: (value: boolean) => void;
}

export const useBiometricAuthStore = create<BiometricAuthStore>()(
  persist(
    (set, get) => ({
      isAuthenticated: false,
      isBiometricAvailable: false,
      biometricType: null,
      biometricEnabled: false,

      authenticate: async () => {
        const { biometricEnabled, isBiometricAvailable } = get();

        if (!biometricEnabled || !isBiometricAvailable) {
          set({ isAuthenticated: true });
          return;
        }

        const result = await LocalAuthentication.authenticateAsync({
          promptMessage: 'Authenticate to continue',
          fallbackLabel: 'Use passcode',
        });

        set({ isAuthenticated: result.success });
      },

      setBiometricEnabled: (enabled) => set({ biometricEnabled: enabled }),

      checkAndSetBiometricAvailability: async () => {
        const hasHardware = await LocalAuthentication.hasHardwareAsync();
        const isEnrolled = await LocalAuthentication.isEnrolledAsync();
        const supportedTypes = await LocalAuthentication.supportedAuthenticationTypesAsync();

        let biometricType: BiometricType | null = null;
        if (supportedTypes.includes(LocalAuthentication.AuthenticationType.FACIAL_RECOGNITION)) {
          biometricType = 'facial';
        } else if (supportedTypes.includes(LocalAuthentication.AuthenticationType.FINGERPRINT)) {
          biometricType = 'fingerprint';
        }

        set({
          isBiometricAvailable: hasHardware && isEnrolled,
          biometricType,
        });
      },

      setIsAuthenticated: (value) => set({ isAuthenticated: value }),
    }),
    {
      name: 'biometric-auth-storage',
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({
        biometricEnabled: state.biometricEnabled,
      }),
    }
  )
);
```

## Store with Array Operations

```tsx
interface ScheduleStore {
  items: Item[];

  addItem: (item: Omit<Item, 'id'>) => void;
  removeItem: (index: number) => void;
  updateItem: (index: number, updates: Partial<Item>) => void;
  reorderItems: (fromIndex: number, toIndex: number) => void;
}

export const useScheduleStore = create<ScheduleStore>()(
  persist(
    (set) => ({
      items: [],

      addItem: (item) =>
        set((state) => ({
          items: [...state.items, { ...item, id: `item_${Date.now()}` }],
        })),

      removeItem: (index) =>
        set((state) => ({
          items: state.items.filter((_, i) => i !== index),
        })),

      updateItem: (index, updates) =>
        set((state) => ({
          items: state.items.map((item, i) =>
            i === index ? { ...item, ...updates } : item
          ),
        })),

      reorderItems: (fromIndex, toIndex) =>
        set((state) => {
          const items = [...state.items];
          const [removed] = items.splice(fromIndex, 1);
          items.splice(toIndex, 0, removed);
          return { items };
        }),
    }),
    {
      name: 'schedule-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
```

## Non-Persisted Store (Transient State)

```tsx
// For screen-level state that doesn't need persistence
interface UIStore {
  activeTabIndex: number;
  selectedItemId: string | null;
  isModalOpen: boolean;

  setActiveTabIndex: (index: number) => void;
  setSelectedItemId: (id: string | null) => void;
  setIsModalOpen: (open: boolean) => void;
  reset: () => void;
}

const initialState = {
  activeTabIndex: 0,
  selectedItemId: null,
  isModalOpen: false,
};

export const useUIStore = create<UIStore>((set) => ({
  ...initialState,

  setActiveTabIndex: (index) => set({ activeTabIndex: index }),
  setSelectedItemId: (id) => set({ selectedItemId: id }),
  setIsModalOpen: (open) => set({ isModalOpen: open }),
  reset: () => set(initialState),
}));
```

## Store Exports

```tsx
// src/store/index.ts
export { useItemStore } from './useItemStore';
export { useAppSettingsStore } from './useAppSettingsStore';
export { useBiometricAuthStore } from './useBiometricAuthStore';
```

## Usage in Components

```tsx
import { useItemStore } from '@/store';

const MyComponent = () => {
  // Select specific state (prevents unnecessary re-renders)
  const items = useItemStore((state) => state.items);
  const createItem = useItemStore((state) => state.createItem);

  // Or destructure multiple values
  const { items, createItem, deleteItem } = useItemStore();

  const handleCreate = () => {
    const id = createItem('New Item');
    console.log('Created:', id);
  };

  return (
    <Button title="Create" onPress={handleCreate} />
  );
};
```

## Async Actions Pattern

```tsx
interface DataStore {
  data: Data[];
  isLoading: boolean;
  error: string | null;

  fetchData: () => Promise<void>;
  saveData: (data: Data) => Promise<void>;
}

export const useDataStore = create<DataStore>((set, get) => ({
  data: [],
  isLoading: false,
  error: null,

  fetchData: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.fetchData();
      set({ data: response, isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },

  saveData: async (data) => {
    set({ isLoading: true });
    try {
      await api.saveData(data);
      set((state) => ({
        data: [...state.data, data],
        isLoading: false,
      }));
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },
}));
```

## Checklist

- [ ] Store file in `src/store/useXxxStore.ts`
- [ ] TypeScript interface for state and actions
- [ ] `persist` middleware with AsyncStorage
- [ ] `version` and `migrate` for schema changes
- [ ] `partialize` for selective persistence
- [ ] Exported from `src/store/index.ts`
- [ ] Actions use immutable updates
- [ ] Selector pattern in components
