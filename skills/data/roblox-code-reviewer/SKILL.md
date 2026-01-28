---
name: roblox-code-reviewer
description: Reviews Roblox Luau code for correctness, modern patterns, security, and performance. Understands event-driven architecture, client/server boundaries, and script organization. Use after writing Roblox code to catch issues before shipping.
allowed-tools: Read, Glob, Grep
model: sonnet
---

# Roblox Code Reviewer

A comprehensive code review skill for Roblox game development. Reviews code for:
- Event-driven architecture correctness
- Client/server boundary violations
- Script organization issues
- Deprecated API usage
- Performance anti-patterns
- Security vulnerabilities

## How to Use

After code is written, review against the checklists in the reference files:
1. `event-architecture.md` - Connection lifecycle, event ordering, cleanup
2. `client-server.md` - What runs where, security boundaries
3. `script-organization.md` - Where scripts should live
4. `deprecated-patterns.md` - Old APIs and modern replacements
5. `performance.md` - Common performance mistakes
6. `security.md` - Exploit prevention patterns

For each issue found:
1. Quote the problematic code with file:line reference
2. Explain the issue briefly
3. Provide the correct pattern

---

## Quick Reference: Critical Checks

### Event-Driven Architecture (Roblox Core Pattern)

Roblox is fundamentally event-driven. Every review must check:

```lua
-- CRITICAL: Store connections for cleanup
local connection = part.Touched:Connect(callback)
-- Later: connection:Disconnect()

-- CRITICAL: Parent LAST (events fire on parenting)
local part = Instance.new("Part")
part.Size = Vector3.new(5, 5, 5)  -- Configure first
part.Parent = workspace           -- Parent last

-- CRITICAL: Use task library, not deprecated globals
task.spawn(fn)   -- not spawn()
task.wait(1)     -- not wait()
task.delay(1, fn) -- not delay()
```

### Client vs Server

| Must be SERVER | Should be CLIENT |
|----------------|------------------|
| DataStore access | UI/Camera |
| Currency/inventory changes | Input handling |
| Damage calculation | Visual effects |
| Game state authority | Client prediction |
| Hit validation | Animation playback |

### Script Placement

| Location | Purpose |
|----------|---------|
| ServerScriptService | Server-only scripts |
| ServerStorage | Server-only modules/data |
| ReplicatedStorage | Shared ModuleScripts |
| StarterPlayerScripts | Persistent client scripts |
| StarterCharacterScripts | Per-spawn client scripts |

### Top 10 Code Smells

1. `Instance.new("Part", workspace)` - Parent as 2nd arg
2. `wait()` / `spawn()` / `delay()` - Use task library
3. `FindFirstChild()` in Heartbeat - Cache references
4. `.Touched:Connect()` without disconnect - Memory leak
5. `RemoteEvent` without type validation - Security hole
6. Client calculating damage - Server authority violation
7. `Velocity` property - Use `AssemblyLinearVelocity`
8. Manual character construction - Use HumanoidDescription
9. Tables created every frame - GC pressure
10. No WaitForChild timeout - Can hang forever

---

## Review Process

### Step 1: Architecture Check
- Is code in correct location (server vs client)?
- Are connections properly managed?
- Is parent set last for Instance.new()?

### Step 2: Security Check
- Are RemoteEvent args validated?
- Is critical logic server-side?
- Are there rate limits?

### Step 3: Performance Check
- Any allocations in hot loops?
- Are references cached?
- Any deprecated APIs?

### Step 4: Modern Patterns Check
- Using task library?
- Using constraint physics?
- Using HumanoidDescription for NPCs?

See reference files for detailed patterns.
