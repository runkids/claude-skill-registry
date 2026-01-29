---
name: component
description: Generate React Native components following established conventions. Use when creating reusable UI components, form inputs, modals, cards, lists, or any UI elements.
---

# Component Generator

Generate React Native components following established patterns.

## Directory Structure

```
src/components/
├── ComponentName/
│   └── index.tsx           # Main component file
├── ComplexComponent/
│   ├── index.tsx           # Main component
│   └── components/         # Sub-components
│       ├── SubComponent1/
│       └── SubComponent2/
└── index.ts                # Barrel exports
```

## Component Template

```tsx
import React from 'react';
import { View, Text, TouchableOpacity, TouchableOpacityProps } from 'react-native';

import { cn } from '@/lib/utils';

export interface ComponentNameProps extends TouchableOpacityProps {
  title: string;
  variant?: 'primary' | 'secondary' | 'outline';
  className?: string;
}

const ComponentName: React.FC<ComponentNameProps> = ({
  title,
  variant = 'primary',
  className,
  ...props
}) => {
  return (
    <TouchableOpacity
      className={cn(
        'flex-row items-center justify-center rounded-2xl p-4',
        variant === 'primary' && 'bg-primary',
        variant === 'secondary' && 'bg-secondary',
        variant === 'outline' && 'border-2 border-primary bg-transparent',
        className,
      )}
      {...props}
    >
      <Text className="text-base font-semibold text-primary-foreground">{title}</Text>
    </TouchableOpacity>
  );
};

export default ComponentName;
```

## Variant Pattern

```tsx
const getBgVariantStyle = (variant: ButtonProps['variant']) => {
  switch (variant) {
    case 'secondary':
      return 'bg-secondary';
    case 'danger':
      return 'bg-destructive';
    case 'success':
      return 'bg-primary';
    case 'outline':
      return 'bg-card border-2 border-primary/15';
    case 'text':
      return 'bg-transparent';
    default:
      return 'bg-primary';
  }
};

const getTextVariantStyle = (variant: ButtonProps['variant']) => {
  switch (variant) {
    case 'secondary':
      return 'text-secondary-foreground';
    case 'danger':
      return 'text-destructive-foreground';
    case 'outline':
      return 'text-foreground';
    case 'text':
      return 'text-primary';
    default:
      return 'text-primary-foreground';
  }
};
```

## ForwardRef Pattern (for inputs)

```tsx
import React, { forwardRef, useState } from 'react';
import { Text, TextInput, TextInputProps, View } from 'react-native';
import { FieldError } from 'react-hook-form';

import { cn } from '@/lib/utils';

interface InputProps extends TextInputProps {
  label?: string;
  leftIcon?: React.ReactElement;
  rightIcon?: React.ReactElement;
  error?: FieldError;
  className?: string;
  inputClassName?: string;
}

const Input = forwardRef<TextInput, InputProps>(
  ({ label, leftIcon, rightIcon, error, className, inputClassName, ...props }, ref) => {
    const [isFocused, setIsFocused] = useState(false);

    return (
      <View className={cn('w-full gap-2', className)}>
        {label && <Text className="text-base font-medium text-foreground">{label}</Text>}
        <View
          className={cn(
            'flex flex-row items-center rounded-2xl border-2 bg-background px-4 py-3',
            isFocused ? 'border-primary' : 'border-border',
            error && 'border-destructive',
          )}
        >
          {leftIcon && <View className="mr-2">{leftIcon}</View>}
          <TextInput
            ref={ref}
            className={cn('flex-1 text-base text-foreground', inputClassName)}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholderTextColor="#999"
            {...props}
          />
          {rightIcon && <View className="ml-2">{rightIcon}</View>}
        </View>
        {error && <Text className="text-sm text-destructive">{error.message}</Text>}
      </View>
    );
  },
);

Input.displayName = 'Input';
export default Input;
```

## Modal Component Pattern

