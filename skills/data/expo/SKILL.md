---
name: expo
description: Expo framework for React Native development with EAS Build, managed workflow, and OTA updates
license: MIT
compatibility: opencode
---

# Expo Skill

Comprehensive patterns and best practices for Expo and React Native development.

## What I Know

### Project Structure

```
app/                    # Expo Router file-based routing
├── (auth)/
│   ├── login.tsx
│   └── _layout.tsx
├── (tabs)/
│   ├── index.tsx
│   ├── settings.tsx
│   └── _layout.tsx
├── _layout.tsx
components/            # Shared components
constants/             # App constants
hooks/                 # Custom hooks
assets/                # Images, fonts, icons
utils/                 # Helper functions
types/                 # TypeScript types
```

### Expo CLI Commands

```bash
# Create new project
npx create-expo-app my-app
npx create-expo-app my-app --template blank-typescript

# Start development server
npx expo start
npx expo start --clear  # Clear cache
npx expo start --tunnel # Tunnel for external access

# Run on device/simulator
npx expo start --ios
npx expo start --android
npx expo start --web

# Install dependencies
npx expo install expo-module
npm install package-name
npx expo install react-native-safe-area-context

# Build
eas build --platform ios
eas build --platform android
eas build --platform all

# Submit to stores
eas submit --platform ios
eas submit --platform android

# Updates
eas update --branch production --message "Fix login bug"
```

### Configuration

**app.json (Expo config)**
```json
{
  "expo": {
    "name": "MyApp",
    "slug": "my-app",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    },
    "updates": {
      "url": "https://u.expo.dev/PROJECT_ID"
    },
    "assetBundlePatterns": [
      "**/*"
    ],
    "ios": {
      "bundleIdentifier": "com.company.myapp",
      "buildNumber": "1",
      "supportsTablet": true,
      "config": {
        "googleSignIn": {
          "reservedClientId": "REVERSED_CLIENT_ID"
        }
      }
    },
    "android": {
      "package": "com.company.myapp",
      "versionCode": 1,
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#ffffff"
      },
      "permissions": [
        "INTERNET",
        "ACCESS_FINE_LOCATION"
      ]
    },
    "extra": {
      "eas": {
        "projectId": "PROJECT_ID"
      }
    },
    "plugins": [
      "expo-secure-store",
      [
        "expo-splash-screen",
        {
          "backgroundColor": "#ffffff",
          "image": "./assets/splash.png"
        }
      ]
    ]
  }
}
```

**app.config.js (Dynamic config)**
```js
const config = {
  name: 'MyApp',
  slug: 'my-app',
  version: '1.0.0',
  orientation: 'portrait',
  icon: './assets/icon.png',
  splash: {
    image: './assets/splash.png',
    resizeMode: 'contain',
    backgroundColor: '#ffffff',
  },
  updates: {
    url: 'https://u.expo.dev/PROJECT_ID',
  },
  assetBundlePatterns: ['**/*'],
  ios: {
    bundleIdentifier: 'com.company.myapp',
    supportsTablet: true,
  },
  android: {
    package: 'com.company.myapp',
    adaptiveIcon: {
      foregroundImage: './assets/adaptive-icon.png',
      backgroundColor: '#ffffff',
    },
  },
  extra: {
    eas: {
      projectId: process.env.EAS_PROJECT_ID,
    },
    apiUrl: process.env.API_URL,
  },
}

export default config
```

### Expo Router

**File-Based Routing Structure**
```
app/
├── _layout.tsx          # Root layout
├── index.tsx            # Home screen (/)
├── about.tsx            # About screen (/about)
├── (auth)/              # Auth route group
│   ├── _layout.tsx      # Auth layout (no tab bar)
│   ├── login.tsx        # /login
│   └── register.tsx     # /register
├── (tabs)/              # Tabs route group
│   ├── _layout.tsx      # Tabs layout with tab bar
│   ├── index.tsx        # / (home tab)
│   ├── profile.tsx      # /profile
│   └── settings.tsx     # /settings
└── [id].tsx             # Dynamic route (/123)
```

