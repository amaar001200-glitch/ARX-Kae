-- ████████████████████████████████████████████████████████████████████████████████
-- █ VISUAL MODULES PACK (Fog Remover + Global Font)
-- █ خام واحد يحتوي على موديلين
-- ████████████████████████████████████████████████████████████████████████████████

local VisualModules = {}

do
    local Lighting = game:GetService("Lighting")
    local Players = game:GetService("Players")
    local LocalPlayer = Players.LocalPlayer
    
    -- ========== موديل إزالة الضباب ==========
    local fogConn = nil
    local originalFog = {}
    
    local function SetFogRemover(state)
        if state then
            originalFog.FogEnd = Lighting.FogEnd
            originalFog.FogStart = Lighting.FogStart
            originalFog.FogColor = Lighting.FogColor
            
            Lighting.FogEnd = 1e9
            Lighting.FogStart = 1e9
            Lighting.FogColor = Color3.new(0, 0, 0)
            
            if fogConn then fogConn:Disconnect() end
            fogConn = Lighting:GetPropertyChangedSignal("FogEnd"):Connect(function()
                Lighting.FogEnd = 1e9
                Lighting.FogStart = 1e9
            end)
        else
            Lighting.FogEnd = originalFog.FogEnd
            Lighting.FogStart = originalFog.FogStart
            Lighting.FogColor = originalFog.FogColor
            if fogConn then fogConn:Disconnect(); fogConn = nil end
        end
    end
    
    -- ========== موديل تغيير الخط ==========
    local originalFonts = {}
    local fontConn = nil
    
    local function SetGlobalFont(state)
        local playerGui = LocalPlayer:FindFirstChild("PlayerGui")
        if not playerGui then return end
        
        if state then
            -- تغيير الخطوط الموجودة
            for _, obj in pairs(playerGui:GetDescendants()) do
                if obj:IsA("TextLabel") or obj:IsA("TextButton") or obj:IsA("TextBox") then
                    pcall(function()
                        if obj.Font ~= Enum.Font.GothamBold then
                            if not originalFonts[obj] then originalFonts[obj] = obj.Font end
                            obj.Font = Enum.Font.GothamBold
                        end
                    end)
                end
            end
            -- مراقبة الإضافات الجديدة
            if fontConn then fontConn:Disconnect() end
            fontConn = playerGui.DescendantAdded:Connect(function(obj)
                if obj:IsA("TextLabel") or obj:IsA("TextButton") or obj:IsA("TextBox") then
                    pcall(function()
                        if not originalFonts[obj] then originalFonts[obj] = obj.Font end
                        obj.Font = Enum.Font.GothamBold
                    end)
                end
            end)
        else
            -- استعادة الخطوط الأصلية
            for obj, oldFont in pairs(originalFonts) do
                pcall(function() obj.Font = oldFont end)
            end
            originalFonts = {}
            if fontConn then fontConn:Disconnect(); fontConn = nil end
        end
    end
    
    -- ========== الدوال العامة ==========
    function VisualModules.FogRemover(state)
        SetFogRemover(state)
    end
    
    function VisualModules.GlobalFont(state)
        SetGlobalFont(state)
    end
end

return VisualModules
