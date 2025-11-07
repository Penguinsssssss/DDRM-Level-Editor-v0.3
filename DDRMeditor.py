#DDRM Editor 3.1

import tkinter
root = tkinter.Tk()
import pygame
import penguinsmodule as pm #type: ignore
import os
import json
import math
import time

theme = "seaglass"
path = None
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
    "seaglass": {
        "shade1": "#A9D6E5", #lightest
        "shade2": "#89C2D9",
        "shade3": "#468FAF",
        "shade4": "#2C7DA0",
        "shade5": "#2A6F97",
        "shade6": "#01497C",
        "shade7": "#013A63",
        "shade8": "#012A4A", #darkest
        },
    "meadow": {
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
    "other": {
        "black": "#000000",
        "white": "#FFFFFF",
        "del1": "#FF7777", #button fills
        "edit1": "#77FF77",
        "play1": "#7777FF",
        "del2": "#AA4444", #button outlines
        "edit2": "#44AA44",
        "play2": "#4444AA",
        "del3": "#881111", #selected variants
        "edit3": "#118811",
        "play3": "#333388",
        },
    "notes": {
        "drums": "#e12929",
        "drumsout": "#940c0c",
        "perc": "#e9852d",
        "percout": "#9c500e",
        "signature": "#fed141",
        "signatureout": "#ad8916",
        "harmony": "#1ec88d",
        "harmonyout": "#038155",
        "melody": "#287ce7",
        "melodyout": "#0b4b9c",
        "bass": "#6b3ad8",
        "bassout": "#3c188c",
        }
}

