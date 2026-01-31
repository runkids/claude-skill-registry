---
name: game-loop
description: Implements game loop systems including round-based gameplay, matchmaking, lobbies, voting, spectator mode, and late-join handling. Use when building multiplayer games that need structured game flow like murder mystery, battle royale, or team-based games.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox Game Loop Systems

When implementing round-based multiplayer games, follow these patterns for smooth game flow.

## Game State Machine

### Core States

```lua
local GameState = {
    WAITING = "Waiting",      -- In lobby, waiting for players
    STARTING = "Starting",    -- Countdown before game starts
    PLAYING = "Playing",      -- Game in progress
    INTERMISSION = "Intermission", -- Between rounds, showing results
    ENDING = "Ending"         -- Game ending, cleanup
}
```

### State Manager

```lua
local GameManager = {}
GameManager.currentState = GameState.WAITING
GameManager.stateStartTime = 0
GameManager.round = 0

local StateChangedEvent = Instance.new("BindableEvent")
GameManager.StateChanged = StateChangedEvent.Event

function GameManager.setState(newState)
    local oldState = GameManager.currentState
    GameManager.currentState = newState
    GameManager.stateStartTime = os.clock()

    StateChangedEvent:Fire(newState, oldState)

    -- Notify clients
    GameStateRemote:FireAllClients(newState, {
        round = GameManager.round,
        timestamp = workspace:GetServerTimeNow()
    })
end

function GameManager.getTimeInState()
    return os.clock() - GameManager.stateStartTime
end
```

### Main Game Loop

```lua
local MIN_PLAYERS = 2
local COUNTDOWN_TIME = 10
local ROUND_TIME = 180
local INTERMISSION_TIME = 15

local function gameLoop()
    while true do
        -- WAITING STATE
        GameManager.setState(GameState.WAITING)

        while #Players:GetPlayers() < MIN_PLAYERS do
            StatusRemote:FireAllClients("Waiting for players...",
                MIN_PLAYERS - #Players:GetPlayers() .. " more needed")
            task.wait(1)
        end

        -- STARTING STATE (Countdown)
        GameManager.setState(GameState.STARTING)

        for i = COUNTDOWN_TIME, 1, -1 do
            StatusRemote:FireAllClients("Game starting in...", i)
            task.wait(1)

            -- Cancel if players left
            if #Players:GetPlayers() < MIN_PLAYERS then
                break
            end
        end

        if #Players:GetPlayers() < MIN_PLAYERS then
            continue
        end

        -- PLAYING STATE
        GameManager.round = GameManager.round + 1
        GameManager.setState(GameState.PLAYING)

        setupRound()

        local roundStartTime = os.clock()
        while os.clock() - roundStartTime < ROUND_TIME do
            -- Check win conditions
            local winner = checkWinCondition()
            if winner then
                break
            end

            task.wait(0.5)
        end

        -- INTERMISSION STATE
        GameManager.setState(GameState.INTERMISSION)

        local results = calculateResults()
        ResultsRemote:FireAllClients(results)

        cleanupRound()

        task.wait(INTERMISSION_TIME)
    end
end

task.spawn(gameLoop)
```

## Lobby System

### Lobby Manager

```lua
local LobbyManager = {}
LobbyManager.lobbySpawn = workspace:WaitForChild("LobbySpawn")
LobbyManager.playersInLobby = {}

function LobbyManager.teleportToLobby(player)
    local character = player.Character
    if not character then return end

    character:PivotTo(LobbyManager.lobbySpawn.CFrame + Vector3.new(
        math.random(-10, 10), 5, math.random(-10, 10)
    ))

    LobbyManager.playersInLobby[player] = true

    -- Enable lobby features
    player:SetAttribute("InLobby", true)
end

function LobbyManager.teleportToGame(player, spawnPoint)
    local character = player.Character
    if not character then return end

    character:PivotTo(spawnPoint.CFrame)

    LobbyManager.playersInLobby[player] = nil
    player:SetAttribute("InLobby", false)
end

function LobbyManager.teleportAllToGame(spawnPoints)
    local players = Players:GetPlayers()

    for i, player in ipairs(players) do
        local spawnIndex = ((i - 1) % #spawnPoints) + 1
        LobbyManager.teleportToGame(player, spawnPoints[spawnIndex])
    end
end
```