**Root Layout**
```tsx
// app/_layout.tsx
import { Stack } from 'expo-router'
import { StatusBar } from 'expo-status-bar'

export default function RootLayout() {
  return (
    <>
      <StatusBar style="auto" />
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="index" options={{ title: 'Home' }} />
        <Stack.Screen name="about" options={{ title: 'About' }} />
      </Stack>
    </>
  )
}
```

**Tabs Layout**
```tsx
// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router'
import { Ionicons } from '@expo/vector-icons'

export default function TabsLayout() {
  return (
    <Tabs screenOptions={{ headerShown: false }}>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="home" size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="person" size={size} color={color} />
          ),
        }}
      />
    </Tabs>
  )
}
```

**Navigation in Expo Router**
```tsx
// app/profile.tsx
import { useRouter } from 'expo-router'
import { Button } from 'react-native'

export default function ProfileScreen() {
  const router = useRouter()

  return (
    <Button
      title="Go to Settings"
      onPress={() => router.push('/settings')}
    />
  )
}
```

### Development Builds

**Setup Development Build**
```bash
# Initialize EAS
npx eas-cli init

# Create development build
eas build --profile development --platform ios

# Run development build
npx expo run:ios
npx expo run:android
```

**eas.json Configuration**
```json
{
  "cli": {
    "version": ">= 5.2.0"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": {
        "resourceClass": "m-medium"
      },
      "android": {
        "resourceClass": "medium"
      }
    },
    "preview": {
      "distribution": "internal",
      "ios": {
        "resourceClass": "m-medium"
      },
      "android": {
        "resourceClass": "medium"
      }
    },
    "production": {
      "ios": {
        "autoIncrement": true
      },
      "android": {
        "autoIncrement": true
      }
    }
  },
  "submit": {
    "production": {}
  }
}
```

### EAS Build

**Build Profiles**
```json
{
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal",
      "ios": {
        "simulator": true
      }
    },
    "production": {
      "ios": {
        "autoIncrement": true
      },
      "android": {
        "autoIncrement": true
      }
    }
  }
}
```

**Build Commands**
```bash
# Development build
eas build --profile development --platform ios

# Preview build (internal testing)
eas build --profile preview --platform all

# Production build
eas build --profile production --platform all

# Local build
eas build --local --platform ios
```

### EAS Update (OTA)

**Update Configuration**
```json
{
  "updates": {
    "url": "https://u.expo.dev/PROJECT_ID"
  }
}
```

**Publishing Updates**
```bash
# Configure update channels
eas update:configure

# Branches
eas branch:create production
eas branch:create preview

# Publish update
eas update --branch production --message "Fix crash on login"

# List updates
eas update:list

# Rollback
eas update:rollback --branch production
```

**Runtime Update Policy**
```tsx
import * as Updates from 'expo-updates'

export default function App() {
  useEffect(() => {
    async function checkForUpdates() {
      try {
        const update = await Updates.checkForUpdateAsync()
        if (update.isAvailable) {
          await Updates.fetchUpdateAsync()
          await Updates.reloadAsync()
        }
      } catch (error) {
        console.log('Error checking for updates:', error)
      }
    }
    checkForUpdates()
  }, [])
}
```

### Expo Modules & APIs

**expo-secure-store**
```tsx
import * as SecureStore from 'expo-secure-store'

// Save data
await SecureStore.setItemAsync('token', 'your-auth-token')

// Get data
const token = await SecureStore.getItemAsync('token')

// Delete data
await SecureStore.deleteItemAsync('token')

// With options
await SecureStore.setItemAsync('key', 'value', {
  keychainAccessible: SecureStore.WHEN_UNLOCKED,
})
```

