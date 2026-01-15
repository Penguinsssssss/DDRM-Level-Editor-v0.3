#DDRM Editor 3.1

import tkinter as tk
root = tk.Tk()
root.withdraw()
screenX = root.winfo_screenwidth()
screenY = root.winfo_screenheight()
root.destroy()
from tkinter import filedialog
import pygame
import penguinsmodule as pm #type: ignore
import os
import json
import math
import copy
import shutil

path = None
GLOBAL_CONFIG_PATH = r"c:\Users\BenjaminSullivan\Downloads\\"

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
    "dry": {
        "shade1": "#ffe169", #lightest
        "shade2": "#edc531",
        "shade3": "#dbb42c",
        "shade4": "#c9a227",
        "shade5": "#b69121",
        "shade6": "#926c15",
        "shade7": "#805b10",
        "shade8": "#76520e", #darkest
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
        "aux-percussion": "#e9852d",
        "aux-percussionout": "#9c500e",
        "signature": "#fed141",
        "signatureout": "#ad8916",
        "harmony": "#1ec88d",
        "harmonyout": "#038155",
        "melody": "#287ce7",
        "melodyout": "#0b4b9c",
        "bass": "#6b3ad8",
        "bassout": "#3c188c",
        "counter": "#d83cb4",
        "counterout": "#8c1972",
        "select": "#999999", #temp, possibly change based on note in the future
        }
}