### Lobby Obby (Mini-game while waiting)

```lua
local function setupLobbyObby()
    local obbyStart = workspace.Lobby.ObbyStart
    local obbyEnd = workspace.Lobby.ObbyEnd

    -- Teleport to start on touch
    obbyStart.Touched:Connect(function(hit)
        local player = Players:GetPlayerFromCharacter(hit.Parent)
        if player and player:GetAttribute("InLobby") then
            hit.Parent:PivotTo(obbyStart.CFrame + Vector3.new(0, 3, 0))
        end
    end)

    -- Reward on completion
    obbyEnd.Touched:Connect(function(hit)
        local player = Players:GetPlayerFromCharacter(hit.Parent)
        if player and player:GetAttribute("InLobby") then
            local completions = player:GetAttribute("LobbyObbyCompletions") or 0
            player:SetAttribute("LobbyObbyCompletions", completions + 1)

            -- Small reward
            DataManager.addCurrency(player, "coins", 10)

            -- Teleport back to start
            hit.Parent:PivotTo(obbyStart.CFrame + Vector3.new(0, 3, 0))
        end
    end)
end
```

## Voting System

### Map Voting

```lua
local VotingManager = {}
VotingManager.maps = {"Desert", "Forest", "City", "Snow"}
VotingManager.votes = {}
VotingManager.options = {}

function VotingManager.startVote(numOptions)
    numOptions = numOptions or 3
    VotingManager.votes = {}
    VotingManager.options = {}

    -- Select random maps for voting
    local available = table.clone(VotingManager.maps)
    for i = 1, math.min(numOptions, #available) do
        local index = math.random(#available)
        table.insert(VotingManager.options, available[index])
        table.remove(available, index)
    end

    -- Notify clients
    VoteStartRemote:FireAllClients(VotingManager.options)
end

function VotingManager.castVote(player, optionIndex)
    if optionIndex < 1 or optionIndex > #VotingManager.options then
        return false
    end

    VotingManager.votes[player.UserId] = optionIndex

    -- Broadcast updated vote counts
    local counts = {}
    for i = 1, #VotingManager.options do
        counts[i] = 0
    end

    for _, vote in pairs(VotingManager.votes) do
        counts[vote] = counts[vote] + 1
    end

    VoteUpdateRemote:FireAllClients(counts)
    return true
end

function VotingManager.getWinner()
    local counts = {}
    for i = 1, #VotingManager.options do
        counts[i] = 0
    end

    for _, vote in pairs(VotingManager.votes) do
        counts[vote] = counts[vote] + 1
    end

    -- Find highest vote (random tiebreaker)
    local maxVotes = 0
    local winners = {}

    for i, count in ipairs(counts) do
        if count > maxVotes then
            maxVotes = count
            winners = {i}
        elseif count == maxVotes then
            table.insert(winners, i)
        end
    end

    local winnerIndex = winners[math.random(#winners)]
    return VotingManager.options[winnerIndex]
end

-- Client voting pad interaction
VotePadRemote.OnServerEvent:Connect(function(player, padIndex)
    VotingManager.castVote(player, padIndex)
end)
```

### Physical Voting Pads