**expo-font**
```tsx
import { useFonts } from 'expo-font'
import { SplashScreen } from 'expo-splash-screen'
import { useEffect } from 'react'

export default function App() {
  const [fontsLoaded] = useFonts({
    'Inter-Regular': require('./assets/fonts/Inter-Regular.ttf'),
    'Inter-Bold': require('./assets/fonts/Inter-Bold.ttf'),
  })

  useEffect(() => {
    async function prepare() {
      await SplashScreen.preventAutoHideAsync()
    }
    prepare()
  }, [])

  useEffect(() => {
    if (fontsLoaded) {
      SplashScreen.hideAsync()
    }
  }, [fontsLoaded])

  if (!fontsLoaded) return null

  return <YourApp />
}
```

**expo-location**
```tsx
import * as Location from 'expo-location'

async function getCurrentLocation() {
  const { status } = await Location.requestForegroundPermissionsAsync()
  if (status !== 'granted') {
    console.log('Permission denied')
    return
  }

  const location = await Location.getCurrentPositionAsync({})
  return {
    latitude: location.coords.latitude,
    longitude: location.coords.longitude,
  }
}

// Watch position changes
const subscription = await Location.watchPositionAsync(
  { accuracy: Location.Accuracy.BestForNavigation },
  (location) => console.log(location)
)
```

**expo-camera**
```tsx
import { CameraView, useCameraPermissions } from 'expo-camera'

export function CameraComponent() {
  const [permission, requestPermission] = useCameraPermissions()
  const [facing, setFacing] = useState<'back' | 'front'>('back')

  if (!permission?.granted) {
    return <Button onPress={requestPermission} title="Grant permission" />
  }

  return (
    <CameraView
      style={{ flex: 1 }}
      facing={facing}
      onBarcodeScanned={(data) => console.log(data)}
    >
      <Button onPress={() => setFacing(current => current === 'back' ? 'front' : 'back')} />
    </CameraView>
  )
}
```

**expo-notifications**
```tsx
import * as Notifications from 'expo-notifications'

// Configure notifications
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
})

// Request permissions
async function requestPermissions() {
  const { status } = await Notifications.requestPermissionsAsync()
  return status === 'granted'
}

// Schedule notification
async function scheduleNotification() {
  await Notifications.scheduleNotificationAsync({
    content: {
      title: 'Hello!',
      body: 'This is a notification',
      data: { screen: 'profile' },
    },
    trigger: { seconds: 5 },
  })
}

// Add response listener
useEffect(() => {
  const subscription = Notifications.addNotificationResponseReceivedListener(
    (response) => {
      const screen = response.notification.request.content.data.screen
      // Navigate to screen
    }
  )
  return () => subscription.remove()
}, [])
```

**expo-image-picker**
```tsx
import * as ImagePicker from 'expo-image-picker'

async function pickImage() {
  const result = await ImagePicker.launchImageLibraryAsync({
    mediaTypes: ['images', 'videos'],
    allowsEditing: true,
    aspect: [4, 3],
    quality: 1,
  })

  if (!result.canceled) {
    return result.assets[0].uri
  }
}
```

**expo-av (Audio/Video)**
```tsx
import { Audio } from 'expo-av'

async function playSound() {
  const { sound } = await Audio.Sound.createAsync(
    require('./assets/sound.mp3')
  )
  await sound.playAsync()
}
```

### Managed vs Bare Workflow

**Managed Workflow (Expo Go)**
- No native code modifications
- Quick iteration with Expo Go app
- Over 50 SDK modules available
- OTA updates included
- Limited to available modules

**Bare Workflow (Development Build)**
- Full native code access
- Any native module can be used
- Custom native modifications
- Requires development build
- OTA updates still available

### Environment Variables

**.env Files**
```bash
# .env.production
API_URL=https://api.production.com
SENTRY_DSN=https://sentry.io/dsn

# .env.development
API_URL=https://api.dev.com
```

