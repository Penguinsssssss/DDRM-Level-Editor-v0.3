#DDRM Level Editor 3.0

import tkinter
root = tkinter.Tk()
import pygame
pygame.init()
import os
import json
import penguinsmodule as pm #type: ignore
import DDRMeditor as de #type: ignore
#import DDRMpopups as dp #type: ignore

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
    "ruby": {
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
        "gray": "#888888",
        "lightgray": "#BBBBBB",
        "darkgray": "#444444",
        "del1": "#FF7777", #button fills
        "edit1": "#77FF77",
        "play1": "#7777FF",
        "del2": "#AA4444", #button outlines
        "edit2": "#44AA44",
        "play2": "#4444AA",
        "del3": "#883333", #selected variants
        "edit3": "#118811",
        "play3": "#404088",
        }
}



class Menu:
    
    def __init__(self, levels_path):
        
        #setup screen
        self.scX = root.winfo_screenwidth() * 0.25
        self.scY = root.winfo_screenheight() * 0.75
        self.screen = pygame.display.set_mode((self.scX, self.scY), pygame.SRCALPHA)
        pygame.display.set_caption('DoDoReMi Level Editor V0.3')
        
        #get data from levels folder
        levels = {}
        for entry in os.scandir(levels_path):
            if entry.is_file():
                print(f"File: {entry.name} (Path: {entry.path})")
                levels[entry.name] = entry.path
        
        #create new level button
        self.addLevelButton = self.AddLevelButton(self, self.screen)
        
        #create list of button objects
        self.levelButtons = []
        id = 1
        for i in levels.values():
            self.levelButtons.append(self.LevelButton(self, self.screen, i, id))
            id += 1
        
        #globals
        self.scroll = 0
        self.path = levels_path
    
    def update(self, withholdUpdate=False):
        
        #update screen
        self.screen.fill(colorPalette[theme]["shade6"])
        self.addLevelButton.update()
        self.addLevelButton.darken(pygame.mouse.get_pos())
        for i in self.levelButtons: i.update()
        for i in self.levelButtons: i.darken(pygame.mouse.get_pos())
        if not withholdUpdate: pygame.display.update()
    
    #check which screen elements have been clicked (if any)
    def recieveClick(self, pos):
        
        self.addLevelButton.recieveClick(pygame.mouse.get_pos())
        
        for i in self.levelButtons:
            if i.recieveClick(pos):
                print(i.name, i.recieveClick(pos))
                if i.recieveClick(pos) == "edit":
                    #open an editor instance of a given path
                    pygame.quit()
                    de.path = i.path
                    de.theme = theme
                    de.main()
                if i.recieveClick(pos) == "delete":
                    #print(dp.confirmDelete())
                    pass

    class TextBox: #clever text implimentation, copied verbaitum from online
    
        def __init__(self, parent, x, y, w, h, placeholder, fontpath="C:/Windows/Fonts/Ebrima.ttf", fontsize=32):
                self.parent = parent
                self.y = y
                self.rect = pygame.Rect(pm.drawAbsolute(x, y, w, h, parent.scX, parent.scY))
                self.font = pygame.font.Font(fontpath, int(fontsize))
                self.text = ""
                self.placeholder = placeholder
                self.active = False
                self.caret_visible = True
                self.caret_timer = 0
                self.caret_position = 0
                self.focus_color = colorPalette[theme]["shade1"]
                self.unfocus_color = colorPalette[theme]["shade3"]
                self.text_color = colorPalette[theme]["shade2"]
                self.placeholder_color = colorPalette[theme]["shade4"]

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False
            if not self.active:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if self.caret_position > 0:
                        self.text = self.text[:self.caret_position - 1] + self.text[self.caret_position:]
                        self.caret_position -= 1
                elif event.key == pygame.K_DELETE:
                    if self.caret_position < len(self.text):
                        self.text = self.text[:self.caret_position] + self.text[self.caret_position + 1:]
                elif event.key == pygame.K_LEFT:
                    self.caret_position = max(0, self.caret_position - 1)
                elif event.key == pygame.K_RIGHT:
                    self.caret_position = min(len(self.text), self.caret_position + 1)
                elif event.key == pygame.K_HOME:
                    self.caret_position = 0
                elif event.key == pygame.K_END:
                    self.caret_position = len(self.text)
                elif event.key == pygame.K_TAB:
                    # handled by popup to move focus
                    pass
                elif event.key == pygame.K_RETURN:
                    # handled by popup
                    pass
                else:
                    if event.unicode.isprintable():
                        self.text = self.text[:self.caret_position] + event.unicode + self.text[self.caret_position:]
                        self.caret_position += 1

        def update(self, dt):
            self.caret_timer += dt
            if self.caret_timer >= 500:
                self.caret_visible = not self.caret_visible
                self.caret_timer = 0

        def draw(self, surface):
            pygame.draw.rect(surface, self.focus_color if self.active else self.unfocus_color, self.rect, 2, 5)
            txt = self.font.render(self.text if self.text else self.placeholder, True,
            self.text_color if self.text else self.placeholder_color)
            surface.blit(txt, (self.rect.x + 8, self.rect.y + (self.rect.height - txt.get_height()) / 2))

            # Draw caret
            if self.active and self.caret_visible:
                caret_x = self.rect.x + 8 + self.font.size(self.text[:self.caret_position])[0]
                caret_y = self.rect.y + 10
                pygame.draw.line(surface, self.text_color, (caret_x, caret_y),
                (caret_x, caret_y + self.font.get_height() - 10), 2)

    class AddLevelButton:
        
        def __init__(self, parent, screen):
            
            self.parent = parent
            self.screen = screen
            
            self.isDark = False
        
        def update(self):
            leftmargin = 0.05
            rightmargin = 0.95
            spacing = 0.28
            offset = 0.25
            scrollm = 0.1
            y = (spacing - offset) - self.parent.scroll * scrollm
            gap = 0.085
            
            #level box
            pygame.draw.rect(self.screen, colorPalette[theme]["shade4" if self.isDark else "shade3"], pm.drawAbsolute(leftmargin, y, rightmargin, y + 0.25, self.parent.scX, self.parent.scY), 0, 5)
            pygame.draw.rect(self.screen, colorPalette[theme]["shade2" if self.isDark else "shade1"], pm.drawAbsolute(leftmargin, y, rightmargin, y + 0.25, self.parent.scX, self.parent.scY), 2, 5)
            self.pos = pm.drawAbsolute(leftmargin, y, rightmargin, y + 0.25, self.parent.scX, self.parent.scY)
            
            pygame.draw.rect(self.screen, colorPalette[theme]["shade2" if self.isDark else "shade1"], pm.drawAbsolute(0.49, y + 0.075, 0.51, y + 0.175, self.parent.scX, self.parent.scY), 0, 5)
            pygame.draw.rect(self.screen, colorPalette[theme]["shade2" if self.isDark else "shade1"], pm.drawAbsolute(0.5 - gap, y + 0.12, 0.5 + gap, y + 0.13, self.parent.scX, self.parent.scY), 0, 5)
        
        def darken(self, pos):
            if self.pos[2] + self.pos[0] > pos[0] > self.pos[0] and self.pos[3] + self.pos[1] > pos[1] > self.pos[1]:
                self.isDark = True
                return
            else: self.isDark = False
        
        def recieveClick(self, pos):
            if self.pos[2] + self.pos[0] > pos[0] > self.pos[0] and self.pos[3] + self.pos[1] > pos[1] > self.pos[1]:
                addLevelPoppup = self.parent.AddLevelPoppup(self.parent)
    
    class LevelButton:
        
        def __init__(self, parent, screen, path, id):
            
            self.parent = parent
            self.screen = screen
            self.id = id
            self.path = path
            
            #update which items are highlighted visually
            self.isDark = False #level
            self.ddark = False #delete
            self.edark = False #edit
            self.pdark = False #playback
            
            #get data from json
            with open(path, "r") as f:
                loaded_data = json.load(f)
            
            #save json data
            self.name, self.author, self.songauthor, self.length, self.bpm, self.key, self.keyscale, = loaded_data["name"], loaded_data["author"], loaded_data["songauthor"], loaded_data["length"], loaded_data["bpm"], loaded_data["key"], loaded_data["keyscale"]
        
        def update(self):
            
            #consts
            leftmargin = 0.05
            rightmargin = 0.95
            spacing = 0.28
            offset = 0.25
            scrollm = 0.1
            y = ((self.id + 1) * spacing - offset) - self.parent.scroll * scrollm
            
            #level box
            pygame.draw.rect(self.screen, colorPalette[theme]["shade5" if self.isDark else "shade4"], pm.drawAbsolute(leftmargin, y, rightmargin, y + 0.25, self.parent.scX, self.parent.scY), 0, 5)
            pygame.draw.rect(self.screen, colorPalette[theme]["shade4" if self.isDark else "shade3"], pm.drawAbsolute(leftmargin, y, rightmargin, y + 0.25, self.parent.scX, self.parent.scY), 2, 5)
            
            #left and right of box
            bx1 = rightmargin - 0.15
            bx2 = rightmargin - 0.03
            
            #delete
            pygame.draw.rect(self.screen, colorPalette["other"]["del3" if self.ddark else "del2"], pm.drawAbsolute(bx1, y + 0.20, bx2, y + 0.24, self.parent.scX, self.parent.scY), 0, 5)
            pygame.draw.rect(self.screen, colorPalette["other"]["del2" if self.ddark else "del1"], pm.drawAbsolute(bx1, y + 0.20, bx2, y + 0.24, self.parent.scX, self.parent.scY), 2, 5)
            
            #edit
            pygame.draw.rect(self.screen, colorPalette["other"]["edit3" if self.edark else "edit2"], pm.drawAbsolute(bx1, y + 0.15, bx2, y + 0.19, self.parent.scX, self.parent.scY), 0, 5)
            pygame.draw.rect(self.screen, colorPalette["other"]["edit2" if self.edark else "edit1"], pm.drawAbsolute(bx1, y + 0.15, bx2, y + 0.19, self.parent.scX, self.parent.scY), 2, 5)
            
            #playback
            pygame.draw.rect(self.screen, colorPalette["other"]["play3" if self.pdark else "play2"], pm.drawAbsolute(bx1, y + 0.10, bx2, y + 0.14, self.parent.scX, self.parent.scY), 0, 5)
            pygame.draw.rect(self.screen, colorPalette["other"]["play2" if self.pdark else "play1"], pm.drawAbsolute(bx1, y + 0.10, bx2, y + 0.14, self.parent.scX, self.parent.scY), 2, 5)
            
            #update positions of screen elements
            self.pos = pm.drawAbsolute(leftmargin, y, rightmargin, y + 0.25, self.parent.scX, self.parent.scY)
            self.dpos = pm.drawAbsolute(bx1, y + 0.20, bx2, y + 0.24, self.parent.scX, self.parent.scY)
            self.epos = pm.drawAbsolute(bx1, y + 0.15, bx2, y + 0.19, self.parent.scX, self.parent.scY)
            self.ppos = pm.drawAbsolute(bx1, y + 0.10, bx2, y + 0.14, self.parent.scX, self.parent.scY)
            
            #draw text
            pm.text(self.screen, #name
                    self.name,
                    pm.drawAbsolute(leftmargin + 0.01, y + 0.03, 0, 0, self.parent.scX, self.parent.scY),
                    colorPalette[theme]["shade2" if self.isDark else "shade1"],
                    32, #fontsize
                    center="left",
                    font="C:/Windows/Fonts/Ebrima.ttf"
                    )
            pm.text(self.screen, #songauthor
                    self.songauthor,
                    pm.drawAbsolute(leftmargin + 0.01, y + 0.085, 0, 0, self.parent.scX, self.parent.scY),
                    colorPalette[theme]["shade4" if self.isDark else "shade3"],
                    24, #fontsize
                    center="left",
                    font="C:/Windows/Fonts/Seguisb.ttf"
                    )
            
            #draw text debug
            if 1==2:
                
                
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
            
            
            #debug single palatte
            if 1==2:
                for i in range(8):
                    pygame.draw.rect(self.screen, colorPalette[theme][f"shade{i + 1}"], [10, i * 10 + 10, 10, 10], 5, 10)
            
            #debug all palattes
            if 1==2:
                iindex = 0
                debuglkrghqwerhj = 50
                for i in colorPalette:
                    iindex += 1
                    if iindex > len(colorPalette) - 2: break
                    for j in range(8):
                        pygame.draw.rect(self.screen, colorPalette[i][f"shade{j + 1}"], [iindex * debuglkrghqwerhj + debuglkrghqwerhj, j * debuglkrghqwerhj + debuglkrghqwerhj, debuglkrghqwerhj, debuglkrghqwerhj], 10, debuglkrghqwerhj)
            
        def recieveClick(self, pos):
            
            #check which screen element got clicked
            if self.dpos[2] + self.dpos[0] > pos[0] > self.dpos[0] and self.dpos[3] + self.dpos[1] > pos[1] > self.dpos[1]: return "delete"
            elif self.epos[2] + self.epos[0] > pos[0] > self.epos[0] and self.epos[3] + self.epos[1] > pos[1] > self.epos[1]: return "edit"
            elif self.ppos[2] + self.ppos[0] > pos[0] > self.ppos[0] and self.ppos[3] + self.ppos[1] > pos[1] > self.ppos[1]: return "playback"
            elif self.pos[2] + self.pos[0] > pos[0] > self.pos[0] and self.pos[3] + self.pos[1] > pos[1] > self.pos[1]: return "level"
        
        def darken(self, pos):
            
            #check if delete is highlighted
            if self.dpos[2] + self.dpos[0] > pos[0] > self.dpos[0] and self.dpos[3] + self.dpos[1] > pos[1] > self.dpos[1]:
                self.ddark = True
                return
            else: self.ddark = False
            
            #check if edit is highlighted
            if self.epos[2] + self.epos[0] > pos[0] > self.epos[0] and self.epos[3] + self.epos[1] > pos[1] > self.epos[1]:
                self.edark = True
                return
            else: self.edark = False
            
            #check if playback is highlighted
            if self.ppos[2] + self.ppos[0] > pos[0] > self.ppos[0] and self.ppos[3] + self.ppos[1] > pos[1] > self.ppos[1]:
                self.pdark = True
                return
            else: self.pdark = False
            
            #check if level is highlighted
            if self.pos[2] + self.pos[0] > pos[0] > self.pos[0] and self.pos[3] + self.pos[1] > pos[1] > self.pos[1]:
                self.isDark = True
                return
            else: self.isDark = False

    class AddLevelPoppup:
        
        def __init__(self, parent):
            
            print("lolm")
            self.data = {
                "name": "",
                "songauthor": "",
                "key": "",
                "bpm": ""
            }
            self.parent = parent
            self.main()
        
        def main(self):
            
            active = True
            
            self.textboxes = [
                self.parent.TextBox(self.parent, 0.25, 0.26, 0.75, 0.26 + 0.07, "Level Name"),
                self.parent.TextBox(self.parent, 0.25, 0.40, 0.75, 0.40 + 0.07, "Song Author"),
                self.parent.TextBox(self.parent, 0.25, 0.54, 0.75, 0.54 + 0.07, "Key"),
                self.parent.TextBox(self.parent, 0.25, 0.68, 0.75, 0.68 + 0.07, "BPM")
            ]
            
            focus_index = 0
            self.textboxes[0].active = True
            
            clock = pygame.time.Clock()
            
            while active:
                
                time_delta = clock.tick(60)/1000.0
                
                self.parent.update(withholdUpdate=True)
                self.update()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        active = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            active = False
                        elif event.key == pygame.K_RETURN: #clever text implimentation copied verbaitum from online
                            # save and close if all fields filled
                            if all(tb.text.strip() for tb in self.textboxes):
                                self.data["name"] = self.textboxes[0].text.strip()
                                self.data["songauthor"] = self.textboxes[1].text.strip()
                                self.data["key"] = self.textboxes[2].text.strip()
                                self.data["bpm"] = self.textboxes[3].text.strip()
                                print("Popup data:", self.data)
                                active = False
                        elif event.key == pygame.K_TAB:
                            # Cycle focus
                            self.textboxes[focus_index].active = False
                            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                                focus_index = (focus_index - 1) % len(self.textboxes)
                            else:
                                focus_index = (focus_index + 1) % len(self.textboxes)
                            self.textboxes[focus_index].active = True

                    for tb in self.textboxes:
                        tb.handle_event(event)

                for tb in self.textboxes:
                    tb.update(time_delta)
                
                pygame.display.update()
        
        def update(self):
            
            bx = 0.15
            by = 0.15
            bw = 0.85
            bh = 0.85
            
            dim = pygame.Surface(self.parent.screen.get_size(), pygame.SRCALPHA)
            dim.fill((0, 0, 0, 180))  # 0–255 alpha, higher = darker
            self.parent.screen.blit(dim, (0, 0))
            
            pygame.draw.rect(self.parent.screen, colorPalette[theme]["shade4"], pm.drawAbsolute(bx, by, bw, bh, self.parent.scX, self.parent.scY), 0, 5)
            pygame.draw.rect(self.parent.screen, colorPalette[theme]["shade3"], pm.drawAbsolute(bx, by, bw, bh, self.parent.scX, self.parent.scY), 2, 5)
            
            font = pygame.font.Font("C:/Windows/Fonts/Ebrima.ttf", 28)
            labels = ["Level Name", "Song Author", "Key", "BPM"]
            
            for i, label in enumerate(labels): #clever text implimentation, copied verbaitum from online
                txt = font.render(label, True, colorPalette[theme]["shade1"])
                rect = txt.get_rect()
                rect.topleft = pm.drawAbsolute(0.18, self.textboxes[i].y - 0.06, 0, 0, self.parent.scX, self.parent.scY)[0:2]
                self.parent.screen.blit(txt, rect)

            # Textboxes
            for tb in self.textboxes:
                tb.draw(self.parent.screen)
            
            pygame.display.update()

def main():
    
    #init
    menu = Menu("c:/users/benja/downloads/ddrm3/testsongs")
    clock = pygame.time.Clock()
    running = True
    menu.update()
    
    while running:
        
        #keep game running at 60 fps
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
        
        #update screen
        menu.update()

main()