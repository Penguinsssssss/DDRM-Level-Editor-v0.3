#DDRM Editor 3.1

import tkinter
root = tkinter.Tk()
import pygame
pygame.init()
import penguinsmodule as pm #type: ignore
import os
import json

theme = "seaglass"
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
        "delete": "#FF0000",
        "edit": "#00AA00",
        "play": "#0000FF",
        "deleteout": "#AA0000",
        "editout": "#005500",
        "playout": "#0000AA",
        }
}

class Editor():
    
    def __init__(self, levelPath):
        
        self.scX = root.winfo_screenwidth() * 0.75
        self.scY = root.winfo_screenheight() * 0.75
        self.screen = pygame.display.set_mode((self.scX, self.scY), pygame.SRCALPHA)
        pygame.display.set_caption('DoDoReMi Level Editor V0.3')
        
        self.path = levelPath
        with open(levelPath, "r") as f:
            loaded_data = json.load(f)
        
        self.name, self.author, self.songauthor, self.length, self.bpm, self.key, self.keyscale, self.notes = loaded_data["name"], loaded_data["author"], loaded_data["songauthor"], loaded_data["length"], loaded_data["bpm"], loaded_data["key"], loaded_data["keyscale"], loaded_data["notes"]
    
    def update(self):
        self.screen.fill(colorPalette[theme]["shade6"])
        self.drawLanes()
        pygame.display.update()
    
    def drawLanes(self):
        for i in self.notes:
            height = 0.25
            for j in range(i["lanes"]):
                pygame.draw.rect(self.screen, colorPalette[theme]["shade8"], pm.drawAbsolute(0, height + (j * 0.08), 1, height + (j * 0.08) + 0.01, self.scX, self.scY), 3)

def initEditor(path, ntheme):
    global theme
    theme = ntheme
    return Editor(path)

def main():
    editor = Editor(r"c:\Users\BenjaminSullivan\Downloads\ddrm3\testsongs\library_ruins.json")
    
    clock = pygame.time.Clock()
    running = True
    editor.update()
    while running:
        
        time_delta = clock.tick(60)/1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        editor.update()

if __name__ == "__main__":
    main()
