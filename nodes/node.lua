--RasPegacy v0.1
--Main Node

gl.setup(720, 486)

local curView = " "
--local font = resource.load_font("Exo2.otf")

-- Watch the view.json file to see which display the user wants
local json = require "json"
util.file_watch("view.json", function(content)
    Vson = json.decode(content)
    VC = Vson.view
    curView = VC.top
end)

function node.render()
    --future: check for day/night, change background accordingly
    --if headlights on? or time of day?
    gl.clear(0, 0, 0, 0)

    -- Render the menu area
    local menu = resource.render_child("menu")
    menu:draw(0,0,720,40)
    menu:dispose()
    
    -- Select which view the user has selected then render that child
        
    if curView == "1" then
        local basic = resource.render_child("basic")
        basic:draw(0, 40, 720, 446)
        basic:dispose()
    elseif curView == "2" then
        local graph = resource.render_child("graph")
        graph:draw(0, 40, 720, 446)
        graph:dispose()
    elseif curView == "3" then
        local blocks = resource.render_child("blocks")
        blocks:draw(0, 40, 720, 446)
        blocks:dispose()
    end

    -- Do stuff?
end