```lua
local function createVotingPads(position, options)
    local pads = Instance.new("Model")
    pads.Name = "VotingPads"

    for i, option in ipairs(options) do
        local pad = Instance.new("Part")
        pad.Size = Vector3.new(8, 1, 8)
        pad.Position = position + Vector3.new((i - 1) * 12 - (#options - 1) * 6, 0, 0)
        pad.Anchored = true
        pad.Material = Enum.Material.Neon
        pad.Color = Color3.fromHSV((i - 1) / #options, 0.8, 0.9)
        pad.Name = "VotePad_" .. i
        pad.Parent = pads

        -- Label
        local billboard = Instance.new("BillboardGui")
        billboard.Size = UDim2.new(0, 200, 0, 50)
        billboard.StudsOffset = Vector3.new(0, 5, 0)
        billboard.Parent = pad

        local label = Instance.new("TextLabel")
        label.Size = UDim2.new(1, 0, 1, 0)
        label.BackgroundTransparency = 1
        label.Text = option .. "\n0 votes"
        label.TextColor3 = Color3.new(1, 1, 1)
        label.TextScaled = true
        label.Parent = billboard

        -- Vote on touch
        pad.Touched:Connect(function(hit)
            local player = Players:GetPlayerFromCharacter(hit.Parent)
            if player then
                VotePadRemote:FireServer(i)
            end
        end)
    end

    pads.Parent = workspace.Lobby
    return pads
end
```

## Ready-Up System

```lua
local ReadyManager = {}
ReadyManager.readyPlayers = {}

function ReadyManager.setReady(player, isReady)
    ReadyManager.readyPlayers[player.UserId] = isReady

    -- Update UI for all players
    ReadyUpdateRemote:FireAllClients(ReadyManager.getReadyStatus())
end

function ReadyManager.getReadyStatus()
    local status = {}
    for _, player in ipairs(Players:GetPlayers()) do
        status[player.UserId] = ReadyManager.readyPlayers[player.UserId] or false
    end
    return status
end

function ReadyManager.allReady()
    local players = Players:GetPlayers()
    if #players < MIN_PLAYERS then return false end

    for _, player in ipairs(players) do
        if not ReadyManager.readyPlayers[player.UserId] then
            return false
        end
    end
    return true
end

function ReadyManager.reset()
    ReadyManager.readyPlayers = {}
    ReadyUpdateRemote:FireAllClients({})
end

-- Modified game loop with ready-up
local function gameLoopWithReady()
    while true do
        GameManager.setState(GameState.WAITING)
        ReadyManager.reset()

        -- Wait for enough players AND all ready
        while not ReadyManager.allReady() do
            local ready = 0
            local total = #Players:GetPlayers()

            for _, isReady in pairs(ReadyManager.readyPlayers) do
                if isReady then ready = ready + 1 end
            end

            StatusRemote:FireAllClients("Ready up!", ready .. "/" .. total .. " ready")
            task.wait(0.5)
        end

        -- Continue with game...
    end
end
```

## Spectator System

