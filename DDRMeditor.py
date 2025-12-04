#DDRM Editor 3.1

import tkinter
root = tkinter.Tk()
from tkinter import filedialog
import pygame
import penguinsmodule as pm #type: ignore
import os
import json
import math
import time

path = None

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
        
        self.name = loaded_data["name"]
        self.author = loaded_data["author"]
        self.songauthor = loaded_data["songauthor"]
        self.length = loaded_data["length"]
        self.bpm = loaded_data["bpm"]
        self.key = loaded_data["key"]
        self.keyscale = loaded_data["keyscale"]
        self.signature = loaded_data["signature"]
        self.chart = loaded_data["chart"]
        
        self.scroll = 0
        self.noteSpacing = 15
        
        #consts
        self.meter_numerator = self.signature[0]
        self.meter_denominator = self.signature[1]
        
        #create utilbar
        self.utilBar = self.UtilBar(self)
        
        #create playback
        self.playback = self.Playback(self)
        
        self.status = "edit"
        
        #create notes
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
            self.height = 0.25
            self.spacing = 0.08
            self.thickness = 0.005
            
            #draw lanes in backdrop
            
            self.nodes = []
            
            for j in range(i["lanes"]):
                
                #draw lane
                pygame.draw.rect(self.screen,
                                colorPalette["notes"][i["part"] + "out"], #draw lane color as outside of notes
                                pm.drawAbsolute(0, self.height + (j * self.spacing),
                                                1,
                                                self.height + (j * self.spacing) + self.thickness,
                                                self.scX,
                                                self.scY),
                                0)
                
                #draw beats in the lane
                pxsperbeat = self.scX / self.noteSpacing
                beats = int(self.scX / pxsperbeat) + 56 #add buffer (temp debug)
                
                for k in range(beats):
                    beat = (k + self.scroll / 5) * pxsperbeat
                    
                    y = pm.drawAbsolute(
                        0,
                        (self.height + (j * self.spacing)) + (self.thickness / 2),
                        0, 0, self.scX, self.scY
                    )[1] #only get y val
                    
                    #pos in pixels
                    pos = [beat, y]
                    
                    #highlight the first note of every measure
                    size = 7 if k % self.meter_numerator == 0 else 3
                    
                    pygame.draw.circle(self.screen,
                                        colorPalette["notes"][i["part"]],
                                        pos,
                                        size,
                                        0)
                    
                    #pos in beats
                    self.nodes.append([k, j])
            
            #allow each note object to draw itself
            for j in self.notes: j.update()
    
    def recieveClick(self, pos, button):
        
        #activated upon any form of mouse input from the user
        #sends signal to each screen element
        if self.status == "edit":
            if button == "LEFT":
                
                wasActive = self.utilBar.checkActive()
                
                noteClicked = False
                for i in self.notes:
                    if i.recieveClick(pos, button):
                        self.notes.remove(i)
                        noteClicked = True
                if self.utilBar.recieveClick(pos, button):
                    return
                elif not noteClicked and not wasActive:
                    closest = self.findClosest(pos, self.nodes)
                    measure = [(closest[0] - closest[0] % self.meter_numerator) / self.meter_numerator, #measure
                                closest[0] % self.meter_numerator + 1, #beat
                                self.meter_numerator] #numerator
                    self.notes.append(self.Note(self, [measure, closest[1] + 1, 0], "melody"))
            elif button == "RIGHT":
                for i in self.notes: i.recieveClick(pos, button)
    
    def findClosest(self, pos, nodes): #taken from online source
            closest_point = None
            min_distance = float('inf')  # Initialize with a very large distance
            
            for point in nodes:
                # Calculate Euclidean distance
                nodepos = [(point[0] + self.scroll / 5) * (self.scX / self.noteSpacing),
                           pm.drawAbsolute(0, (self.height + (point[1] * self.spacing)) + (self.thickness / 2), 0, 0, self.scX, self.scY)[1]]
                distance = math.sqrt((pos[0] - nodepos[0])**2 + (pos[1] - nodepos[1])**2)
                
                if distance < min_distance:
                    min_distance = distance
                    closest_point = point
            
            return closest_point
    
    def devdebug(self):
        for i in self.notes: print(i.npos)
    
    def writeNotes(self):
        noteslist = []
        for i in self.notes: noteslist.append([i.npos, i.lane, i.pitch])
        return noteslist
    
    class Note:
        
        def __init__(self, parent, data, part):
            self.parent = parent
            self.npos = data[0]
            self.measure = (self.npos[0] + (self.npos[1] - 1) / self.npos[2]) * self.parent.meter_numerator
            self.lane = data[1]
            self.pitch = data[2]
            self.part = part
            
            self.held = False
            
            self.isDark = False
        
        def update(self):
            
            height = 0.25
            spacing = 0.08 #per beat
            thickness = 0.005
            self.radius = 20
            
            #update position based on zoom and scroll
            if self.held == False:
                self.pos = [(self.measure + self.parent.scroll / 5) * (self.parent.scX / self.parent.noteSpacing),
                            (height * self.parent.scY) + ((self.lane - 1) * (spacing * self.parent.scY)) + ((thickness * self.parent.scY) / 2)]
            else: self.pos = pygame.mouse.get_pos()
            
            #draw fill
            pygame.draw.circle(self.parent.screen,
                                colorPalette["notes"][self.part],
                                self.pos, self.radius,
                                0) #filled circle
            
            #draw outline
            pygame.draw.circle(self.parent.screen,
                                colorPalette["notes"][self.part + "out"],
                                self.pos,
                                self.radius,
                                5) #outline
        
        def recieveClick(self, pos, button):
            
            distance = math.sqrt((pos[0] - self.pos[0]) ** 2 + (pos[1] - self.pos[1]) ** 2)
            
            #activate if within note size
            
            if distance < self.radius:
                if button == "LEFT": #delete
                    return True
                else: self.isDark = True #darken
            else: self.isDark = False #undarken
    
    class UtilBar:
        
        def __init__(self, parent):
            
            self.parent = parent
            
            self.thickness = 0.05
            buttonLen = 0.07
            
            #dummy buttons
            self.buttons = []
            self.buttons.append(self.UtilButton(self, "File", ["New", "Open", "Save", "Save As", "Export"], [0, 0, buttonLen, self.thickness]))
            self.buttons.append(self.UtilButton(self, "Edit", ["Edit Song Info", "Change Audio"], [buttonLen, 0, buttonLen * 2, self.thickness]))
            self.buttons.append(self.UtilButton(self, "Themes", list(colorPalette.keys()), [buttonLen * 2, 0, buttonLen * 3, self.thickness]))
            self.buttons.append(self.UtilButton(self, "Tools", ["Undo", "Redo", "Zoom", "Edit Meter"], [buttonLen * 3, 0, buttonLen * 4, self.thickness]))
            self.buttons.append(self.UtilButton(self, "Song", ["Add Part", "Add Instrument"], [buttonLen * 4, 0, buttonLen * 5, self.thickness]))
        
        def update(self):
            
            #draw top bar
            pygame.draw.rect(self.parent.screen,
                            colorPalette[theme]["shade7"],
                            pm.drawAbsolute(0, 0, 1,
                                            self.thickness,
                                            self.parent.scX,
                                            self.parent.scY),
                            0)
            
            #allow buttons to update themselves
            
            for i in self.buttons:
                
                i.update()
                
                #"highlight" if mouse is ontop
                i.darken(pygame.mouse.get_pos())
        
        def recieveClick(self, pos, button):
            
            for i in self.buttons:
                #check if an option is clicked
                if i.active and i.dropDownPos is not None and i.dropDownPos[0] + i.dropDownPos[2] > pos[0] > i.dropDownPos[0] and i.dropDownPos[1] + i.dropDownPos[3] > pos[1] > i.dropDownPos[1]:
                    i.dropdownrecieveClick(pos, button)
                    return True
            
            #turn off all dropdowns
            for i in self.buttons: i.active = False
            
            #turn on a new dropdown if it has been clicked
            for i in self.buttons:
                if i.pos[0] < pos[0] < i.pos[0] + i.pos[2] and i.pos[1] < pos[1] < i.pos[1] + i.pos[3]:
                    i.active = True
                    return True
        
        def checkActive(self):
            for i in self.buttons:
                if i.active: return True
        
        class UtilButton:
            
            def __init__(self, parent, title, options, dims):
                self.parent = parent
                self.title = title
                self.options = options
                self.dims = dims
                
                #"highlight"
                self.isDark = False
                self.optionhighlighted = None
                self.active = False
                
                self.dropDownPos = None
            
            def update(self):
                
                if self.active:
                    
                    pos = pygame.mouse.get_pos()
                    
                    self.buttonDepth = 0.05
                    
                    self.dropDownPos = pm.drawAbsolute(self.dims[0],
                                                        self.dims[3] - self.dims[1],
                                                        self.dims[2],
                                                        self.dims[3] + (self.buttonDepth * len(self.options)),
                                                        self.parent.parent.scX,
                                                        self.parent.parent.scY)
                    
                    pygame.draw.rect(self.parent.parent.screen,
                                    colorPalette[theme]["shade4"],
                                    self.dropDownPos, 0)
                    pygame.draw.rect(self.parent.parent.screen,
                                    colorPalette[theme]["shade5"],
                                    self.dropDownPos, 2)
                    
                    #checks to see if each option is highlighted
                    if self.dropDownPos[2] + self.dropDownPos[0] > pos[0] > self.dropDownPos[0] and self.dropDownPos[3] + self.dropDownPos[1] > pos[1] > self.dropDownPos[1]: #dim below selected option
                        yndex = pos[1] / self.parent.parent.scY
                        counter = -1
                        while yndex > self.buttonDepth:
                            yndex -= self.buttonDepth
                            counter += 1
                        posy = self.dropDownPos[1] + ((counter) * self.buttonDepth * self.parent.parent.scY)
                        
                        pygame.draw.rect(self.parent.parent.screen,
                                        colorPalette[theme]["shade7"],
                                        [self.dropDownPos[0],
                                            posy,
                                            self.dropDownPos[2],
                                            self.buttonDepth * self.parent.parent.scY])
                        
                        self.optionhighlighted = counter
                    
                    else:
                        self.optionhighlighted = None
                    
                    #draws each option in a dropdown
                    index = 1
                    for i in self.options:
                        
                        textsize = 16 - round(len(i) / 2 if len(i) > 11 else 3)
                        
                        pm.text(self.parent.parent.screen,
                            i.capitalize(),
                            pm.drawAbsolute(((self.dims[2] - self.dims[0]) / 2) + self.dims[0], self.parent.thickness / 2 + (self.buttonDepth * index), 0, 0, self.parent.parent.scX, self.parent.parent.scY)[0:2],
                            colorPalette[theme]["shade2"],
                            textsize,
                            center="center",
                            font="C:/Windows/Fonts/Ebrima.ttf"
                        )
                        index += 1
                    
                #draw fill
                pygame.draw.rect(self.parent.parent.screen,
                                colorPalette[theme]["shade6" if self.isDark else "shade5"],
                                pm.drawAbsolute(self.dims[0],
                                                self.dims[1],
                                                self.dims[2],
                                                self.dims[3],
                                                self.parent.parent.scX,
                                                self.parent.parent.scY),
                                0)
                
                #draw outline
                pygame.draw.rect(self.parent.parent.screen,
                                colorPalette[theme]["shade7" if self.isDark else "shade6"],
                                pm.drawAbsolute(self.dims[0],
                                                self.dims[1],
                                                self.dims[2],
                                                self.dims[3],
                                                self.parent.parent.scX,
                                                self.parent.parent.scY),
                                2)
                
                #update own position based on zoom and scroll
                self.pos = pm.drawAbsolute(self.dims[0],
                                            self.dims[1],
                                            self.dims[2],
                                            self.dims[3],
                                            self.parent.parent.scX,
                                            self.parent.parent.scY)
                
                #draw label
                pm.text(self.parent.parent.screen,
                    self.title,
                    pm.drawAbsolute(((self.dims[2] - self.dims[0]) / 2) + self.dims[0], self.parent.thickness / 2, 0, 0, self.parent.parent.scX, self.parent.parent.scY)[0:2],
                    colorPalette[theme]["shade2"],
                    18,
                    center="center",
                    font="C:/Windows/Fonts/Ebrima.ttf"
                    )
                
            def darken(self, pos):
                
                #highlight if mouse is ontop
                if self.pos[2] + self.pos[0] > pos[0] > self.pos[0] and self.pos[3] + self.pos[1] > pos[1] > self.pos[1]: self.isDark = True
                else: self.isDark = False
            
            def recieveClick(self, pos, button):
                
                if self.active:
                    self.dropdownrecieveClick(pos, button)
                
                #activates upon mouse input, if clicked start a new loop in which its own menu is shown
                elif self.pos[2] + self.pos[0] > pos[0] > self.pos[0] and self.pos[3] + self.pos[1] > pos[1] > self.pos[1]:
                    
                    self.active = not self.active
            
            def dropdownrecieveClick(self, pos, button):
                
                if self.dropDownPos is None:
                    self.active = False
                    return
                
                #checks if option was clicked
                if button == "LEFT" and self.dropDownPos[2] + self.dropDownPos[0] > pos[0] > self.dropDownPos[0] and self.dropDownPos[3] + self.dropDownPos[1] > pos[1] > self.dropDownPos[1]:
                    #runs respective code
                    self.functions(self.options[self.optionhighlighted])
                else:
                    #turns off dropdown loop
                    self.active = False
                    #passes click to Menu()
                    self.parent.parent.recieveClick(pos, button)
            
            def functions(self, function):
                print(f"function: {function}")
                if function in colorPalette: #change theme
                    theme = function
                elif function == "New":
                    print("new")
                elif function == "Open" or function == "Change Audio":
                    root.withdraw()
                    file_path = filedialog.askopenfilename(
                        title="Select a level",
                        filetypes=[("Json files", "*.json"), ("All files", "*.*")]
                    )
                    print(file_path)
                    root.destroy()
                elif function == "Save":
                    with open(self.parent.parent.path, 'r') as file: data = json.load(file)
                    data["chart"][0]["notes"] = self.parent.parent.writeNotes()
                    with open(self.parent.parent.path, 'w') as file: json.dump(data, file, indent=4)
                    print("file saved !")
                elif function == "Save As": pass
                elif function == "Export": pass
                else: pass
    
    class Playback:
        
        def __init__(self, parent):
            self.parent = parent
        
        def playback(self):
            self.parent.scroll = 0
            self.parent.status = "playback"

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
            if event.type == pygame.MOUSEWHEEL and editor.status == "edit":
                
                mods = pygame.key.get_mods()
                
                #hold alt to zoom
                if mods & pygame.KMOD_ALT:
                    editor.noteSpacing -= event.y
                    if editor.noteSpacing < 1: editor.noteSpacing = 1
                    if editor.noteSpacing > 9999: editor.noteSpacing = 9999
                    #print(f"zoom: {editor.noteSpacing}")
                
                #hold shift to scroll faster
                elif mods & pygame.KMOD_SHIFT:
                    editor.scroll += event.y * 10
                    if editor.scroll < -9999: editor.scroll = -9999
                    if editor.scroll > 0: editor.scroll = 0
                    #print(f"zoom: {editor.noteSpacing}")
                
                #scroll normal speed if no key is held
                else:
                    editor.scroll += event.y * 2
                    if editor.scroll < -9999: editor.scroll = -9999
                    if editor.scroll > 0: editor.scroll = 0
                    #print(f"scroll: {editor.scroll}")
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: editor.recieveClick(pygame.mouse.get_pos(), "LEFT")
                elif event.button == 3: editor.recieveClick(pygame.mouse.get_pos(), "RIGHT")
            
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_p: #run playback
                    editor.playback.playback()
        
        editor.update()

#code is meant to be run as a package in the menu script
if __name__ == "__main__":
    path = r"c:\Users\Benjaminsullivan\Downloads\ddrm3\testsongs\ddrm_library_ruins.json"
    main()