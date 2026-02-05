---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}} Use this skill when working with drawing operations, sprites, animations, shaders, or any visual rendering in LÖVE games.
license: MIT
metadata:
  author: Ron Dekker <rondekker.nl>
---

## When to use this skill
{{SKILL_DESCRIPTION}} Use this skill when working with drawing operations, sprites, animations, shaders, or any visual rendering in LÖVE games.

## Common use cases
- Drawing shapes, images, and text
- Creating animations and particle effects
- Implementing custom shaders and post-processing effects
- Managing sprites and sprite batches
- Handling screen transitions and visual effects

{{MODULES_LIST}}
{{FUNCTIONS_LIST}}
{{CALLBACKS_LIST}}
{{TYPES_LIST}}
{{ENUMS_LIST}}

## Examples

### Drawing a colored rectangle
```lua
-- Draw a red rectangle
function love.draw()
  love.graphics.setColor(1, 0, 0, 1)  -- RGBA: red, fully opaque
  love.graphics.rectangle("fill", 100, 100, 200, 150)
end
```

### Loading and drawing an image
```lua
local image

function love.load()
  image = love.graphics.newImage("sprite.png")
end

function love.draw()
  love.graphics.draw(image, 200, 200, 0, 2, 2)  -- Draw at 200,200 with 2x scale
end
```

## Best practices
- Load graphics resources in love.load() to avoid delays during gameplay
- Use sprite batches for efficient drawing of many identical sprites
- Consider using canvas objects for complex compositions
- Be mindful of coordinate system (0,0 is top-left by default)
- Use appropriate image formats: PNG for transparency, JPEG for photos

## Performance considerations
- Too many draw calls can cause performance issues
- Large images consume more memory
- Complex shaders impact GPU performance
- Frequent state changes (color, blend mode) can be expensive
- Particle systems can be CPU-intensive with many particles

## Platform compatibility
- **Desktop (Windows, macOS, Linux)**: Full graphics support including shaders
- **Mobile (iOS, Android)**: Full support but some shader features may be limited
- **Web**: Good support but some advanced features may not be available