```tsx
import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import Modal from 'react-native-modal';
import { SafeAreaView } from 'react-native-safe-area-context';
import { X } from 'lucide-react-native';

import { MODAL_ANIMATION_DURATION } from '@/constants/common';
import Button from '../Button';

interface MyModalProps {
  isVisible: boolean;
  onClose: () => void;
  onConfirm: (data: SomeData) => void;
}

const MyModal: React.FC<MyModalProps> = ({ isVisible, onClose, onConfirm }) => {
  const handleClose = () => {
    onClose();
  };

  const handleConfirm = (data: SomeData) => {
    setTimeout(() => {
      onConfirm(data);
    }, MODAL_ANIMATION_DURATION);
    handleClose();
  };

  return (
    <Modal
      isVisible={isVisible}
      onBackdropPress={handleClose}
      animationIn="fadeInUp"
      animationOut="fadeOutDown"
      backdropTransitionOutTiming={0}
      hideModalContentWhileAnimating={true}
      useNativeDriverForBackdrop={true}
      backdropOpacity={0.5}
      style={{ justifyContent: 'flex-end', margin: 0 }}
    >
      <SafeAreaView className="rounded-t-2xl bg-background p-6">
        <View className="mb-4 flex-row items-center justify-between">
          <Text className="text-lg font-semibold text-foreground">Modal Title</Text>
          <TouchableOpacity onPress={handleClose} className="p-1">
            <X color="hsl(var(--muted-foreground))" size={20} />
          </TouchableOpacity>
        </View>
        {/* Modal content */}
        <Button title="Confirm" onPress={() => handleConfirm(data)} className="mt-4" />
      </SafeAreaView>
    </Modal>
  );
};

export default MyModal;
```

## Collapsible List Pattern

```tsx
import React, { useState } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { ChevronDown, ChevronUp, Trash2 } from 'lucide-react-native';
import Animated, { FadeIn, FadeOut } from 'react-native-reanimated';

import { cn } from '@/lib/utils';
import { SHADOWS } from '@/constants/theme';

interface Item {
  id: string;
  title: string;
}

interface CollapsibleListProps {
  title: string;
  items: Item[];
  onRemove: (index: number) => void;
}

const CollapsibleList: React.FC<CollapsibleListProps> = ({ title, items, onRemove }) => {
  const [isExpanded, setIsExpanded] = useState(true);

  if (items.length === 0) return null;

  return (
    <View className="rounded-2xl bg-card p-4" style={SHADOWS.calm}>
      <TouchableOpacity
        onPress={() => setIsExpanded(!isExpanded)}
        className="flex-row items-center justify-between"
      >
        <Text className="text-base font-semibold text-foreground">
          {title} ({items.length})
        </Text>
        {isExpanded ? (
          <ChevronUp color="hsl(var(--muted-foreground))" size={20} />
        ) : (
          <ChevronDown color="hsl(var(--muted-foreground))" size={20} />
        )}
      </TouchableOpacity>

      {isExpanded && (
        <Animated.View entering={FadeIn} exiting={FadeOut} className="mt-3 gap-2">
          {items.map((item, index) => (
            <View
              key={item.id}
              className="flex-row items-center justify-between rounded-xl bg-secondary p-3"
            >
              <Text className="text-sm text-foreground">{item.title}</Text>
              <TouchableOpacity onPress={() => onRemove(index)}>
                <Trash2 color="hsl(var(--destructive))" size={18} />
              </TouchableOpacity>
            </View>
          ))}
        </Animated.View>
      )}
    </View>
  );
};

export default CollapsibleList;
```

## Shadows (CSS-in-JS)

```tsx
import { SHADOWS } from '@/constants/theme';

<View style={SHADOWS.calm} className="rounded-2xl bg-card p-4">
  {/* Content */}
</View>

// Available: calm, calmLg, calmXl, none
```

## Icons (lucide-react-native)

```tsx
import { ArrowLeft, Check, ChevronDown, X, Plus, Minus, Trash2 } from 'lucide-react-native';

<ArrowLeft color="hsl(var(--primary))" size={20} />
<Check color="hsl(var(--muted-foreground))" size={20} />
```

## Barrel Exports

```tsx
// src/components/index.ts
export { default as Button, type ButtonProps } from './Button';
export { default as Input } from './Input';
export { default as MyComponent, type MyComponentProps } from './MyComponent';
export type { PickerOption } from './Picker';
```

## Theme Colors

```
bg-background / text-foreground     - Main background/text
bg-primary / text-primary           - Brand primary
bg-secondary / text-secondary       - Secondary
bg-destructive / text-destructive   - Error/danger
bg-muted / text-muted-foreground    - Muted elements
bg-card                             - Card background
border-border                       - Borders
```

## Checklist

- [ ] Directory: `src/components/ComponentName/index.tsx`
- [ ] TypeScript interface extending base RN props
- [ ] NativeWind classes via `cn()` utility
- [ ] `className` prop for customization
- [ ] `SHADOWS` constant for shadows (not Tailwind shadow classes)
- [ ] `lucide-react-native` for icons
- [ ] Exported from `src/components/index.ts`
- [ ] ForwardRef for ref-needing components