**Using Constants**
```tsx
import Constants from 'expo-constants'

const apiUrl = Constants.expoConfig?.extra?.apiUrl || 'https://api.default.com'
```

### App Stores Submission

**iOS Store**
```bash
# Configure app store connect
eas submit --platform ios --latest

# With specific build
eas submit --platform ios --buildId BUILD_ID
```

**Android Store**
```bash
# Submit to Google Play
eas submit --platform android --latest
```

### Common Pitfalls

1. **Not using EAS Update** → Missing out on OTA updates
2. **Hardcoding values** → Use app.config.js and environment variables
3. **Ignoring file size** → Large assets slow down updates
4. **Not testing on devices** → Simulator doesn't catch all issues
5. **Forgetting permissions** → Add permissions in app.json
6. **Breaking changes** → Test updates thoroughly
7. **Not using development builds** → Needed for custom native modules

### Best Practices

1. **Use Expo Router** → Modern navigation solution
2. **EAS Build for production** → Reliable cloud builds
3. **OTA updates** → Fix bugs without store approval
4. **TypeScript** → Type safety across your app
5. **Environment variables** → Different configs per environment
6. **Font optimization** → Only load needed fonts
7. **Image optimization** → Use proper image sizes
8. **Error tracking** → Use Sentry or similar
9. **Analytics** → Track user behavior
10. **Test before publishing** → Test on real devices

## Version Notes

### Supported Versions
- **Recommended:** Expo SDK 52+ (latest stable)
- **Minimum:** Expo SDK 50+ (React Native 0.73+)

### Version Summary

| SDK | Release Date | React Native | Key Features |
|-----|--------------|--------------|--------------|
| 52 | Nov 2024 | 0.76 | New Architecture default, Hermes only, EAS Build v2 |
| 51 | May 2024 | 0.74 | Expo Router v3, improved dev tools |
| 50 | Feb 2024 | 0.73 | Metro 2, improved animations |
| 49 | Jan 2024 | 0.72 | Expo Router stable, Node 18+ |

### Recent Breaking Changes

#### Expo SDK 51 → 52
<!-- 🆕 v52: New Architecture default in Expo Go -->
```tsx
// v52: New Architecture (Fabric/TurboModules) enabled by default
// No code changes needed for most apps
// Paper components now use Fabric renderer
```

<!-- 🚫 v52: JavaScript Core (JSC) removed -->
```bash
# v52: Hermes is now the ONLY JS engine
# JSC is no longer supported
# All apps must use Hermes (already default since SDK 50)
```

<!-- 🔄 v52: EAS Build v2 changes -->
```json
// eas.json - v52 new format
{
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": {
        "resourceClass": "m-medium"
      }
    }
  }
}
```

<!-- 🆕 v52: expo-camera API changes -->
```tsx
// v52+: CameraView renamed from Camera
import { CameraView, useCameraPermissions } from 'expo-camera'

// v51: import { Camera } from 'expo-camera'
```

#### Expo SDK 50 → 51
<!-- 🆕 v51: Expo Router v3 -->
```tsx
// v51+: New router API
import { useRouter, useLocalSearchParams } from 'expo-router'

// Updated navigation
const router = useRouter()
const params = useLocalSearchParams()
```

<!-- 🔄 v51: Metro 2 changes -->
```js
// metro.config.js - v51 uses Metro 2
const { getDefaultConfig } = require('expo/metro-config')

const config = getDefaultConfig(__dirname)

// No more config.requiresMainFieldsSetup
```

<!-- 🆕 v51: Improved dev tools -->
```bash
# v51+: New dev server features
npx expo start --dev-client  # Better dev client support
npx expo start --no-dev  # Production builds without dev tools
```

#### Expo SDK 49 → 50
<!-- 🆕 v50: Node 18+ required -->
```bash
# v50+: Requires Node.js 18+
node --version  # Must be 18.x or higher
```

<!-- 🆕 v50: Metro 2.0 -->
```js
// v50+: Simplified Metro config
const config = getDefaultConfig(__dirname)
// No more complex metro config needed
```

