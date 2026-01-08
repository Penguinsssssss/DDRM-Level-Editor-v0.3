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
        "drag": "#77FF77" #used for dragselect
        },
    "notes": { #colors used to denote differing parts
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
        "select": "#999999", #temp, possibly change based on note in the future
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
        self.path = levelPath + "\chart.json"
        with open(self.path, "r") as f:
            loaded_data = json.load(f)
        
        #setup info from json
        self.name = loaded_data["name"]
        self.author = loaded_data["author"]
        self.songauthor = loaded_data["songauthor"]
        self.length = loaded_data["length"]
        self.bpm = loaded_data["bpm"]
        self.key = loaded_data["key"]
        self.keyscale = loaded_data["keyscale"]
        self.signature = loaded_data["signature"]
        self.offset = loaded_data["offset"]
        self.chart = loaded_data["chart"]
        
        #how far the user has scrolled in the chart
        self.scroll = 0
        
        #zoom; how many beats are fit on the screen at a time
        self.noteSpacing = 12
        
        #allows placing notes in differing time signatures
        self.meter_numerator = self.signature[0]
        self.meter_denominator = self.signature[1]
        
        #create utilbar
        self.utilBar = self.UtilBar(self)
        
        #switch between editing and playback (possibly menu aswell)
        self.status = "edit"
        
        #create playback object
        self.playback = self.Playback(self)
        
        #create notes
        self.notes = []
        for i in self.chart[0]["notes"]:
            self.notes.append(self.Note(self, i, self.chart[0]["part"]))
        
        # drag-select system
        self.dragging = False
        self.dragStart = None
        self.dragEnd = None
        
        self.partSelects = []
        for i in self.chart:
            self.partSelects.append(self.PartSelect(self, i["part"], len(self.partSelects)))
        
        for i in self.partSelects: print(i.part)
        
        self.inFocusPart = self.chart[0]
    
    def update(self):
        
        #fill screen
        self.screen.fill(colorPalette[theme]["shade6"])
        self.drawBackdrop()
        
        #draw screen elements
        self.drawChart()
        self.utilBar.update()
        for i in self.partSelects: i.update()
        
        #draw dragselect
        self.drawDragSelect()
        
        #update playback
        if self.status == "playback":
            self.playback.update()
        
        #show updates to the user
        pygame.display.update()
    
    def drawChart(self):
        
        #draw each part overlayed ontop of one another, will change to one part at a time later
        i = self.inFocusPart
            
        #consts
        self.height = 0.25
        self.spacing = 0.08
        self.thickness = 0.005
        
        #create blank list of valid nodes
        self.nodes = []
        
        #create lanes
        for j in range(i["lanes"]):
            
            #draw a lane
            pygame.draw.rect(self.screen,
                            colorPalette["notes"][i["part"] + "out"], #draw lane color as outside of notes
                            pm.drawAbsolute(0, self.height + (j * self.spacing),
                                            1,
                                            self.height + (j * self.spacing) + self.thickness,
                                            self.scX,
                                            self.scY),
                            0)
            
            #draw nodes in the lane
            pxspernode = self.scX / self.noteSpacing
            numnodes = int(self.scX / pxspernode) + 500 #add buffer (temp debug)
            
            for k in range(numnodes):
                node = (k + self.scroll / 5) * pxspernode
                
                y = pm.drawAbsolute(
                    0,
                    (self.height + (j * self.spacing)) + (self.thickness / 2),
                    0, 0, self.scX, self.scY
                )[1] #only get y val
                
                #pos in pixels
                pos = [node, y]
                
                #highlight the first note of every measure
                size = 7 if k % self.meter_numerator == 0 else 3
                
                pygame.draw.circle(self.screen,
                                    colorPalette["notes"][i["part"]],
                                    pos,
                                    size,
                                    0)
                
                #pos in nodes
                self.nodes.append([k, j])
        
        #allow each note object to draw itself
        for j in self.notes: j.update() #NOTE SELF.NOTES DOES NOT UPDATE AUTOMATICALLY WITH INFOCUSPART FIX LATER
    
    def drawBackdrop(self):
        
        beatxlength = 1 / self.noteSpacing #account for zoom
        
        for i in range(self.noteSpacing):
            
            #move to account for scroll
            scrolloffset = (self.scroll / (5 * self.noteSpacing)) % 1 #wrap back around the screen if too far
            
            #place start and end of bar based on zoom
            start = (i * beatxlength + scrolloffset) % 1
            end = start + beatxlength
            
            #only color if even number (ODD NUMBER BREAKS THIS!!! FIX LATER (currently cheating by not allowing the user to set an odd number))
            if (i % self.noteSpacing) % 2 == 0: pygame.draw.rect(self.screen, colorPalette[theme]["shade5"], pm.drawAbsolute(start, 0, end, 1, self.scX, self.scY), 0)
    
    def drawDragSelect(self):
        
        #draw drag selection box
        if self.dragging and self.dragStart and self.dragEnd:
            xs, ys = self.dragStart
            xe, ye = self.dragEnd
            left = min(xs, xe)
            top = min(ys, ye)
            width = abs(xs - xe)
            height = abs(ys - ye)
            pygame.draw.rect(self.screen, colorPalette["other"]["drag"], (left, top, width, height), 2)
    
    def finishDragSelect(self):
        
        #get drag selection box
        xs, ys = self.dragStart
        xe, ye = self.dragEnd
        left = min(xs, xe)
        right = max(xs, xe)
        top = min(ys, ye)
        bottom = max(ys, ye)
        
        #select highlighted notes
        for i in self.notes:
            nx, ny = i.pos
            if left <= nx <= right and top <= ny <= bottom:
                i.selected = True
            else:
                i.selected = False
        
        #setup for new drag
        self.dragging = False
        self.dragStart = None
        self.dragEnd = None
    
    def recieveClick(self, pos, button):
        
        #activated upon any form of mouse input from the user
        #sends signal to each screen element
        
        #only allow users to modify chart during editing
        if self.status == "edit":
            
            #deleting
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
            
            #selecting and dragselecting
            elif button == "RIGHT":
                
                #check for right click on empty space
                selected = False
                
                for i in self.notes:
                    if i.recieveClick(pos, button): selected = True
                
                #dragselect
                if not selected:
                    self.dragging = True
                    self.dragStart = pos
                    self.dragEnd = pos
    
    def recieveKey(self, key):
        
        #delete selection
        if key == pygame.K_DELETE or key == pygame.K_BACKSPACE:
            for i in reversed(self.notes):
                if i.selected: self.notes.remove(i)
        
        #move selection up
        if key == pygame.K_w or key == pygame.K_UP:
            for i in self.notes:
                if i.selected: i.lane = max(i.lane - 1, 1)
        
        #move selection down
        if key == pygame.K_s or key == pygame.K_DOWN:
            for i in self.notes:
                if i.selected: i.lane = min(i.lane + 1, 6) #NOTE HARDCODED TO 6, FIX LATER
        
        #move selection left
        if key == pygame.K_a or key == pygame.K_LEFT:
            for i in self.notes:
                if i.selected:
                    i.updateMeasure(-1)
        
        #move selection right
        if key == pygame.K_d or key == pygame.K_RIGHT:
            for i in self.notes:
                if i.selected:
                    i.updateMeasure(1)
        
        if key == pygame.K_t:
            self.inFocusPart = self.chart[1]
    
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
        #dev
        for i in self.notes: print(i.npos)
    
    def writeNotes(self):
        #dev
        noteslist = []
        for i in self.notes: noteslist.append([i.npos, i.lane, i.pitch])
        return noteslist
    
    def export(self):
        
        #initialize to a very large number (will add logic later)
        duration = 90000
        
        #guide is jackboxes system for keeping track of beats (stored in ms)
        guide = []
        
        #create guide
        i = 0
        while i < duration - (60000 / self.bpm) * 4:
            
            #upload in batches of four (jackboxes system)
            batch = []
            for j in range(4):
                batch.append(round(i))
                i += 60000 / self.bpm
            guide.append(batch)
        
        data = {
            "slug": self.name, #song title
            "composer": self.songauthor, #song author
            "duration": duration, #make automatic later
            "bucket": "Jackbox", #seemingly never used, but still initialized to "Jackbox"
            "scaleKey": self.key, #Ab - G#
            "scaleType": self.keyscale, #major, minor
            "guideStartOffset": self.offset, #no idea what this is for
            "guide": guide, #dark and light purple background animation
            "hasLocalizedBackingTrack": False, #i think this is meant to help people impliment their own songs, but I don't know how it works, nor do I have the actual individual recordings of parts of the songs I am using
            "beatmaps": [], #will be filled with somthing from each part later
            "preferredAssignments": [ #make automatic later
                
                [
                "melody",
                "rave-synth",
                ],
                
                ],
            "unlockType": "NumUniqueSongsCompleted", #unlock condition, comprehensive list below
            "unlockRequirement": 2 #amount of unlock condition needed, int
            }
        
        #add parts to beatmap field
        for i in self.chart: #for i in all parts
            
            inputs = []
            for j in i["notes"]:
                
                start = ((j[0][0] + (j[0][1] - 1) / j[0][2]) * self.meter_numerator * (60000 / self.bpm)) - self.offset #turn measures into beats into milliseconds
                
                inputs.append(
                    {
                        "start": round(start), #note placement in milliseconds
                        "lanes": [ #lane in which note is placed, no idea why its a list but sure i guess
                            j[1] - 1
                        ],
                        "notes": [
                            {
                                "start": 0, #is the sound offset by anything
                                "duration": 288, #how long does the sound play, 288 is placeholder
                                "note": 34 #what pitch is the sound, 34 is placeholder
                            }
                        ]
                    }
                )
            
            data["beatmaps"].append(
                {
            "slug": i["part"], #melody, drums, etc
            "type": "Discrete", #no idea what this does but things break without it
            "category": i["part"].capitalize(), #Melody, Drums, etc
            "difficulty": i["difficulty"], #1-5
            "instruments": ["rave-synth"], #valid instruments
            "instrumentRequirements": [i["part"].capitalize()], #melody, drums, etc, no idea what this does either...
            "events": [], #seemingly never used? initializing blank seems to work out just fine
            "inputs": inputs, #all notes
            "laneCount": i["lanes"] #1-6
            }
                )
        
        #hotwired to downloads, make this hook into jackbox directly eventually
        with open(r'c:\Users\Benja\Downloads\config.json', 'w') as json_file:
            json.dump(data, json_file, indent=2)
    
    class Note:
        
        def __init__(self, parent, data, part):
            
            #setup valid data
            self.parent = parent
            self.npos = data[0]
            print(self.npos)
            self.measure = (self.npos[0] + (self.npos[1] - 1) / self.npos[2]) * self.parent.meter_numerator
            self.lane = data[1]
            self.pitch = data[2]
            self.part = part
            
            #change color and behavior if selected
            self.selected = False
        
        def update(self):
            
            #consts
            height = 0.25
            spacing = 0.08 #per beat
            thickness = 0.005
            self.radius = 20
            
            #update position based on zoom and scroll
            self.pos = [(self.measure + self.parent.scroll / 5) * (self.parent.scX / self.parent.noteSpacing),
                        (height * self.parent.scY) + ((self.lane - 1) * (spacing * self.parent.scY)) + ((thickness * self.parent.scY) / 2)]
            
            #draw fill
            pygame.draw.circle(self.parent.screen,
                                colorPalette["notes"][self.part],
                                self.pos, self.radius,
                                0) #filled circle
            
            #draw outline
            pygame.draw.circle(self.parent.screen,
                                colorPalette["notes"][self.part + "out"] if not self.selected else colorPalette["notes"]["select"],
                                self.pos,
                                self.radius,
                                5) #outline
        
        def recieveClick(self, pos, button):
            
            #distance eq
            distance = math.sqrt((pos[0] - self.pos[0]) ** 2 + (pos[1] - self.pos[1]) ** 2)
            
            #activate if within note size
            
            if distance < self.radius:
                if button == "LEFT": #delete
                    return True #tell code that a note has been selected
                else:
                    self.selected = True #select
                    return True #tell code that a note has been selected
            
            else: self.selected = False #unselect
        
        def updateMeasure(self, value):
            
            #moves the note over one beat BASED ON INDIVIDUAL numerators. Fix later PLEASE
            
            if value == -1:
                if self.npos[1] == 1:
                    self.npos[0] -= 1
                    self.npos[1] = self.npos[2]
                else: self.npos[1] -= 1
            
            elif value == 1:
                if self.npos[1] == self.npos[2]:
                    self.npos[0] += 1
                    self.npos[1] = 1
                else: self.npos[1] += 1
            
            self.measure = (self.npos[0] + (self.npos[1] - 1) / self.npos[2]) * self.parent.meter_numerator
    
    class UtilBar:
        
        def __init__(self, parent):
            
            #setup valid data
            self.parent = parent
            
            #consts
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
                
                #highlight if mouse is ontop
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
            #check if any field is open
            for i in self.buttons:
                if i.active: return True
        
        class UtilButton:
            
            def __init__(self, parent, title, options, dims):
                
                #setup valid data
                self.parent = parent
                self.title = title
                self.options = options
                self.dims = dims
                
                #highlight globals
                self.isDark = False
                self.optionhighlighted = None
                self.active = False
                
                #globals
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
                elif function == "Export":
                    self.parent.parent.export()
                else: pass
    
    class PartSelect:
        
        def __init__(self, parent, part, index):
            self.parent = parent
            self.part = part
            self.index = index
            print(self.index)
        
        def update(self):
            width = 0.09
            x = width * self.index
            y = self.parent.utilBar.thickness
            x2 = x + width
            y2 = y + 0.03
            
            pygame.draw.rect(self.parent.screen, colorPalette["notes"][self.part], pm.drawAbsolute(x, y, x2, y2, self.parent.scX, self.parent.scY), 0)
            pygame.draw.rect(self.parent.screen, colorPalette["notes"][self.part + "out"], pm.drawAbsolute(x, y, x2, y2, self.parent.scX, self.parent.scY), 2)
        
        def recieveClick(self, pos, button):
            pass
    
    class Playback:
        
        def __init__(self, parent):
            self.parent = parent
        
        def update(self):
            
            pxsperbeat = self.parent.scX / self.parent.noteSpacing
            pos = pxsperbeat * 1
            
            ypospm = self.parent.utilBar.thickness
            ypos = pm.drawAbsolute(0, ypospm, 0, 0, self.parent.scX, self.parent.scY)[1]
            
            pygame.draw.rect(self.parent.screen, "#00FF99", [pos - 2.5, ypos, 5, 900], 0)

def main():
    
    tdebug = 0
    songPlayed = False
    
    pygame.init()
    pygame.mixer.init()
    
    #create editor object
    editor = Editor(path)
    
    clock = pygame.time.Clock()
    running = True
    editor.update()
    while running:
        
        if editor.status == "edit":
        
            #game runs at 60fps
            time_delta = clock.tick(60)/1000.0
            
            #event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                #updates scroll for editor
                if event.type == pygame.MOUSEWHEEL and editor.status == "edit":
                    
                    mods = pygame.key.get_mods()
                    
                    #hold alt to zoom
                    if mods & pygame.KMOD_ALT:
                        editor.noteSpacing -= event.y * 2
                        if editor.noteSpacing < 1: editor.noteSpacing = 1
                        if editor.noteSpacing > 9999: editor.noteSpacing = 9999
                        print(f"zoom: {editor.noteSpacing}")
                    
                    #hold shift to scroll faster
                    elif mods & pygame.KMOD_SHIFT:
                        editor.scroll += event.y * 10
                        if editor.scroll < -9999: editor.scroll = -9999
                        if editor.scroll > 0: editor.scroll = 0
                        print(f"scroll: {editor.noteSpacing}")
                    
                    #scroll normal speed if no key is held
                    else:
                        editor.scroll += event.y * 1
                        if editor.scroll < -9999: editor.scroll = -9999
                        if editor.scroll > 0: editor.scroll = 0
                        print(f"scroll: {editor.scroll}")
                
                #pass clicks to editor
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: editor.recieveClick(pygame.mouse.get_pos(), "LEFT")
                    elif event.button == 3: editor.recieveClick(pygame.mouse.get_pos(), "RIGHT")
                
                #pass keypresses to editor
                if event.type == pygame.KEYDOWN:
                    
                    #dev playback hotkey
                    if event.key == pygame.K_p: #run playback
                        pygame.mixer.music.load(path + r"\backing.mp3")
                        editor.status = "playback"
                        editor.scroll = 5
                    
                    else:
                        editor.recieveKey(event.key)
                
                #update dragend
                if event.type == pygame.MOUSEMOTION and editor.dragging: editor.dragEnd = event.pos
                
                #end drag
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3: #right mouse
                    if editor.dragging:
                        editor.dragging = False
                        editor.finishDragSelect()
            
            #step editor
            editor.update()
        
        elif editor.status == "playback":
            
            time_delta = clock.tick(30)/1000.0
            
            beatsecond = (1 / 60) * 10 #one beat per second
            beattime = (beatsecond * editor.bpm) / 60
            
            editor.scroll -= round(beattime, 4)
            tdebug += 1
            
            if tdebug * (1000/60) > editor.offset and not songPlayed:
                pygame.mixer.music.play()
                songPlayed = True
            
            editor.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

#code is meant to be run as a package in the menu script
if __name__ == "__main__":
    path = r"c:\Users\Benjaminsullivan\Downloads\ddrm3\testsongs\library_ruins"
    main()



"""
- HasWatchedCredits
- NumUniqueSongsCompleted
- NumUniqueSongsPerfected
- NumUniqueSongsPlayed
- NumUniqueSongsSurvived
- TotalPartsPerfected
- TotalSongsPlayed
- TotalTimesEaten
- TotalTimesSurvived
"""