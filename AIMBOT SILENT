-- █ AIMBOT (SILENT) - OPTIMIZED (reduced update frequency)
-- تم تصليح الموديول ليكون جاهزاً للرفع والاستخدام

local AimbotModule = {}

do
    local Players = game:GetService("Players")
    local player = Players.LocalPlayer
    local RunService = game:GetService("RunService")
    local Camera = workspace.CurrentCamera

    getgenv().AimbotActive = false

    local AimbotConfig = {
        TargetPart = "HumanoidRootPart",
        MaxDistance = 1500,
        SwordRange = 1000,
        HitboxSize = 30
    }

    local CurrentTarget = nil
    local CurrentTargetPos = nil
    local DefaultSize = Vector3.new(2,2,1)

    local TargetLine = Drawing.new("Line")
    TargetLine.Color = Color3.fromRGB(180, 0, 255)
    TargetLine.Thickness = 2
    TargetLine.Transparency = 1
    TargetLine.Visible = false

    local function GetNearestEnemy()
        local char = player.Character
        if not char then return nil end
        local myHrp = char:FindFirstChild("HumanoidRootPart")
        if not myHrp then return nil end
        local nearest = nil
        local nearestDist = AimbotConfig.MaxDistance
        for _, pl in ipairs(Players:GetPlayers()) do
            if pl ~= player and pl.Character then
                local hrp = pl.Character:FindFirstChild("HumanoidRootPart")
                local hum = pl.Character:FindFirstChildOfClass("Humanoid")
                if hrp and hum and hum.Health > 0 then
                    local dist = (hrp.Position - myHrp.Position).Magnitude
                    if dist < nearestDist then
                        nearestDist = dist
                        nearest = pl
                    end
                end
            end
        end
        return nearest
    end

    -- Update target every 0.1 seconds instead of every frame
    task.spawn(function()
        while true do
            if getgenv().AimbotActive then
                local targetCandidate = GetNearestEnemy()
                if targetCandidate and targetCandidate.Character then
                    CurrentTarget = targetCandidate
                    local hrp = targetCandidate.Character:FindFirstChild(AimbotConfig.TargetPart)
                    if hrp then
                        CurrentTargetPos = hrp.Position + Vector3.new(0, 0.5, 0)
                    else
                        CurrentTargetPos = nil
                    end
                else
                    CurrentTarget = nil
                    CurrentTargetPos = nil
                end
            else
                CurrentTarget = nil
                CurrentTargetPos = nil
            end
            task.wait(0.1)
        end
    end)

    RunService.RenderStepped:Connect(function()
        if not getgenv().AimbotActive or not CurrentTargetPos then
            TargetLine.Visible = false
            return
        end
        local myHrp = player.Character and player.Character:FindFirstChild("HumanoidRootPart")
        if not myHrp then TargetLine.Visible = false; return end
        local myPos, myVisible = Camera:WorldToViewportPoint(myHrp.Position)
        local targetPos, targetVisible = Camera:WorldToViewportPoint(CurrentTargetPos)
        if myVisible and targetVisible then
            TargetLine.From = Vector2.new(myPos.X, myPos.Y)
            TargetLine.To = Vector2.new(targetPos.X, targetPos.Y)
            TargetLine.Visible = true
        else
            TargetLine.Visible = false
        end
    end)

    local oldIndex
    oldIndex = hookmetamethod(game, "__index", function(self, index)
        if index == "Hit" and getgenv().AimbotActive and not checkcaller() then
            if CurrentTarget and CurrentTarget.Character and CurrentTarget.Character:FindFirstChild("HumanoidRootPart") then
                return CurrentTarget.Character.HumanoidRootPart.CFrame
            end
        end
        return oldIndex(self, index)
    end)

    local oldNamecall
    oldNamecall = hookmetamethod(game, "__namecall", function(self, ...)
        local method = getnamecallmethod()
        local args = {...}
        if getgenv().AimbotActive and CurrentTargetPos and not checkcaller() then
            if method == "FireServer" or method == "InvokeServer" then
                local remoteName = tostring(self.Name):lower()
                if not string.find(remoteName, "m1") and not string.find(remoteName, "click") and not string.find(remoteName, "attack") then
                    local changed = false
                    for i, v in ipairs(args) do
                        if typeof(v) == "Vector3" then
                            args[i] = CurrentTargetPos
                            changed = true
                        end
                    end
                    if changed then return oldNamecall(self, unpack(args)) end
                end
            end
        end
        return oldNamecall(self, ...)
    end)

    -- Update hitboxes every 0.2 seconds (optimized)
    local lastHitboxUpdate = 0
    RunService.Heartbeat:Connect(function()
        if not getgenv().AimbotActive then return end
        local now = tick()
        if now - lastHitboxUpdate < 0.2 then return end
        lastHitboxUpdate = now
        local char = player.Character
        if not char then return end
        local myHrp = char:FindFirstChild("HumanoidRootPart")
        if not myHrp then return end
        for _, pl in ipairs(Players:GetPlayers()) do
            if pl ~= player then
                local enemyChar = pl.Character
                if enemyChar then
                    local hrp = enemyChar:FindFirstChild("HumanoidRootPart")
                    if hrp then
                        local dist = (hrp.Position - myHrp.Position).Magnitude
                        if dist <= AimbotConfig.SwordRange then
                            local wantedSize = Vector3.new(AimbotConfig.HitboxSize, AimbotConfig.HitboxSize, AimbotConfig.HitboxSize)
                            if hrp.Size ~= wantedSize then hrp.Size = wantedSize end
                            if hrp.Transparency ~= 1 then hrp.Transparency = 1 end
                            if hrp.CanCollide ~= false then hrp.CanCollide = false end
                            if hrp.CanTouch ~= true then hrp.CanTouch = true end
                        else
                            if hrp.Size ~= DefaultSize then hrp.Size = DefaultSize end
                        end
                    end
                end
            end
        end
    end)

    print("[ARAKS HUB] INVISIBLE HITBOX & ANGLE FIX LOADED")

    function AimbotModule:SetState(state)
        getgenv().AimbotActive = state
    end
end

return AimbotModule
