#DDRM Level Editor 3.0

import tkinter
root = tkinter.Tk()
import pygame
pygame.init()
import penguinsmodule as pm #type: ignore
import os
import json

# --- THEMES ---
#Default: https://coolors.co/palette/10002b-240046-3c096c-5a189a-7b2cbf-9d4edd-c77dff-e0aaff
#Cherry: https://coolors.co/palette/590d22-800f2f-a4133c-c9184a-ff4d6d-ff758f-ff8fa3-ffb3c1-ffccd5-fff0f3
#Sea: https://coolors.co/palette/012a4a-013a63-01497c-014f86-2a6f97-2c7da0-468faf-61a5c2-89c2d9-a9d6e5
#Sunset: https://coolors.co/palette/03071e-370617-6a040f-9d0208-d00000-dc2f02-e85d04-f48c06-faa307-ffba08
#Steel: https://coolors.co/palette/f8f9fa-e9ecef-dee2e6-ced4da-adb5bd-6c757d-495057-343a40-212529
#Pastel: https://coolors.co/palette/fbf8cc-fde4cf-ffcfd2-f1c0e8-cfbaf0-a3c4f3-90dbf4-8eecf5-98f5e1-b9fbc0
#Meadow: https://coolors.co/palette/d9ed92-b5e48c-99d98c-76c893-52b69a-34a0a4-168aad-1a759f-1e6091-184e77
#Verdant: https://coolors.co/palette/004b23-006400-007200-008000-38b000-70e000-9ef01a-ccff33
#unnamed green: https://coolors.co/palette/d8f3dc-b7e4c7-95d5b2-74c69d-52b788-40916c-2d6a4f-1b4332-081c15
#Dreamscape: https://coolors.co/palette/9ba9ff-a5adff-afb1ff-b9b5ff-c4baff-cebeff-d8c2ff-e2c6ff-eccaff
#unnamed red: https://coolors.co/palette/fc9ca2-fb747d-fa4c58-f92432-e30613-c70512-9f040e-77030b-500207
#better unnamed red: https://coolors.co/palette/641220-6e1423-85182a-a11d33-a71e34-b21e35-bd1f36-c71f37-da1e37-e01e37
#unnamed teal: https://coolors.co/palette/99e2b4-88d4ab-78c6a3-67b99a-56ab91-469d89-358f80-248277-14746f-036666

theme = "default"
colorPalette = {
    "default": {
        "shade1": "#E0AAFF", #lightest
        "shade2": "#C77DFF",
        "shade3": "#9D4EDD",
        "shade4": "#7B2CBF",
        "shade5": "#5A189A",
        "shade6": "#3C096C",
        "shade7": "#240046",
        "shade8": "#10002B", #darkest
        },
    "steel": {
        "shade1": "#E9ECEF", #lightest
        "shade2": "#DEE2E6",
        "shade3": "#CED4DA",
        "shade4": "#ADB5BD",
        "shade5": "#6C757D",
        "shade6": "#495057",
        "shade7": "#343A40",
        "shade8": "#212529", #darkest
        },
    "cherry": {
        "shade1": "#FFCCD5", #lightest
        "shade2": "#FFB3C1",
        "shade3": "#FF8FA3",
        "shade4": "#FF4D6D",
        "shade5": "#C9184A",
        "shade6": "#A4133C",
        "shade7": "#800F2F",
        "shade8": "#590D22", #darkest
        },
    "seablue": {
        "shade1": "#A9D6E5", #lightest
        "shade2": "#89C2D9",
        "shade3": "#468FAF",
        "shade4": "#2C7DA0",
        "shade5": "#2A6F97",
        "shade6": "#01497C",
        "shade7": "#013A63",
        "shade8": "#012A4A", #darkest
        },
    "asparagus": {
        "shade1": "#CCFF33", #lightest
        "shade2": "#9EF01A",
        "shade3": "#70E000",
        "shade4": "#38B000",
        "shade5": "#008000",
        "shade6": "#007200",
        "shade7": "#006400",
        "shade8": "#004B23", #darkest
        },
    "mint": {
        "shade1": "#D8F3DC", #lightest
        "shade2": "#B7E4C7",
        "shade3": "#74C69D",
        "shade4": "#52B788",
        "shade5": "#40916C",
        "shade6": "#2D6A4F",
        "shade7": "#1B4332",
        "shade8": "#081C15", #darkest
        },
    "dreamscape": { #needs work
        "shade8": "#9BA9FF", #darkest
        "shade7": "#A5ADFF",
        "shade6": "#AFB1FF",
        "shade5": "#B9B5FF",
        "shade4": "#C4BAFF",
        "shade3": "#CEBEFF",
        "shade2": "#D8C2FF",
        "shade1": "#E2C6FF", #lightest
        },
    "red": {
        "shade1": "#FC9CA2", #lightest
        "shade2": "#FB747D",
        "shade3": "#FA4C58",
        "shade4": "#F92432",
        "shade5": "#E30613",
        "shade6": "#C70512",
        "shade7": "#9F040E",
        "shade8": "#500207", #darkest
        },
    "teal": {
        "shade1": "#99E2B4", #lightest
        "shade2": "#88D4AB",
        "shade3": "#78C6A3",
        "shade4": "#56AB91",
        "shade5": "#469D89",
        "shade6": "#358F80",
        "shade7": "#14746F",
        "shade8": "#036666", #darkest
        },
    "eyesore": {
        "shade1": "#10FF15", #lightest
        "shade2": "#20F035",
        "shade3": "#30E055",
        "shade4": "#40D075",
        "shade5": "#50C085",
        "shade6": "#60B065",
        "shade7": "#70A045",
        "shade8": "#809025", #darkest
        },
    "theme": {
        "shade1": "#", #lightest
        "shade2": "#",
        "shade3": "#",
        "shade4": "#",
        "shade5": "#",
        "shade6": "#",
        "shade7": "#",
        "shade8": "#", #darkest
        },
    "other": {
        "black": "#000000",
        "white": "#FFFFFF",
        "delete": "#FF0000",
        "edit": "#00AA00",
        "play": "#0000FF",
        "deleteout": "#AA0000",
        "editout": "#005500",
        "playout": "#0000AA",
        }
}