<!-- 🔄 v50: EAS Update changes -->
```json
// app.json - v50 updates URL format
{
  "expo": {
    "updates": {
      "url": "https://u.expo.dev/PROJECT_ID"  // New format
    }
  }
}
```

### Version Callouts by Feature

**Expo Router**
<!-- ✅ v50+: File-based routing stable -->
<!-- 🆕 v51: v3 with improved performance -->
```tsx
// Stable routing across v50, v51, v52
// app/(tabs)/index.tsx
export default function HomeScreen() {
  return <View>Home</View>
}
```

**EAS Build**
<!-- ✅ v50+: EAS Build stable -->
<!-- 🔄 v52: v2 with improved caching -->
```bash
# Stable across versions
eas build --platform ios
eas build --platform all

# v52+: Faster builds with improved caching
```

**EAS Update (OTA)**
<!-- ✅ v50+: OTA updates stable -->
```bash
# Stable across versions
eas update --branch production --message "Fix bug"

# v50+: New URL format for updates
```

**expo-notifications**
<!-- ✅ v50+: API stable -->
```tsx
// Stable across versions
import * as Notifications from 'expo-notifications'

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
})
```

**expo-camera**
<!-- 🔄 v52: Camera API renamed -->
```tsx
// v52+: New API
import { CameraView, useCameraPermissions } from 'expo-camera'

export function CameraScreen() {
  const [permission, requestPermission] = useCameraPermissions()

  if (!permission?.granted) {
    return <Button onPress={requestPermission} title="Grant permission" />
  }

  return (
    <CameraView style={{ flex: 1 }}>
      {/* Camera UI */}
    </CameraView>
  )
}

// v51-: Old API
// import { Camera } from 'expo-camera'
```

**expo-secure-store**
<!-- ✅ v50+: API stable -->
```tsx
// Stable across versions
import * as SecureStore from 'expo-secure-store'

await SecureStore.setItemAsync('token', 'value')
const token = await SecureStore.getItemAsync('token')
```

**Hermes Engine**
<!-- ✅ v50+: Hermes default -->
<!-- 🚫 v52: Hermes ONLY (JSC removed) -->
```bash
# v50+: Hermes is default
# v52: Hermes is the ONLY option
# No need to configure - always enabled
```

**New Architecture**
<!-- 🔄 v52: Default enabled -->
```tsx
// v52+: New Architecture enabled by default
// No changes needed for most apps
// Fabric renderer and TurboModules active

// v51-: Opt-in via app.json
```

### Upgrade Recommendations

**From SDK 50 to 51:**
1. Run `npx expo install --fix`
2. Update Expo Router to v3
3. Review Metro config changes
4. Test on development build
5. Update any camera imports

**From SDK 51 to 52:**
1. Run `npx expo install --fix`
2. Ensure using Hermes (remove any JSC config)
3. Update camera imports to `CameraView`
4. Test on new Expo Go with New Architecture
5. Review EAS Build v2 changes

**EAS Upgrade:**
```bash
# Update EAS CLI
npm install -g eas-cli

# Check for deprecations
eas build:platform:list
```

### Minimum Requirements by SDK

| SDK | Node | React Native | Xcode | Android |
|-----|------|--------------|-------|---------|
| 52 | 18+ | 0.76 | 15.0+ | API 34+ |
| 51 | 18+ | 0.74 | 15.0+ | API 33+ |
| 50 | 18+ | 0.73 | 14.0+ | API 33+ |

### Deprecation Timeline

**SDK 52 Deprecations:**
- JavaScript Core (JSC) - removed
- Old Camera API - renamed to CameraView
- Legacy dev server - use --dev-client

**Upcoming Deprecations (SDK 53+):**
- Watch for Expo Router updates
- Check for EAS Build v3 announcements

---

*Part of SuperAI GitHub - Centralized OpenCode Configuration*