class Editor:
    
    def __init__(self, levelPath):
        
        #setup screen
        self.scX = root.winfo_screenwidth() * 0.75
        self.scY = root.winfo_screenheight() * 0.75
        self.screen = pygame.display.set_mode((self.scX, self.scY), pygame.SRCALPHA)
        pygame.display.set_caption('DoDoReMi Level Editor V0.3')
        
        #get filepath
        self.path = levelPath
        with open(levelPath, "r") as f:
            loaded_data = json.load(f)
        
        self.name, self.author, self.songauthor, self.length, self.bpm, self.key, self.keyscale, self.chart = loaded_data["name"], loaded_data["author"], loaded_data["songauthor"], loaded_data["length"], loaded_data["bpm"], loaded_data["key"], loaded_data["keyscale"], loaded_data["chart"]
        self.scroll = 0
        
        #create utilbar and notes
        self.utilBar = self.UtilBar(self)
        
        self.notes = []
        for i in self.chart[0]["notes"]:
            self.notes.append(self.Note(self, i, self.chart[0]["part"]))
    
    def update(self):
        
        #fill screen
        self.screen.fill(colorPalette[theme]["shade6"])
        
        #draw screen elements
        self.drawChart()
        self.utilBar.update()
        
        #show updates to the user
        pygame.display.update()
    
    def drawChart(self):
        
        #for i in each individual part
        for i in self.chart:
            
            #consts
            height = 0.25
            spacing = 0.08
            thickness = 0.005
            
            #draw lanes in backdrop
            for j in range(i["lanes"]):
                pygame.draw.rect(self.screen, colorPalette[theme]["shade4"], pm.drawAbsolute(0, height + (j * spacing), 1, height + (j * spacing) + thickness, self.scX, self.scY), 0)
            
            #allow each note object to draw itself
            for j in self.notes: j.update()
    
    def recieveClick(self, pos):
        
        #activated upon any form of mouse input from the user
        #sends signal to each screen element
        
        self.utilBar.recieveClick(pos)
        for i in self.notes: i.recieveClick(pos)
    
    class Note():
        
        def __init__(self, parent, npos, part):
            self.parent = parent
            self.npos = npos
            self.part = part
            
            self.held = False
        
        def update(self):
            
            height = 0.25
            spacing = 0.08 #per beat
            thickness = 0.005
            noteSpacing = 8 #smaller is larger gaps between notes
            
            #update position based on zoom and scroll
            if self.held == False: self.pos = [(self.npos[0] + self.parent.scroll / 5) * (self.parent.scX / noteSpacing), (height * self.parent.scY) + ((self.npos[1] - 1) * (spacing * self.parent.scY)) + ((thickness * self.parent.scY) / 2)]
            else: self.pos = pygame.mouse.get_pos()
            self.radius = 20
            
            #draw fill
            pygame.draw.circle(self.parent.screen, colorPalette["notes"][self.part], self.pos, self.radius, 0)
            
            #draw outline
            pygame.draw.circle(self.parent.screen, colorPalette["notes"][self.part + "out"], self.pos, self.radius, 5)

            
        def recieveClick(self, pos):
            
            #get distance from centre of note to mouse
            distance = math.sqrt((pos[0] - self.pos[0]) ** 2 + (pos[1] - self.pos[1]) ** 2)
            
            #activate if within note size
            if distance < self.radius:
                print(self.npos)
                self.held = True
        
    class UtilBar:
        
        def __init__(self, parent):
            
            self.parent = parent
            
            self.thickness = 0.05
            buttonLen = 0.07
            
            #dummy buttons
            self.buttons = []
            self.buttons.append(self.UtilButton(self, "File", ["load", "save"], [0, 0, buttonLen, self.thickness]))
            self.buttons.append(self.UtilButton(self, "Edit", ["undo", "redo"], [buttonLen, 0, buttonLen * 2, self.thickness]))
            self.buttons.append(self.UtilButton(self, "View", ["playback", "open file location"], [buttonLen * 2, 0, buttonLen * 3, self.thickness]))
            self.buttons.append(self.UtilButton(self, "Tools", ["zoom", "meter"], [buttonLen * 3, 0, buttonLen * 4, self.thickness]))
        
        def update(self):
            
            #draw top bar
            pygame.draw.rect(self.parent.screen, colorPalette[theme]["shade8"], pm.drawAbsolute(0, 0, 1, self.thickness, self.parent.scX, self.parent.scY), 0)
            
            #allow buttons to update themselves
            
            for i in self.buttons:
                i.update()
                
                #"highlight" if mouse is ontop
                i.darken(pygame.mouse.get_pos())
        
        def recieveClick(self, pos):
            
            #allow each button to check if they have been clicked
            for i in self.buttons: i.recieveClick(pos)
        
        class UtilButton:
            
            def __init__(self, parent, title, options, dims):
                self.parent = parent
                self.title = title
                self.options = options
                self.dims = dims
                
                #"highlight"
                self.isDark = False
            
            def update(self):
                
                #draw fill
                pygame.draw.rect(self.parent.parent.screen, colorPalette[theme]["shade6" if self.isDark else "shade5"], pm.drawAbsolute(self.dims[0], self.dims[1], self.dims[2], self.dims[3], self.parent.parent.scX, self.parent.parent.scY), 0)
                
                #draw outline
                pygame.draw.rect(self.parent.parent.screen, colorPalette[theme]["shade7" if self.isDark else "shade6"], pm.drawAbsolute(self.dims[0], self.dims[1], self.dims[2], self.dims[3], self.parent.parent.scX, self.parent.parent.scY), 2)
                
                #update own position based on zoom and scroll
                self.pos = pm.drawAbsolute(self.dims[0], self.dims[1], self.dims[2], self.dims[3], self.parent.parent.scX, self.parent.parent.scY)
                
                #draw label
                pm.text(self.parent.parent.screen,
                    self.title,
                    pm.drawAbsolute(((self.dims[2] - self.dims[0]) / 2) + self.dims[0], self.parent.thickness / 2, 0, 0, self.parent.parent.scX, self.parent.parent.scY)[0:2],
                    colorPalette[theme]["shade3" if self.isDark else "shade2"],
                    20,
                    center="center",
                    font="C:/Windows/Fonts/Ebrima.ttf"
                    )
            
            def darken(self, pos):
                
                #highlight if mouse is ontop
                if self.pos[2] + self.pos[0] > pos[0] > self.pos[0] and self.pos[3] + self.pos[1] > pos[1] > self.pos[1]: self.isDark = True
                else: self.isDark = False
            
            def recieveClick(self, pos):
                
                #activates upon mouse input, if clicked start a new loop in which its own menu is shown
                if self.pos[2] + self.pos[0] > pos[0] > self.pos[0] and self.pos[3] + self.pos[1] > pos[1] > self.pos[1]:
                    
                    active = True
                    clock = pygame.time.Clock()
                    
                    while active:
                        
                        time_delta = clock.tick(60)/1000.0
                        
                        self.update()
                        
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                active = False

def main():
    
    pygame.init()
    
    #create editor object
    editor = Editor(path)
    
    clock = pygame.time.Clock()
    running = True
    editor.update()
    while running:
        
        #game runs at 60fps
        time_delta = clock.tick(60)/1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            #updates scroll for editor
            if event.type == pygame.MOUSEWHEEL:
                
                print(editor.scroll)
                
                editor.scroll -= event.y
                if editor.scroll < -9999: editor.scroll = -9999
                if editor.scroll > 9999: editor.scroll = 9999
            
            if event.type == pygame.MOUSEBUTTONDOWN: #activates for any moues input, fix later
                editor.recieveClick(pygame.mouse.get_pos())
        
        editor.update()

#code is meant to be run as a package in the menu script
if __name__ == "__main__":
    path = r"c:\Users\BenjaminSullivan\Downloads\ddrm3\test_song.json"
    main()