```lua
local SpectatorManager = {}
SpectatorManager.spectators = {}
SpectatorManager.targets = {}

function SpectatorManager.makeSpectator(player)
    local character = player.Character
    if character then
        -- Make invisible and non-collidable
        for _, part in ipairs(character:GetDescendants()) do
            if part:IsA("BasePart") then
                part.Transparency = 1
                part.CanCollide = false
            end
        end

        local humanoid = character:FindFirstChildOfClass("Humanoid")
        if humanoid then
            humanoid.WalkSpeed = 32  -- Faster movement
        end
    end

    SpectatorManager.spectators[player] = true
    player:SetAttribute("IsSpectator", true)

    -- Start spectating a random alive player
    SpectatorManager.spectateNext(player)
end

function SpectatorManager.removeSpectator(player)
    SpectatorManager.spectators[player] = nil
    SpectatorManager.targets[player] = nil
    player:SetAttribute("IsSpectator", false)
end

function SpectatorManager.getAlivePlayers()
    local alive = {}
    for _, player in ipairs(Players:GetPlayers()) do
        if not SpectatorManager.spectators[player] and
           player.Character and
           player.Character:FindFirstChildOfClass("Humanoid") and
           player.Character:FindFirstChildOfClass("Humanoid").Health > 0 then
            table.insert(alive, player)
        end
    end
    return alive
end

function SpectatorManager.spectateNext(player)
    local alive = SpectatorManager.getAlivePlayers()
    if #alive == 0 then return end

    local currentIndex = table.find(alive, SpectatorManager.targets[player]) or 0
    local nextIndex = (currentIndex % #alive) + 1

    SpectatorManager.targets[player] = alive[nextIndex]
    SpectateTargetRemote:FireClient(player, alive[nextIndex])
end

function SpectatorManager.spectatePrevious(player)
    local alive = SpectatorManager.getAlivePlayers()
    if #alive == 0 then return end

    local currentIndex = table.find(alive, SpectatorManager.targets[player]) or 2
    local prevIndex = ((currentIndex - 2) % #alive) + 1

    SpectatorManager.targets[player] = alive[prevIndex]
    SpectateTargetRemote:FireClient(player, alive[prevIndex])
end

-- Client-side spectator camera
-- In LocalScript:
local spectatingTarget = nil

SpectateTargetRemote.OnClientEvent:Connect(function(target)
    spectatingTarget = target
end)

RunService.RenderStepped:Connect(function()
    if not LocalPlayer:GetAttribute("IsSpectator") then return end
    if not spectatingTarget or not spectatingTarget.Character then return end

    local targetHead = spectatingTarget.Character:FindFirstChild("Head")
    if targetHead then
        -- Third-person view of target
        Camera.CameraType = Enum.CameraType.Custom
        Camera.CameraSubject = targetHead
    end
end)
```

## Team Assignment

```lua
local TeamManager = {}

function TeamManager.assignTeams(mode)
    local players = Players:GetPlayers()

    if mode == "FFA" then
        -- Free for all - no teams
        for _, player in ipairs(players) do
            player.Team = nil
            player.Neutral = true
        end

    elseif mode == "TwoTeams" then
        -- Split into two teams
        local shuffled = table.clone(players)
        for i = #shuffled, 2, -1 do
            local j = math.random(i)
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
        end

        local half = math.ceil(#shuffled / 2)
        for i, player in ipairs(shuffled) do
            if i <= half then
                player.Team = Teams.Red
            else
                player.Team = Teams.Blue
            end
        end

    elseif mode == "OneVsAll" then
        -- One special player vs everyone else
        local special = players[math.random(#players)]

        for _, player in ipairs(players) do
            if player == special then
                player.Team = Teams.Special
            else
                player.Team = Teams.Normal
            end
        end

        return special  -- Return the special player
    end
end

function TeamManager.balanceTeams()
    local teamCounts = {}
    for _, team in ipairs(Teams:GetTeams()) do
        teamCounts[team] = #team:GetPlayers()
    end

    -- Find imbalanced teams
    local maxTeam, minTeam
    local maxCount, minCount = 0, math.huge

    for team, count in pairs(teamCounts) do
        if count > maxCount then
            maxCount = count
            maxTeam = team
        end
        if count < minCount then
            minCount = count
            minTeam = team
        end
    end

    -- Move player if difference > 1
    if maxCount - minCount > 1 then
        local playersOnMax = maxTeam:GetPlayers()
        local toMove = playersOnMax[math.random(#playersOnMax)]
        toMove.Team = minTeam

        TeamChangeRemote:FireClient(toMove, minTeam.Name)
    end
end
```

## Late Join Handling