class Editor:
    
    def __init__(self, levelPath):
        
        #setup screen
        self.scX = screenX * 0.75
        self.scY = screenY * 0.75
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
        self.unlock_condition = loaded_data["unlockType"]
        self.unlock_value = loaded_data["unlockRequirement"]
        self.chart = loaded_data["chart"]
        
        #status
        self.status = "edit"
        
        #how far the user has scrolled in the chart
        self.scroll = 0
        
        #zoom; how many beats are fit on the screen at a time
        self.noteSpacing = 12
        
        #allows placing notes in differing time signatures
        self.meter_numerator = self.signature[0]
        self.meter_denominator = self.signature[1]
        self.view_meter_num = self.meter_numerator
        self.view_meter_den = self.meter_denominator
        
        #create utilbar
        self.utilBar = self.UtilBar(self)
        
        #create playback object
        self.playback = self.Playback(self)
        
        #playback
        self.playing = False
        self.playPosMs = 0
        self.msPerBeat = (60000 / self.bpm)
        self.songLengthMs = 0
        try:
            pygame.mixer.music.load(os.path.join(os.path.dirname(self.path), "backing.ogg"))
            self.songLengthMs = pygame.mixer.Sound(os.path.join(os.path.dirname(self.path), "backing.ogg")).get_length() * 1000
        except:
            print("no audio file found")
        
        #store note data by part
        self.notes_by_part = {}
        for part_data in self.chart:
            part_name = part_data["part"]
            self.notes_by_part[part_name] = [
                self.Note(self, note_data, part_name)
                for note_data in part_data["notes"]
            ]
        
        #load initial part
        self.inFocusPart = self.chart[0]
        self.notes = self.notes_by_part[self.inFocusPart["part"]]
        
        #drag-select system
        self.dragging = False
        self.dragStart = None
        self.dragEnd = None
        
        #make partSelects
        self.partSelects = []
        for i in self.chart:
            self.partSelects.append(self.PartSelect(self, i["part"], len(self.partSelects)))
        
        #undo and redo history are called "stacks"
        self.undo_stack = []
        self.redo_stack = []
        
        #save starting to state to undo
        self.push_undo()
        
        #copy paste
        self.clipboard = []
        
        #check if a popup is open
        self.popup = None
        
        #output levels to a folder
        self.output_path = r"C:\users\benjaminsullivan\downloads"
    
    #drawing
    def update(self):
        
        #fill screen
        self.screen.fill(colorPalette[theme]["shade6"])
        self.drawBackdrop()
        
        #draw screen elements
        self.drawChart()
        for i in self.partSelects: i.update()
        self.utilBar.update()
        
        #draw dragselect
        self.drawDragSelect()
        
        #update playback
        self.playback.update()
        
        #update popup
        if self.popup:
            self.popup.update()
        
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
            numnodes = int(self.scX / pxspernode) + 2000 #add buffer (temp debug)
            
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
                size = 7 if k % self.view_meter_num == 0 else 3
                
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
        
        beatxlength = 1 / self.noteSpacing
        beats_per_measure = self.view_meter_num
        
        for i in range(self.noteSpacing):
            
            #convert beat index to measure index
            measure_index = i // beats_per_measure
            
            #horizontal position
            scrolloffset = (self.scroll / (5 * self.noteSpacing)) % 1
            start = (i * beatxlength + scrolloffset) % 1
            end   = start + beatxlength
            
            #color every other measure
            if measure_index % 2 == 0: pygame.draw.rect(self.screen, colorPalette[theme]["shade6"], pm.drawAbsolute(start, 0, end, 1, self.scX, self.scY), 0)
    
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
    
    #input handling
    def recieveClick(self, pos, button):
        
        #activated upon any form of mouse input from the user
        #sends signal to each screen element
        
        #only allow users to modify chart during editing
        for i in self.partSelects: i.recieveClick(pos, button)
        
        if self.status == "edit":
            
            #deleting
            if button == "LEFT":
                
                wasActive = self.utilBar.checkActive()
                
                noteClicked = False
                for i in self.notes:
                    if i.recieveClick(pos, button):
                        self.push_undo()
                        self.notes.remove(i)
                        noteClicked = True
                if self.utilBar.recieveClick(pos, button):
                    return
                elif not noteClicked and not wasActive:
                    closest = self.findClosest(pos, self.nodes)
                    if closest: #ensure that note is not too far away
                        measure = [(closest[0] - closest[0] % self.view_meter_num) / self.view_meter_num, #measure
                                    closest[0] % self.view_meter_num + 1, #beat
                                    self.view_meter_num] #numerator
                        self.push_undo()
                        self.notes.append(self.Note(self, [measure, closest[1] + 1, 0], self.inFocusPart["part"]))
            
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
                
                for i in self.partSelects:
                    if i.recieveClick(pos, button): self.dragging = False
    
    def recieveKey(self, key):
        
        #delete selection
        if key == pygame.K_DELETE or key == pygame.K_BACKSPACE:
            self.push_undo()
            for i in reversed(self.notes):
                if i.selected: self.notes.remove(i)
        
        #move selection up
        if key == pygame.K_w or key == pygame.K_UP:
            self.push_undo()
            for i in self.notes:
                if i.selected: i.lane = max(i.lane - 1, 1)
        
        #move selection down
        if key == pygame.K_s or key == pygame.K_DOWN:
            self.push_undo()
            for i in self.notes:
                if i.selected: i.lane = min(i.lane + 1, 6) #NOTE HARDCODED TO 6, FIX LATER
        
        #move selection left
        if key == pygame.K_a or key == pygame.K_LEFT:
            self.push_undo()
            for i in self.notes:
                if i.selected:
                    i.updateMeasure(-1)
        
        #move selection right
        if key == pygame.K_d or key == pygame.K_RIGHT:
            self.push_undo()
            for i in self.notes:
                if i.selected:
                    i.updateMeasure(1)
    
    #match
    def findClosest(self, pos, nodes): #taken from online source
            closest_point = None
            min_distance = float('inf')  # Initialize with a very large distance
            max_range = 30
            
            for point in nodes:
                # Calculate Euclidean distance
                nodepos = [(point[0] + self.scroll / 5) * (self.scX / self.noteSpacing),
                           pm.drawAbsolute(0, (self.height + (point[1] * self.spacing)) + (self.thickness / 2), 0, 0, self.scX, self.scY)[1]]
                distance = math.sqrt((pos[0] - nodepos[0])**2 + (pos[1] - nodepos[1])**2)
                
                if distance < min_distance:
                    min_distance = distance
                    closest_point = point
            
            if min_distance < max_range:
                return closest_point
            else: return None
    
    #dev
    def devdebug(self):
        #dev
        for i in self.notes: print(i.npos)
    
    def writeNotes(self):
        #dev
        noteslist = []
        for i in self.notes: noteslist.append([i.npos, i.lane, i.pitch])
        return noteslist
    
    #user functions
    def export(self):
        
        #initialize to a very large number (will add logic later)
        duration = 0
        for i in self.chart:
            for j in i["notes"]:
                duration = max(round(((j[0][0] + (j[0][1] - 1) / j[0][2]) * self.meter_numerator * (60000 / self.bpm)) - self.offset), duration)
        
        #guide is jackboxes system for keeping track of beats (stored in ms)
        guide = []
        
        #create guide
        i = 0
        while i <= duration - (60000 / self.bpm) * 4:
            
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
            "preferredAssignments": [], #code below sets this
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
            
            inputs.sort(key=lambda x: x["start"])
            
            data["beatmaps"].append(
                {
            "slug": i["part"], #melody, drums, etc
            "type": "Discrete", #no idea what this does but things break without it
            "category": i["part"].capitalize() if i["part"] != "aux-percussion" else "AuxPercussion", #Melody, Drums, etc
            "difficulty": i["difficulty"], #1-5
            "instruments": i["instruments"], #valid instruments
            "instrumentRequirements": [i["part"].capitalize()], #melody, drums, etc, no idea what this does either...
            "events": [], #seemingly never used? initializing blank seems to work out just fine
            "inputs": inputs, #all notes
            "laneCount": i["lanes"] #1-6
            }
                )
        
        preferred = []
        seen = set()
        
        for part in self.chart:
            part_slug = part["part"]
            
            instruments = part.get("instruments") or ["rave-synth"]
            
            for instr in instruments:
                key = (part_slug, instr)
                if key in seen:
                    continue
                seen.add(key)
                preferred.append([part_slug, instr])
                
            data["preferredAssignments"] = preferred
                
        out_dir = os.path.join(self.output_path, self.name)
        
        #delete existing folder
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)  #nukes folder + contents
        os.makedirs(out_dir, exist_ok=True)
        
        #write config.json
        config_path = os.path.join(out_dir, "config.json")
        with open(config_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=2)
        
        #language files to generate
        languages = ["de", "en", "es", "es-XL", "fr", "it", "pt_BR"]
        title_data = {
            "TITLE": self.name
        }
        for lang in languages:
            lang_path = os.path.join(out_dir, f"{lang}.json")
            with open(lang_path, "w", encoding="utf-8") as f:
                json.dump(title_data, f, indent=2, ensure_ascii=False)
        
        #copy backing.ogg into the folder
        src_path = os.path.join(path, "backing.ogg")
        dst_path = os.path.join(out_dir, "backing.ogg")
        
        try:
            shutil.copy2(src_path, dst_path)
            print(f"Copied '{src_path}' -> '{dst_path}'")
        except FileNotFoundError:
            print(f"Error: '{src_path}' not found.")
        except PermissionError:
            print("Error: Permission denied. Is the destination file open in another program?")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def snapshot(self):
        
        #store a snaphop of the notes
        
        data = []
        
        for i in self.notes:
            data.append({
                "npos": copy.deepcopy(i.npos),
                "lane": i.lane,
                "pitch": i.pitch,
                "part": i.part
            })
        
        return data
    
    def restore_snapshot(self, data):
        
        #set notes to a previous snapshot
        self.notes = []
        
        for i in data:
            note = self.Note(self, [i["npos"], i["lane"], i["pitch"]], i["part"])
            self.notes.append(note)
    
    def push_undo(self):
        
        self.undo_stack.append(self.snapshot())
        
        if len(self.undo_stack) > 200: #cap memory at 200
            self.undo_stack.pop(0)
            
        self.redo_stack.clear()
    
    def undo(self):
        
        if len(self.undo_stack) <= 1:
            return #nothing to undo
        
        #retreve last state
        state = self.undo_stack.pop()
        
        #set redo stack to prior state
        self.redo_stack.append(state)
        
        #set current state to last snapshot
        self.restore_snapshot(self.undo_stack[-1])
    
    def redo(self):
        if not self.redo_stack:
            return #nothing to redo
        
        #grab snapshot from stack
        state = self.redo_stack.pop()
        
        #allow user to undo a redo
        self.undo_stack.append(state)
        
        #load snapshot
        self.restore_snapshot(state)
    
    def copy(self):
        selected = [i for i in self.notes if i.selected]
        if len(selected) == 0:
            return #nothing to copy
        
        beats = self.meter_numerator
        
        #convert notes to absolute beat indices
        abs_beats = []
        for i in selected:
            absbeat = i.npos[0] * beats + (i.npos[1] - 1)
            abs_beats.append(absbeat)
            
        min_beat = min(abs_beats)
        min_lane = min(i.lane for i in selected)
        
        #empty clipboard
        self.clipboard = []
        
        #store notes in clipboard dict
        for i in selected:
            absbeat = i.npos[0] * beats + (i.npos[1] - 1)
            self.clipboard.append({
                "beat": absbeat - min_beat, #relative beat offset
                "lane": i.lane - min_lane,
                "pitch": i.pitch,
                "part": i.part,
                "numerator": i.npos[2]
            })
    
    def paste(self):
        if not self.clipboard:
            return #nothing to paste
        
        #store pre-paste state
        self.push_undo()
        
        #find leftmost node
        left_node = int(-self.scroll / 5)
        
        #unselect selected notes
        for i in self.notes: i.selected = False
        
        for i in self.clipboard:
            
            new_beat = left_node + i["beat"]
            new_lane = 1 + i["lane"]
            
            #convert absolute beat index back to npos
            measureidx = new_beat // i["numerator"]
            beat = (new_beat % i["numerator"]) + 1
            newnpos = [measureidx, beat, i["numerator"]]
            
            #append note
            note = self.Note(self, [newnpos, new_lane, i["pitch"]], i["part"])
            note.selected = True
            self.notes.append(note)
    
    def getPlaybackStartBeat(self):
        return -self.scroll / 5
    
    def startPlayback(self):
        #set mode to playback
        self.status = "playback"
        
        #get starting beat
        startBeat = self.getPlaybackStartBeat()
        
        #convert beats to milliseconds
        msPerBeat = (60000 / self.bpm)
        startMs = startBeat * msPerBeat
        
        #start audio from beat
        pygame.mixer.music.play(start= startMs / 1000.0)
        
        #playback logic
        self.playback.startBeat = startBeat
        self.playback.startMs = startMs
        self.playback.elapsed = 0
        
        #dev
        print(f"Playback starting at beat {startBeat}, ms={startMs}")
    
    def openSongInfoPopup(self):
        
        conditions = [
            "----",
            "HasWatchedCredits",
            "NumUniqueSongsCompleted",
            "NumUniqueSongsPerfected",
            "NumUniqueSongsPlayed",
            "NumUniqueSongsSurvived",
            "TotalPartsPerfected",
            "TotalSongsPlayed",
            "TotalTimesEaten",
            "TotalTimesSurvived"
                ]
        
        fields = {
            "Song Name": self.name,
            "Song Author": self.songauthor,
            "BPM": str(self.bpm),
            "Offset": str(self.offset),
            "Unlock Condition": "----",
            "Unlock Value": str(getattr(self, "unlock_value", self.unlock_value))
        }
        
        def apply_changes(values):
            self.name = values["Song Name"]
            self.songauthor = values["Song Author"]
            self.bpm = int(values["BPM"])
            self.offset = float(values["Offset"])
            self.unlock_condition = values["Unlock Condition"]
            self.unlock_value = int(values["Unlock Value"])
            
            #update JSON
            with open(self.path, "r") as f:
                data = json.load(f)
            
            data["name"] = self.name
            data["songauthor"] = self.songauthor
            data["bpm"] = self.bpm
            data["offset"] = self.offset
            data["unlockType"] = self.unlock_condition
            data["unlockRequirement"] = self.unlock_value
            
            with open(self.path, "w") as f:
                json.dump(data, f, indent=4)
            
            print("saved changes")
        
        self.popup = self.PopupWindow(self, "Song Info", fields, apply_changes)
        self.popup.addDropdown("Unlock Condition", conditions)
    
    def changeSongAudio(self):
        #select audio file
        
        temp_root = tk.Tk()
        temp_root.withdraw()
        file_path = filedialog.askopenfilename(
            title="select new backing audio",
            filetypes=[
                ("Audio files", "*.mp3 *.ogg *.wav"),
                ("All files", "*.*")
            ]
        )
        temp_root.deiconify()
        temp_root.destroy()
        
        if not file_path:
            print("no audio selected")
            return
        
        #extension
        ext = os.path.splitext(file_path)[1]
        
        #destination path
        song_folder = os.path.dirname(self.path)
        new_path = os.path.join(song_folder, "backing" + ext)
        
        try:
            #delete prev file
            
            for f in os.listdir(song_folder):
                if f.startswith("backing."):
                    os.remove(os.path.join(song_folder, f))
            
            #copy new file
            shutil.copy(file_path, new_path)
            
            #save new audio path to JSON
            with open(self.path, "r") as f:
                data = json.load(f)
                
            data["audio"] = "backing" + ext
            
            with open(self.path, "w") as f:
                json.dump(data, f, indent=4)
            
            print(f"audio replaced successfully {new_path}")
            
        except Exception as e:
            print("failed to replace audio:", e) #lawd help me
    
    def openThemeWindow(self):
        
        def apply_theme(selected_theme):
            global theme
            theme = selected_theme
            print("Switched theme to:", theme)
            
        self.popup = self.PopupWindow(self, "Select Theme", fields=None, on_save=apply_theme, is_theme_window=True
        )
    
    def openViewingMeterPopup(self):
        fields = {
            "Numerator": str(self.view_meter_num),
            "Denominator": str(self.view_meter_den)
        }
        
        #upon saving
        def apply(values):
            
            #prevent user foolishness
            try:
                num = int(values["Numerator"])
                den = int(values["Denominator"])
                if num < 1 or den < 1:
                    raise ValueError
                self.scroll = (self.scroll - self.noteSpacing) * (num / self.view_meter_num) #update scroll to match where the users was looking
                self.view_meter_num = num
                self.view_meter_den = den
            except:
                print("ingvalid")
            
        #create popup
        self.popup = self.PopupWindow(parent=self, title="Change Viewing Meter", fields=fields, on_save=apply, is_theme_window=False
        )
    
    def openConfigMenu(self):
        fields = {
            "Output Path": self.output_path
        }
        
        def apply_changes(values):
            
            path = values["Output Path"]
            if os.path.isdir(path):
                self.output_path = path
            else: print("invalid path")
            
            self.output_path = values["Output Path"]
            
            #ensure config folder exists
            os.makedirs(os.path.dirname(GLOBAL_CONFIG_PATH), exist_ok=True)
            
            #load existing config
            if os.path.exists(GLOBAL_CONFIG_PATH):
                with open(GLOBAL_CONFIG_PATH, "r", encoding="utf-8") as f:
                    try:
                        config = json.load(f)
                    except json.JSONDecodeError:
                        config = {}
            else:
                config = {}
            
            config["output_path"] = self.output_path
            with open(GLOBAL_CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
                
            print(f"Saved output path to {GLOBAL_CONFIG_PATH}")
        
        self.popup = self.PopupWindow(self, "Change Output Location", fields, apply_changes)
    
    def format_notes(self, notes):
        result = []
        for i in notes:
            result.append([
                i.npos.copy(),
                i.lane,
                i.pitch
            ])
        return result
    
    def togglePlayback(self):
        
        if not self.playing:
            
            #start playback
            self.playing = True
            
            #compute leftmost beat
            leftNode = -self.scroll / 5
            
            #convert to real beat
            leftMusicalBeat = leftNode * (self.meter_numerator / self.view_meter_num)
            
            #convert to milliseconds
            startMs = leftMusicalBeat * self.msPerBeat
            
            #begin playback from that position
            self.playPosMs = startMs + self.offset
            try:
                pygame.mixer.music.play(start=startMs / 1000.0)
            except:
                print("could not play audio from offset")
            
        else:
            #stop playback
            self.playing = False
            pygame.mixer.music.stop()
    
    def openAddPartWindow(self):
        
        fields = {
            "Part Type": "----"
        }
        
        def apply(values):
            print("Selected new part:", values["Part Type"])
            self.addPartToJson(values["Part Type"])
        
        remainingparts = ["drums", "perc", "signature", "harmony", "melody", "bass", "counter"]
        for i in self.chart:
            if i["part"] in remainingparts: remainingparts.remove(i["part"])
        
        self.popup = self.PopupWindow(self, "Add Part", fields, apply)
        self.popup.addDropdown("Part Type", remainingparts)
    
    def addPartToJson(self, part_name: str):
        
        part_name = part_name.strip().lower()
        if not part_name:
            print("invalid part name")
            return False
        
        #load json
        with open(self.path, "r") as f:
            data = json.load(f)
        
        #create new part entry
        new_part = {
            "part": part_name,
            "instruments": ["foo", "bar"],
            "difficulty": 1,
            "lanes": 6,
            "notes": []
        }
        
        data["chart"].append(new_part)
        
        #save json
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)
            
        #update editor
        self.chart = data["chart"]
        
        #add empty note list for this part
        if not hasattr(self, "notes_by_part"):
            self.notes_by_part = {}
        self.notes_by_part[part_name] = []
        
        #add a new PartSelect button
        self.partSelects.append(self.PartSelect(self, part_name, len(self.partSelects)))
        
        print("added new part:", part_name)
        return True
    
    def openAddInstrumentWindow(self, part_index: int):
        #safety
        if part_index < 0 or part_index >= len(self.chart):
            print("invalid part index")
            return
        
        part_name = self.chart[part_index]["part"]
        
        instrument_choices = ["(none)", 'agnes-the-dog', 'agnes-the-dog-howls', 'alarm-clock', 'arp-synth', 'baby-sloppy-horn', 'banjo', 'bari-sax', 'bass-flute', 'bassoon', 'beatbox', 'bitdrums', 'bottlecaps', 'burpin-conga', 'burpin-drums', 'burps-melody', 'cajon', 'cannon', 'car-alarm', 'castanets', 'casual-saxophone', 'caxixi', 'cello-bowed', 'cello-plucked', 'cheeks-melody', 'cheeks-percussion', 'clarinet', 'constant-scream', 'continuous-agnes', 'continuous-burp', 'continuous-constant-screaming', 'continuous-doug', 'continuous-flute', 'continuous-gargles', 'continuous-jan', 'continuous-kazoo', 'continuous-lip-flipper', 'continuous-mario', 'continuous-natures-bugle', 'continuous-shredding-guitar', 'continuous-slide-whistle', 'continuous-susan', 'continuous-taz', 'contrabass-clarinet', 'contrabass-flute', 'contrabassoon', 'cow-bell', 'didgeridoo', 'dinner-bell', 'dj-drums', 'double-bass-bowed', 'double-bass-plucked', 'doug', 'drum-set-clean', 'eb-soprano-clarinet', 'electric-bass', 'euphonium', 'extra-sloppy-horn', 'extra-tall-bongos', 'fast-food-cup', 'field-drums', 'flugelhorn', 'flute', 'french-horn-redo', 'gargles', 'goat', 'gong', 'grandmas-piano', 'guiro', 'guitar-acoustic-chords', 'guitar-acoustic-notes', 'guitar-electric-chords', 'guitar-electric-noamp', 'guitar-metal-chords', 'guitar-metal-notes', 'guitar-rock-chords', 'guitar-rock-notes', 'h0-ly-crap', 'husky-clarinet', 'jaw-harp', 'jazz-drums', 'kazoo', 'kettle-drums', 'kung-fu-drums', 'lil-ukulele-friend-redo', 'lip-flipper', 'little-congas', 'marching-bass-drum', 'marching-drums', 'marimba', 'mario', 'mommy-sax', 'mosquito', 'music-box', 'oboe', 'ocarina', 'piccolo', 'piccolo-trumpet', 'pieces-of-wood', 'pluck-synth', 'plucky-violin', 'plucky-violins-cousin', 'pots-n-pans', 'rain-stick', 'rave-synth', 'rave-synth-0', 'rhodes', 'robot-synth', 'shaky-shaker', 'shy-flute', 'sloppy-horn-sampler', 'sloppy-horn-senior', 'snap-clap-stomp', 'snare-drum', 'squeeze-box', 'tall-bongos', 'tamborine', 'taz-the-cat', 'the-beef', 'the-beef-0', 'tootsaphone', 'trumpet', 'tuba', 'tutorial', 'uncle-sax', 'vibes', 'vibraslap', 'violin', 'violin-0', 'violins-cousin', 'voice-alto', 'voice-soprano', 'weird-oboe', 'whistle', 'wind-chimes', 'wobble-bass', 'wobble-bass-0', 'wood-block']
        
        #get existing instruments from chart
        existing_instruments = self.chart[part_index].get("instruments", [])
        if not isinstance(existing_instruments, list):
            existing_instruments = []
            
        #fields
        fields = {
            "Add Instrument": instrument_choices[0],
            "Remove Instrument": "(none)"
        }
        
        def apply(values):
            add_inst = values["Add Instrument"].strip()
            remove_inst = values["Remove Instrument"].strip()
            
            #load chart.json
            with open(self.path, "r") as f:
                data = json.load(f)
                
            chart_list = data.get("chart", [])
            if part_index >= len(chart_list):
                print("chart index mismatch")
                return
            
            part_obj = chart_list[part_index]
            
            #ensure instruments list exists
            if "instruments" not in part_obj or not isinstance(part_obj["instruments"], list):
                part_obj["instruments"] = []
                
            changed = False
            
            #add
            if add_inst and add_inst != "(none)":
                if add_inst not in part_obj["instruments"]:
                    part_obj["instruments"].append(add_inst)
                    changed = True
                else:
                    print("instrument already present:", add_inst)
                    
            #remove
            if remove_inst and remove_inst != "(none)":
                if remove_inst in part_obj["instruments"]:
                    part_obj["instruments"].remove(remove_inst)
                    changed = True
                else:
                    print("instrument not found on part:", remove_inst)
                    
            if not changed:
                print("no changes made")
                return
            
            #write
            with open(self.path, "w") as f:
                json.dump(data, f, indent=4)
                
            #update chart
            self.chart = data["chart"]
            
            #refresh inFocusPart
            if self.inFocusPart and self.inFocusPart.get("part") == part_name:
                self.inFocusPart = self.chart[part_index]
                
            print(f"updated instruments for '{part_name}':", self.chart[part_index].get("instruments", []))
            
        #open popup
        self.popup = self.PopupWindow(self, f"Edit Instruments ({part_name})", fields, apply)
        
        #attach dropdowns
        self.popup.addDropdown("Add Instrument", instrument_choices)
        
        #removable list
        remove_choices = ["(none)"] + existing_instruments
        self.popup.addDropdown("Remove Instrument", remove_choices)
    
    class Note:
        
        def __init__(self, parent, data, part):
            
            #setup valid data
            self.parent = parent
            self.npos = data[0]
            self.measure = (self.npos[0] + (self.npos[1] - 1) / self.npos[2]) * self.parent.view_meter_num
            self.lane = data[1]
            self.pitch = data[2]
            self.part = part
            
            #change color and behavior if selected
            self.selected = False
            
            self.pos = [0, 0]
            self.radius = 20
        
        def update(self):
            
            self.measure = (self.npos[0] + (self.npos[1] - 1) / self.npos[2]) * self.parent.view_meter_num
            
            #consts
            height = 0.25
            spacing = 0.08 #per beat
            thickness = 0.005
            
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
            buttonLen = 0.1
            
            #dummy buttons
            self.buttons = []
            self.buttons.append(self.UtilButton(self, "File", ["Open", "Save", "Export", "Exit"], [0, 0, buttonLen, self.thickness]))
            self.buttons.append(self.UtilButton(self, "Edit", ["Edit Song Info", "Change Audio", "Add Part"], [buttonLen, 0, buttonLen * 2, self.thickness]))
            self.buttons.append(self.UtilButton(self, "Tools", ["Undo", "Redo", "Edit Meter"], [buttonLen * 2, 0, buttonLen * 3, self.thickness]))
            self.buttons.append(self.UtilButton(self, "Play", ["Play"], [buttonLen * 3, 0, buttonLen * 4, self.thickness]))
            self.buttons.append(self.UtilButton(self, "Config", ["Change Output Path", "Change Theme"], [buttonLen * 4, 0, buttonLen * 5, self.thickness]))
        
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
                
                #dev
                print(f"function: {function}")
                
                if function == "New": print("new")
                elif function == "Open":
                    
                    #user selects a level folder
                    root=tk.Tk()
                    root.withdraw()
                    file_path = filedialog.askdirectory(
                        title="Select a level folder", initialdir="/"
                    )
                    root.destroy()
                    
                    #check if folder is valid
                    chartpath = file_path + "\\chart.json"
                    if os.path.isfile(chartpath):
                        
                        #change path
                        global path
                        path = file_path
                        
                        #open a new pygame window with updated path
                        pygame.quit()
                        main()
                    else:
                        print("invadild level data")
                    
                elif function == "Save":
                    with open(self.parent.parent.path, 'r') as file:
                        data = json.load(file)
                        
                    for part_data in data["chart"]:
                        part_name = part_data["part"]
                        notes_for_part = self.parent.parent.notes_by_part[part_name]
                        part_data["notes"] = self.parent.parent.format_notes(notes_for_part)
                        
                    with open(self.parent.parent.path, 'w') as file:
                        json.dump(data, file, indent=4)
                        
                    print("file saved !")
                    
                elif function == "Export": self.parent.parent.export()
                elif function == "Edit Song Info": self.parent.parent.openSongInfoPopup()
                elif function == "Change Audio": self.parent.parent.changeSongAudio()
                elif function == "Undo": self.parent.parent.undo()
                elif function == "Redo": self.parent.parent.redo()
                elif function == "Play": self.parent.parent.togglePlayback()
                elif function == "Change Theme" : self.parent.parent.openThemeWindow()
                elif function == "Edit Meter" : self.parent.parent.openViewingMeterPopup()
                elif function == "Change Output Path": self.parent.parent.openConfigMenu()
                elif function == "Add Part": self.parent.parent.openAddPartWindow()
                elif function == "Exit": pygame.quit()
                else: print("unknown function")
    
    class PartSelect:
        
        def __init__(self, parent, part, index):
            
            self.parent = parent
            self.part = part
            self.index = index
            
            self.dark = False
        
        def update(self):
            
            width = 1/7
            height = 0.03
            x = width * self.index
            y = self.parent.utilBar.thickness
            x2 = x + width
            y2 = y + height
            
            self.pos = [x * self.parent.scX, y * self.parent.scY, x2 * self.parent.scX, y2 * self.parent.scY]
            
            self.darken(pygame.mouse.get_pos())
            
            pygame.draw.rect(self.parent.screen, colorPalette["notes"][self.part] if not self.dark else colorPalette["notes"][self.part + "out"], pm.drawAbsolute(x, y, x2, y2, self.parent.scX, self.parent.scY), 0)
            pygame.draw.rect(self.parent.screen, colorPalette["notes"][self.part + "out"] if not self.dark else colorPalette["notes"]["select"], pm.drawAbsolute(x, y, x2, y2, self.parent.scX, self.parent.scY), 2)
        
        def recieveClick(self, pos, button):
            
            if self.pos[0] < pos[0] < self.pos[2] and self.pos[1] < pos[1] < self.pos[3]:
                
                if button == "RIGHT":
                    #dont open if another popup already exists
                    if self.parent.popup is None:
                        self.parent.openAddInstrumentWindow(self.index)
                    return True
                
                else:
                    self.parent.inFocusPart = self.parent.chart[self.index]
                    part_name = self.parent.inFocusPart["part"]
                    self.parent.notes = self.parent.notes_by_part[part_name]
                    
                    print(self.part)
        
        def darken(self, pos):
            
            if self.pos[0] < pos[0] < self.pos[2] and self.pos[1] < pos[1] < self.pos[3]:
                
                self.dark = True
            
            else: self.dark = False
    
    class Playback:
        def __init__(self, parent):
            self.parent = parent
            
        def update(self):
            if not self.parent.playing:
                return
            
            musicalBeat = self.parent.playPosMs / self.parent.msPerBeat
            nodeIndex = musicalBeat * (self.parent.view_meter_num / self.parent.meter_numerator)
            x = (nodeIndex + self.parent.scroll / 5) * (self.parent.scX / self.parent.noteSpacing)
            
            #draw bar (HARDCODED)
            pygame.draw.rect(self.parent.screen, (0, 255, 0), (x, 0, 4, self.parent.scY))
    
    class PopupWindow:
        
        def __init__(self, parent, title, fields, on_save, is_theme_window=False):
            
            self.parent = parent
            self.title = title
            self.fields = dict(fields) if fields is not None else {} #clone
            self.on_save = on_save
            
            self.is_theme_window = is_theme_window
            self.selected_theme = None
            
            self.active = True
            
            #popup size
            self.w = parent.scX * 0.6 if self.is_theme_window else parent.scX * 0.6
            self.h = parent.scY * 0.7 if self.is_theme_window else parent.scY * 0.7
            if title == "Change Output Location":
                self.w = parent.scX * 0.6
                self.h = parent.scY * 0.5
            self.x = (parent.scX - self.w) // 3
            self.y = (parent.scY - self.h) // 3
            
            self.focus = None
            
            #font
            self.font = pygame.font.SysFont("C:/Windows/Fonts/Ebrima.ttf", 20)
            self.title_font = pygame.font.SysFont("C:/Windows/Fonts/Ebrima.ttf", 28, bold=True)
            
            #dropdown support
            self.dropdowns = {}
            self.openDropdown = None
            self.dropdownHover = None
            self.dropdownScroll = 0
            self.dropdownMaxVisible = 5
            self.dropdownItemHeight = 40
        
        #text entry
        def handleTextInput(self, char):
            if self.focus is None:
                return #nowhere to type
            self.fields[self.focus] += char
        
        def handleBackspace(self):
            if self.focus is None:
                return #nowhere to backspace
            self.fields[self.focus] = self.fields[self.focus][:-1] #we love string slicing
        
        def addDropdown(self, fieldName, options):
            self.dropdowns[fieldName] = options
        
        #click entry
        def click(self, pos):
            
            #check if clicking a dropdown field
            for fieldName, opts in self.dropdowns.items():
                
                offset = 40
                j = list(self.fields.keys()).index(fieldName)
                rect = pygame.Rect(self.x + 220, self.y + offset + j * 40, 300, 40)
                
                #if click on closed dropdown, close dropdown
                if rect.collidepoint(pos):
                    self.openDropdown = fieldName
                    return
                
            #check if clicking inside an open dropdown
            if self.openDropdown:
                fieldName = self.openDropdown
                opts = self.dropdowns[fieldName]
                
                offset = 40
                j = list(self.fields.keys()).index(fieldName)
                base_rect = pygame.Rect(self.x + 220, self.y + offset + j * 40, 300, 40)
                
                #determine visible dropdown box
                opts = self.dropdowns[self.openDropdown]
                visible = opts[self.dropdownScroll : self.dropdownScroll + self.dropdownMaxVisible]
                
                #dropdown rectangle
                drop_rect = pygame.Rect(base_rect.x, base_rect.y + 40,
                                        300, self.dropdownItemHeight * len(visible))
                
                if drop_rect.collidepoint(pos):
                    relY = pos[1] - drop_rect.y
                    index = relY // self.dropdownItemHeight
                    selectedOption = visible[index]
                    
                    #apply selected value
                    self.fields[self.openDropdown] = selectedOption
                    self.openDropdown = None
                    return
                
                #click elsewhere closes dropdown
                self.openDropdown = None
            
            if self.is_theme_window:
                hit = self.handleThemeClick(pos)
                if hit: #detect if theme was clicked
                    self.selected_theme = hit
                    return
                
                #save/cancel buttons (HARDCODED)
                save_rect = pygame.Rect(self.x + 80, self.y + self.h - 80, 150, 50)
                cancel_rect = pygame.Rect(self.x + 280, self.y + self.h - 80, 150, 50)
                
                #if clicked on save_rect
                if save_rect.collidepoint(pos):
                    if self.selected_theme is not None:
                        self.on_save(self.selected_theme)
                    self.parent.popup = None
                    self.active = False
                
                #if clicked on cancel_rect
                elif cancel_rect.collidepoint(pos):
                    self.parent.popup = None
                    self.active = False
                
                return
            
            else:
                
                offset = 40 #debug
                j = 0
                
                #check textboxes
                for i in self.fields:
                    rect = pygame.Rect(self.x + 220, self.y + offset + j * 40, 300, 40)
                    if rect.collidepoint(pos):
                        self.focus = i
                        return
                    j += 1
                
                #buttons
                save_rect = pygame.Rect(self.x + 80, self.y + self.h - 80, 150, 50)
                cancel_rect = pygame.Rect(self.x + 280, self.y + self.h - 80, 150, 50)
                
                #save_rect
                if save_rect.collidepoint(pos):
                    self.on_save(self.fields)
                    self.parent.popup = None
                    self.active = False
                
                #cancel_rect
                elif cancel_rect.collidepoint(pos):
                    self.parent.popup = None
                    self.active = False
        
        def handleThemeClick(self, pos):
            
            themes = list(colorPalette.keys())
            
            #remove non-themes
            if "other" in themes:
                themes.remove("other")
            if "notes" in themes:
                themes.remove("notes")
            
            #amount of themes displayed per collumn
            cols = 3
            
            #(HARDCODED)
            tile_w = 150
            tile_h = 100
            margin = 20
            
            #(HARDCODED)
            grid_x = self.x + 40
            grid_y = self.y + 80
            
            for i, theme_name in enumerate(themes):
                
                #determine the location in the grid
                col = i % cols
                row = i // cols
                
                #create a rect for each theme
                rect = pygame.Rect(
                    grid_x + col * (tile_w + margin),
                    grid_y + row * (tile_h + margin),
                    tile_w,
                    tile_h
                )
                
                #check if a theme was clicked
                if rect.collidepoint(pos):
                    return theme_name
                
            return None
        
        def handleDropdownScroll(self, event):
            if not self.openDropdown:
                return
            
            #number of items
            opts = self.dropdowns[self.openDropdown]
            total = len(opts)
            
            max_scroll = max(0, total - self.dropdownMaxVisible)
            
            if event.type == pygame.MOUSEWHEEL:
                self.dropdownScroll -= event.y
                if self.dropdownScroll < 0:
                    self.dropdownScroll = 0
                if self.dropdownScroll > max_scroll:
                    self.dropdownScroll = max_scroll
        
        #drawing
        def update(self):
            
            #dim background
            dim = pygame.Surface((self.parent.scX, self.parent.scY), pygame.SRCALPHA)
            dim.fill((0, 0, 0, 180))
            self.parent.screen.blit(dim, (0, 0))
            
            #popup box
            pygame.draw.rect(self.parent.screen, colorPalette[theme]["shade5"], (self.x, self.y, self.w, self.h), 0, 5)
            pygame.draw.rect(self.parent.screen, colorPalette[theme]["shade3"], (self.x, self.y, self.w, self.h), 4, 5)
            
            #title (HARDCODED)
            title_surf = self.title_font.render(self.title, True, colorPalette[theme]["shade2"])
            self.parent.screen.blit(title_surf, (self.x + 20, self.y + 20))
            
            #theme window
            if self.is_theme_window:
                self.drawThemeWindow()
            else:
                self.drawStandardFields()
            
            #draw fields
            y_offset = 40
            j = 0
            
            #iterate over fields
            for i, value in self.fields.items():
                
                #draw title of field (HARDCODED)
                text_surf = self.font.render(i + ":", True, colorPalette[theme]["shade2"])
                self.parent.screen.blit(text_surf, (self.x + 20, self.y + y_offset + j * 40))
                
                #draw field (HARDCODED)
                rect = pygame.Rect(self.x + 220, self.y + y_offset + j * 40, 300, 25)
                pygame.draw.rect(self.parent.screen, colorPalette[theme]["shade4"], rect, 0, 5)
                pygame.draw.rect(self.parent.screen, colorPalette[theme]["shade2"], rect, 2, 5)
                
                #display entered information (HARDCODED)
                val_surf = self.font.render(value, True, colorPalette[theme]["shade2"])
                self.parent.screen.blit(val_surf, (rect.x + 5, rect.y + 5))
                
                #cursor indicator (HARDCODED)
                if self.focus == i:
                    cx = rect.x + 5 + val_surf.get_width() + 2
                    cy = rect.y + 5
                    pygame.draw.line(self.parent.screen, colorPalette[theme]["shade1"], 
                                    (cx, cy), (cx, cy + 30), 2)
                
                j += 1
            
            #buttons (HARDCODED)
            save_rect = pygame.Rect(self.x + 80, self.y + self.h - 80, 150, 50)
            cancel_rect = pygame.Rect(self.x + 280, self.y + self.h - 80, 150, 50)
            
            pygame.draw.rect(self.parent.screen, colorPalette["other"]["edit3"], save_rect)
            pygame.draw.rect(self.parent.screen, colorPalette["other"]["del3"], cancel_rect)
            
            #button text (HARDCODED)
            save_txt = self.font.render("Save", True, colorPalette[theme]["shade2"])
            cancel_txt = self.font.render("Cancel", True, colorPalette[theme]["shade2"])
            
            self.parent.screen.blit(save_txt, (save_rect.x + 35, save_rect.y + 10))
            self.parent.screen.blit(cancel_txt, (cancel_rect.x + 25, cancel_rect.y + 10))
            
            #draw open dropdowns
            if self.openDropdown:
                fieldName = self.openDropdown
                opts = self.dropdowns[fieldName]
                
                y_offset = 40
                j = list(self.fields.keys()).index(fieldName)
                
                base_rect = pygame.Rect(self.x + 220, self.y + y_offset + j * 40,
                                        200, 25)
                
                #get visible slice
                visible = opts[self.dropdownScroll : self.dropdownScroll + self.dropdownMaxVisible]
                totalVisible = len(visible)
                
                #dropdown frame
                drop_rect = pygame.Rect(base_rect.x, base_rect.y + 25,
                                        200, self.dropdownItemHeight * totalVisible)
                
                #background frame
                pygame.draw.rect(self.parent.screen, colorPalette[theme]["shade4"], drop_rect, 0, 5)
                pygame.draw.rect(self.parent.screen, colorPalette[theme]["shade2"], drop_rect, 2, 5)
                
                #clip drawing area so items don't escape **the box**
                surface = self.parent.screen
                prevClip = surface.get_clip()
                surface.set_clip(drop_rect)
                
                #draw visible options
                for i, opt in enumerate(visible):
                    opt_rect = pygame.Rect(drop_rect.x,
                                        drop_rect.y + i * self.dropdownItemHeight,
                                        200, self.dropdownItemHeight)
                    
                    pygame.draw.rect(surface, colorPalette[theme]["shade5"], opt_rect)
                    
                    txtsurf = self.font.render(opt, True, colorPalette[theme]["shade1"])
                    surface.blit(txtsurf, (opt_rect.x + 5, opt_rect.y + 5))
                    
                #restore clip
                surface.set_clip(prevClip)
                
                #draw scrollbar if needed
                total = len(opts)
                if total > self.dropdownMaxVisible:
                    barHeight = drop_rect.height * (self.dropdownMaxVisible / total)
                    barY = drop_rect.y + (drop_rect.height - barHeight) * (self.dropdownScroll / (total - self.dropdownMaxVisible))
                    pygame.draw.rect(surface, colorPalette[theme]["shade1"],
                                    pygame.Rect(drop_rect.right - 8, barY, 6, barHeight))
        
        def drawStandardFields(self):
            
            #copy of above text (i cant be bothered to figure out logic)
            
            y_offset = 40
            j = 0
            
            for i, value in self.fields.items():
                text_surf = self.font.render(i + ":", True, colorPalette[theme]["shade2"])
                self.parent.screen.blit(text_surf, (self.x + 20, self.y + y_offset + j * 40))
                
                rect = pygame.Rect(self.x + 220, self.y + y_offset + j * 40, 200, 25)
                pygame.draw.rect(self.parent.screen, colorPalette[theme]["shade4"], rect, 0, 5)
                pygame.draw.rect(self.parent.screen, colorPalette[theme]["shade2"], rect, 2, 5)
                
                val_surf = self.font.render(value, True, colorPalette[theme]["shade2"])
                self.parent.screen.blit(val_surf, (rect.x + 5, rect.y + 5))
                
                #cursor
                if i == self.focus:
                    cx = rect.x + 5 + val_surf.get_width() + 2
                    cy = rect.y + 5
                    pygame.draw.line(self.parent.screen, colorPalette[theme]["shade1"], (cx, cy), (cx, cy + 30), 2)
                
                j += 1
            
            #buttons
            save_rect = pygame.Rect(self.x + 80, self.y + self.h - 80, 150, 50)
            cancel_rect = pygame.Rect(self.x + 280, self.y + self.h - 80, 150, 50)
            
            pygame.draw.rect(self.parent.screen, colorPalette["other"]["edit3"], save_rect)
            pygame.draw.rect(self.parent.screen, colorPalette["other"]["del3"], cancel_rect)
            
            save_txt = self.font.render("Save", True, colorPalette[theme]["shade2"])
            cancel_txt = self.font.render("Cancel", True, colorPalette[theme]["shade2"])
            
            self.parent.screen.blit(save_txt, (save_rect.x + 40, save_rect.y + 10))
            self.parent.screen.blit(cancel_txt, (cancel_rect.x + 25, cancel_rect.y + 10))
        
        def drawThemeWindow(self): #all of this is hardcoded ;(((((
            
            themes = list(colorPalette.keys())
            
            #remove non-themes
            if "other" in themes:
                themes.remove("other")
            if "notes" in themes:
                themes.remove("notes")
            
            cols = 3
            tile_w = 150
            tile_h = 100
            margin = 20
            
            grid_x = self.x + 40
            grid_y = self.y + 80
            
            for i, theme_name in enumerate(themes):
                col = i % cols
                row = i // cols
                
                rect = pygame.Rect(
                    grid_x + col * (tile_w + margin),
                    grid_y + row * (tile_h + margin),
                    tile_w,
                    tile_h
                )
                
                theme_data = colorPalette[theme_name]
                
                #title
                pygame.draw.rect(self.parent.screen, theme_data["shade3"], rect, border_radius=6)
                pygame.draw.rect(self.parent.screen, theme_data["shade1"], rect, 3, border_radius=6)
                
                #draw preview of shades
                shade_h = 14
                yy = rect.y + 10
                for shade in ["shade1", "shade2", "shade3", "shade4", "shade5"]: #we no longer love slicing
                    pygame.draw.rect(
                        self.parent.screen,
                        theme_data[shade],
                        (rect.x + 6, yy, tile_w - 12, shade_h),
                        border_radius=3
                    )
                    yy += shade_h + 4
                    
                #selected outline
                if self.selected_theme == theme_name:
                    pygame.draw.rect(self.parent.screen, (255,255,0), rect, 5, border_radius=6)
                    
                #theme Label
                txt = self.font.render(theme_name, True, theme_data["shade1"])
                self.parent.screen.blit(txt, (rect.x + 10, rect.y + tile_h - 25))
                
            #buttons
            save_rect = pygame.Rect(self.x + 80, self.y + self.h - 80, 150, 50)
            cancel_rect = pygame.Rect(self.x + 280, self.y + self.h - 80, 150, 50)
            
            pygame.draw.rect(self.parent.screen, colorPalette["other"]["edit3"], save_rect)
            pygame.draw.rect(self.parent.screen, colorPalette["other"]["del3"], cancel_rect)
            
            #text
            save_txt = self.font.render("Apply", True, colorPalette[theme]["shade2"])
            cancel_txt = self.font.render("Cancel", True, colorPalette[theme]["shade2"])
            
            self.parent.screen.blit(save_txt, (save_rect.x + 35, save_rect.y + 10))
            self.parent.screen.blit(cancel_txt, (cancel_rect.x + 25, cancel_rect.y + 10))

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
            
            #playback
            if editor.playing:
                
                editor.playPosMs += time_delta * 1000 #convert seconds to ms
                
                #stop if audio ends
                if editor.playPosMs >= editor.songLengthMs:
                    editor.playing = False
                    pygame.mixer.music.stop()
            
            #event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if editor.popup: #pass info to popup
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        editor.popup.click(event.pos)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            editor.popup.handleBackspace()
                        else:
                            editor.popup.handleTextInput(event.unicode)
                    elif editor.popup.openDropdown and event.type == pygame.MOUSEWHEEL:
                        editor.popup.handleDropdownScroll(event)
                    continue
                
                
                #updates scroll for editor
                if event.type == pygame.MOUSEWHEEL and editor.status == "edit":
                    
                    mods = pygame.key.get_mods()
                    
                    #hold alt to zoom
                    if mods & pygame.KMOD_ALT:
                        editor.noteSpacing -= event.y * 2
                        if editor.noteSpacing < 1: editor.noteSpacing = 1
                        if editor.noteSpacing > 9999: editor.noteSpacing = 9999
                        #print(f"zoom: {editor.noteSpacing}")
                    
                    #hold shift to scroll faster
                    elif mods & pygame.KMOD_SHIFT:
                        editor.scroll += event.y * 15
                        if editor.scroll < -9999: editor.scroll = -9999
                        if editor.scroll > 0: editor.scroll = 0
                        #print(f"scroll: {editor.noteSpacing}")
                    
                    #scroll normal speed if no key is held
                    else:
                        editor.scroll += event.y * 4
                        if editor.scroll < -9999: editor.scroll = -9999
                        if editor.scroll > 0: editor.scroll = 0
                        #print(f"scroll: {editor.scroll}")
                
                #pass clicks to editor
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: editor.recieveClick(pygame.mouse.get_pos(), "LEFT")
                    elif event.button == 3: editor.recieveClick(pygame.mouse.get_pos(), "RIGHT")
                
                #pass keypresses to editor
                if event.type == pygame.KEYDOWN:
                    
                    #dev playback hotkey
                    if event.key == pygame.K_p: #run playback
                        pygame.mixer.music.load(path + r"\backing.ogg")
                        editor.togglePlayback()
                    
                    else:
                        editor.recieveKey(event.key)
                
                #update dragend
                if event.type == pygame.MOUSEMOTION and editor.dragging: editor.dragEnd = event.pos
                
                #end drag
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3: #right mouse
                    if editor.dragging:
                        editor.dragging = False
                        editor.finishDragSelect()
                
                #typical keyboard shortcuts
                if event.type == pygame.KEYUP:
                    mods = pygame.key.get_mods()
                    #undo/redo
                    if mods & pygame.KMOD_CTRL:
                        if event.key == pygame.K_z:
                            editor.undo()
                            continue
                        if event.key == pygame.K_y:
                            editor.redo()
                            continue
                    
                    #copy/paste
                    if mods & pygame.KMOD_CTRL:
                        if event.key == pygame.K_c:
                            editor.copy()
                            continue
                        if event.key == pygame.K_v:
                            editor.paste()
                            continue
            
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
    path = r"c:\Users\Benjaminsullivan\Downloads\ddrm3\testsongs\pigstep"
    main()

"""

"""