class Menu():
    
    def __init__(self, levels_path):
        
        #setup screen
        self.scX = root.winfo_screenwidth() * 0.75
        self.scY = root.winfo_screenheight() * 0.75
        self.screen = pygame.display.set_mode((self.scX, self.scY), pygame.SRCALPHA)
        pygame.display.set_caption('DoDoReMi Level Editor V0.3')
        
        #get data from levels folder
        levels = {}
        for entry in os.scandir(levels_path):
            if entry.is_file():
                print(f"File: {entry.name} (Path: {entry.path})")
                levels[entry.name] = entry.path
        
        #create list of button objects
        self.levelButtons = []
        id = 1
        for i in levels.values():
            self.levelButtons.append(self.LevelButton(self, self.screen, i, id))
            id += 1
        
        #globals
        self.scroll = 0
    
    def update(self):
        self.screen.fill(colorPalette[theme]["shade6"])
        for i in self.levelButtons: i.update()
        pygame.display.update()
    
    def recieveClick(self, pos):
        for i in self.levelButtons:
            if i.recieveClick(pos): print(i.name)

    class LevelButton():
        
        def __init__(self, parent, screen, path, id):
            
            self.parent = parent
            self.screen = screen
            self.id = id
            
            #get data from json
            with open(path, "r") as f:
                loaded_data = json.load(f)
            
            self.name, self.author, self.songauthor, self.length, self.bpm, self.key, self.keyscale, = loaded_data["name"], loaded_data["author"], loaded_data["songauthor"], loaded_data["length"], loaded_data["bpm"], loaded_data["key"], loaded_data["keyscale"]
        
        def update(self):
            
            #consts
            leftmargin = 0.05
            rightmargin = 0.95
            spacing = 0.28
            offset = 0.25
            scrollm = 0.1
            playleft = 0.65
            editleft = 0.75
            deleteleft = 0.85
            subbuttonymargin = 0.005
            
            
            y = (self.id * spacing - offset) - self.parent.scroll * scrollm
            
            #box fill
            pygame.draw.rect(self.screen, colorPalette[theme]["shade5"], pm.drawAbsolute(leftmargin, y, rightmargin, y + 0.25, self.parent.scX, self.parent.scY), 0, 10)
            
            #playback button
            #pygame.draw.rect(self.screen, colorPalette["other"]["play"], pm.drawAbsolute(playleft, y + subbuttonymargin, editleft, y + 0.25 - subbuttonymargin, self.parent.scX, self.parent.scY), 0, 1)
            #pygame.draw.rect(self.screen, colorPalette["other"]["playout"], pm.drawAbsolute(playleft, y + subbuttonymargin, editleft, y + 0.25 - subbuttonymargin, self.parent.scX, self.parent.scY), 5, 1)
            
            #edit button
            #pygame.draw.rect(self.screen, colorPalette["other"]["edit"], pm.drawAbsolute(editleft, y + subbuttonymargin, deleteleft, y + 0.25 - subbuttonymargin, self.parent.scX, self.parent.scY), 0, 1)
            #pygame.draw.rect(self.screen, colorPalette["other"]["editout"], pm.drawAbsolute(editleft, y + subbuttonymargin, deleteleft, y + 0.25 - subbuttonymargin, self.parent.scX, self.parent.scY), 5, 1)
            
            #delete button
            #pygame.draw.rect(self.screen, colorPalette["other"]["delete"], pm.drawAbsolute(deleteleft, y + subbuttonymargin, rightmargin, y + 0.25 - subbuttonymargin, self.parent.scX, self.parent.scY), 0, 1)
            #pygame.draw.rect(self.screen, colorPalette["other"]["deleteout"], pm.drawAbsolute(deleteleft, y + subbuttonymargin, rightmargin, y + 0.25 - subbuttonymargin, self.parent.scX, self.parent.scY), 5, 1)
            
            #box outline
            pygame.draw.rect(self.screen, colorPalette[theme]["shade7"], pm.drawAbsolute(leftmargin, y, rightmargin, y + 0.25, self.parent.scX, self.parent.scY), 5, 10)
            
            self.pos = pm.drawAbsolute(leftmargin, y, rightmargin, y + 0.25, self.parent.scX, self.parent.scY)
            
            #draw text
            pm.text(self.screen, #name
                self.name,
                pm.drawAbsolute(leftmargin + 0.01, y + 0.05, 0, 0, self.parent.scX, self.parent.scY),
                colorPalette[theme]["shade2"],
                48 - len(self.name), #fontsize
                center="left",
                font="C:/Windows/Fonts/Segoeuib.ttf"
                )
            pm.text(self.screen, #songauthor
                self.songauthor,
                pm.drawAbsolute(leftmargin + 0.01, y + 0.125, 0, 0, self.parent.scX, self.parent.scY),
                colorPalette[theme]["shade2"],
                32 - len(self.name), #fontsize
                center="left",
                font="C:/Windows/Fonts/Seguisb.ttf"
                )
            pm.text(self.screen, #length
                f"Length: {self.length}",
                pm.drawAbsolute(leftmargin + 0.27, y + 0.05, 0, 0, self.parent.scX, self.parent.scY),
                colorPalette[theme]["shade3"],
                24, #fontsize
                center="left",
                font="C:/Windows/Fonts/Seguisbi.ttf"
                )
            pm.text(self.screen, #key
                f"Key: {self.key} {self.keyscale}",
                pm.drawAbsolute(leftmargin + 0.27, y + 0.125, 0, 0, self.parent.scX, self.parent.scY),
                colorPalette[theme]["shade3"],
                24, #fontsize
                center="left",
                font="C:/Windows/Fonts/Seguisbi.ttf"
                )
            pm.text(self.screen, #bpm
                f"Bpm: {self.bpm}",
                pm.drawAbsolute(leftmargin + 0.27, y + 0.2, 0, 0, self.parent.scX, self.parent.scY),
                colorPalette[theme]["shade3"],
                24, #fontsize
                center="left",
                font="C:/Windows/Fonts/Seguisbi.ttf"
                )
            
            
            #debug
            for i in range(8):
                pygame.draw.rect(self.screen, colorPalette[theme][f"shade{i + 1}"], [10, i * 10 + 10, 10, 10], 5, 10)
        
        def recieveClick(self, pos):
            #checks if click is within bounds of border
            if self.pos[2] + self.pos[0] > pos[0] > self.pos[0] and self.pos[3] + self.pos[1] > pos[1] > self.pos[1]: return True
            else: return False

def main():
    
    #init
    menu = Menu("c:/users/benjaminsullivan/downloads/ddrm3/testsongs")
    clock = pygame.time.Clock()
    running = True
    menu.update()
    while running:
        
        time_delta = clock.tick(60)/1000.0
        
        #process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEWHEEL:
                
                menu.scroll -= event.y
                if menu.scroll < 0: menu.scroll = 0
                if menu.scroll > 9999: menu.scroll = 9999
            
            if event.type == pygame.MOUSEBUTTONDOWN: #activates for any moues input, fix later
                menu.recieveClick(pygame.mouse.get_pos())
        
        menu.update()

main()