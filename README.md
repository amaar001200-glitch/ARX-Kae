return function(shared)

    local AutoKenModule = {
        Enabled = false,
        Running = false
    }

    local Players = game:GetService("Players")
    local ReplicatedStorage = game:GetService("ReplicatedStorage")
    local CollectionService = game:GetService("CollectionService")

    local LocalPlayer = Players.LocalPlayer

    local Remotes = ReplicatedStorage:WaitForChild("Remotes")
    local CommE = Remotes:WaitForChild("CommE")

    local PlayerGui = LocalPlayer:WaitForChild("PlayerGui")

    local task_wait = task.wait
    local task_spawn = task.spawn

    local function getKenButton()

        local mobileButtons = PlayerGui:FindFirstChild("MobileContextButtons")

        if not mobileButtons then
            return nil
        end

        local contextFrame = mobileButtons:FindFirstChild("ContextButtonFrame")

        if not contextFrame then
            return nil
        end

        return contextFrame:FindFirstChild("BoundActionKen")

    end

    local function startAutoKen()

        if AutoKenModule.Running then
            return
        end

        AutoKenModule.Running = true

        task_spawn(function()

            local kenButton = nil

            while AutoKenModule.Enabled do

                task_wait(0.12)

                local char = LocalPlayer.Character

                if char and CollectionService:HasTag(char, "Ken") then

                    if not kenButton or not kenButton.Parent then
                        kenButton = getKenButton()
                    end

                    if kenButton and kenButton:GetAttribute("Selected") ~= true then
                        kenButton:SetAttribute("Selected", true)
                    end

                    local om = getrenv()._G.OM

                    if om and not om.active then

                        om.radius = 0
                        om:setActive(true)

                        CommE:FireServer("Ken", true)

                    end
                end
            end

            AutoKenModule.Running = false

        end)
    end

    function AutoKenModule:SetAutoKen(state)

        self.Enabled = state

        if state then
            startAutoKen()
        end

    end

    return AutoKenModule

end