```lua
local function handleLateJoin(player)
    local state = GameManager.currentState

    if state == GameState.WAITING or state == GameState.INTERMISSION then
        -- Can join normally
        LobbyManager.teleportToLobby(player)

    elseif state == GameState.STARTING then
        -- Countdown - join the round
        LobbyManager.teleportToLobby(player)
        -- Will be teleported with everyone when round starts

    elseif state == GameState.PLAYING then
        -- Game in progress - spectate or join mid-round
        if ALLOW_MID_ROUND_JOIN then
            -- Join the round
            TeamManager.assignToSmallestTeam(player)
            local spawn = getTeamSpawn(player.Team)
            LobbyManager.teleportToGame(player, spawn)
        else
            -- Force spectate
            LobbyManager.teleportToLobby(player)
            player:SetAttribute("JoinedLate", true)

            task.wait(2)  -- Wait for character
            SpectatorManager.makeSpectator(player)

            StatusRemote:FireClient(player, "Round in progress", "You'll join next round")
        end
    end
end

Players.PlayerAdded:Connect(function(player)
    player.CharacterAdded:Connect(function()
        handleLateJoin(player)
    end)
end)
```

## Round Setup & Cleanup

```lua
local function setupRound()
    -- Select map
    local selectedMap = VotingManager.getWinner()
    loadMap(selectedMap)

    -- Assign teams
    local specialPlayer = TeamManager.assignTeams(currentGameMode)

    -- Get spawn points
    local spawnPoints = workspace.CurrentMap.Spawns:GetChildren()

    -- Teleport players
    LobbyManager.teleportAllToGame(spawnPoints)

    -- Give loadouts
    for _, player in ipairs(Players:GetPlayers()) do
        giveLoadout(player, player.Team)
    end

    -- Initialize round-specific systems
    initializeObjectives()
    resetScores()

    -- Notify clients
    RoundStartRemote:FireAllClients({
        map = selectedMap,
        mode = currentGameMode,
        timeLimit = ROUND_TIME,
        specialPlayer = specialPlayer and specialPlayer.UserId
    })
end

local function cleanupRound()
    -- Return all players to lobby
    for _, player in ipairs(Players:GetPlayers()) do
        LobbyManager.teleportToLobby(player)

        -- Reset player state
        player:SetAttribute("IsSpectator", false)
        player:SetAttribute("JoinedLate", false)

        -- Reset character
        if player.Character then
            local humanoid = player.Character:FindFirstChildOfClass("Humanoid")
            if humanoid then
                humanoid.Health = humanoid.MaxHealth
            end
        end

        -- Clear inventory
        clearTemporaryItems(player)
    end

    -- Unload map
    if workspace:FindFirstChild("CurrentMap") then
        workspace.CurrentMap:Destroy()
    end

    -- Reset managers
    SpectatorManager.spectators = {}
    SpectatorManager.targets = {}
    VotingManager.votes = {}
end
```

## Win Conditions

```lua
local function checkWinCondition()
    local mode = currentGameMode

    if mode == "Elimination" then
        -- Last player/team alive wins
        local alive = SpectatorManager.getAlivePlayers()

        if #alive <= 1 then
            return alive[1]  -- Winner (or nil if draw)
        end

        -- Check team elimination
        local teamsAlive = {}
        for _, player in ipairs(alive) do
            teamsAlive[player.Team] = true
        end

        local count = 0
        local lastTeam
        for team in pairs(teamsAlive) do
            count = count + 1
            lastTeam = team
        end

        if count == 1 then
            return lastTeam  -- Winning team
        end

    elseif mode == "ScoreLimit" then
        -- First to reach score wins
        for _, player in ipairs(Players:GetPlayers()) do
            if (player:GetAttribute("RoundScore") or 0) >= SCORE_LIMIT then
                return player
            end
        end

    elseif mode == "KingOfTheHill" then
        -- Control objective for duration
        local controller = getObjectiveController()
        if controller then
            local controlTime = controller:GetAttribute("ControlTime") or 0
            if controlTime >= CONTROL_DURATION then
                return controller
            end
        end
    end

    return nil  -- No winner yet
end
```

## Results Calculation

```lua
local function calculateResults()
    local results = {
        winner = nil,
        mvp = nil,
        players = {}
    }

    -- Determine winner
    results.winner = checkWinCondition()

    -- Calculate player stats
    local highestScore = 0

    for _, player in ipairs(Players:GetPlayers()) do
        local stats = {
            kills = player:GetAttribute("RoundKills") or 0,
            deaths = player:GetAttribute("RoundDeaths") or 0,
            score = player:GetAttribute("RoundScore") or 0,
            damage = player:GetAttribute("RoundDamage") or 0,
            objectives = player:GetAttribute("RoundObjectives") or 0
        }

        results.players[player.UserId] = stats

        -- MVP is highest score
        if stats.score > highestScore then
            highestScore = stats.score
            results.mvp = player.UserId
        end

        -- Grant rewards
        local baseReward = 50
        local winBonus = (player == results.winner or player.Team == results.winner) and 100 or 0
        local mvpBonus = (player.UserId == results.mvp) and 50 or 0

        local totalReward = baseReward + winBonus + mvpBonus + (stats.kills * 10)
        DataManager.addCurrency(player, "coins", totalReward)

        -- Grant XP
        LevelingService.addExperience(player, stats.score + baseReward)
    end

    return results
end
```

## Complete Integration Example

```lua
-- Main server script for round-based game

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")
local Teams = game:GetService("Teams")

-- Configuration
local CONFIG = {
    MIN_PLAYERS = 2,
    MAX_PLAYERS = 16,
    COUNTDOWN_TIME = 15,
    ROUND_TIME = 300,
    INTERMISSION_TIME = 20,
    ALLOW_MID_ROUND_JOIN = false,
    GAME_MODES = {"Elimination", "TeamDeathmatch", "FreeForAll"}
}

-- Initialize managers
local GameManager = require(script.GameManager)
local LobbyManager = require(script.LobbyManager)
local VotingManager = require(script.VotingManager)
local SpectatorManager = require(script.SpectatorManager)
local TeamManager = require(script.TeamManager)

-- Create remotes
local Remotes = Instance.new("Folder")
Remotes.Name = "GameRemotes"
Remotes.Parent = ReplicatedStorage

local GameStateRemote = Instance.new("RemoteEvent", Remotes)
GameStateRemote.Name = "GameState"

local VoteRemote = Instance.new("RemoteEvent", Remotes)
VoteRemote.Name = "Vote"

local ReadyRemote = Instance.new("RemoteEvent", Remotes)
ReadyRemote.Name = "Ready"

local SpectateRemote = Instance.new("RemoteEvent", Remotes)
SpectateRemote.Name = "Spectate"

-- Main loop
task.spawn(function()
    while true do
        -- WAITING
        GameManager.setState("Waiting")

        while #Players:GetPlayers() < CONFIG.MIN_PLAYERS do
            task.wait(1)
        end

        -- MAP VOTING
        VotingManager.startVote(3)

        for i = 10, 1, -1 do
            task.wait(1)
        end

        local selectedMap = VotingManager.getWinner()

        -- COUNTDOWN
        GameManager.setState("Starting")

        for i = CONFIG.COUNTDOWN_TIME, 1, -1 do
            if #Players:GetPlayers() < CONFIG.MIN_PLAYERS then
                break
            end
            task.wait(1)
        end

        if #Players:GetPlayers() < CONFIG.MIN_PLAYERS then
            continue
        end

        -- START ROUND
        GameManager.setState("Playing")
        setupRound(selectedMap)

        local startTime = os.clock()

        while os.clock() - startTime < CONFIG.ROUND_TIME do
            local winner = checkWinCondition()
            if winner then
                break
            end
            task.wait(0.5)
        end

        -- INTERMISSION
        GameManager.setState("Intermission")

        local results = calculateResults()
        ResultsRemote:FireAllClients(results)

        cleanupRound()

        task.wait(CONFIG.INTERMISSION_TIME)
    end
end)
```
