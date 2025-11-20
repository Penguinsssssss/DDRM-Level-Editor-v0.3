# DDRM-Level-Editor-v0.3
Benjamin Sullivan junior year semester 1 Programming Studio project

# Task List (No specific order)
- Save / Save as / Auto Save ?
- Export as level file
  - Currently stored in beats/measures, not milliseconds
- Allow users to edit level info when in menu
  - Example, BPM, audio file, file name
- Create new parts
  - Get list of instuments for each part
  - Add new instruments to part
  - Toggle view between parts
- Playback button
   - Allow users to start playback from later in the level ?
- Create demo song(s)

# Timeline (sorted newest to oldest)

## Wed Nov. 19 (night)
- Users can now save edits made to their level under File >> Save
- Debugs
  - Buttons no longer "miss" clicks sporadically
  - Editor no longer crashes when opening a dropdown menu with another dropdown active

## Wed Nov. 19
- Changed system for storing notes
  - Old system was stored in beats, example beat 22
  - Now stores notes in measures, example measure 5 beat 2 of 4

## Tues Nov. 18 (night)
- Users can now zoom in and out by holding alt
- The first beat of every measure is now enlarged (meter is stored internally)

## Tues Nov. 18
- Utilbar now has drowdown windows
- Options in the dropdown are highlighted
- Upon clicking a function will run based on the highlighted option
- Menu closed by clicking anywhere outside the menu

## Thurs Nov. 13
- Users can now add and remove notes
- Changes are not yet saved to the json

## Wed Nov. 5
- I have been attempting to make the note class be able to be clicked and dragged around, but things have been breaking
- I will revert to a previous version of the code and try again

## Wed Oct. 29
- Each note is now an object of the "note" class

## Mon Oct. 27
- Util bar now has clickable options (file, edit, view, tools)

## Wed Oct. 22
- Template in place for "UtilBar"
  - Bar that allows users to access tabs like "file" or "view"

## Mon Oct. 20
- Notes are now controlled by the scroll wheel in the editor

## Wed Oct. 15
- Create Level pop-up now has textboxes to enter information, saves data to a new file

## Tue Oct. 14
- Create Level button now displays pop-up window

## Mon Oct. 13
- Added "Create Level" button
- Button does nothing yet

## Thu Oct. 9
- Created "Editor" program, edit button now opens an instance of the editor

## Wed Oct. 8
- Levels now have interactable buttons
  - Playback
  - Edit
  - Delete
- Clicking edit opens an editor instance for the given level

## Tue Sep. 30
- Added "edit" tab to level display
  - Able to Playback/Edit/Delete levels from menu

## Thurs Sep. 26
- Changed menu dimensions (16:9 - 4:9)
- Updated all buttons accordingly

## Mon Sep. 22
- New font setup (ebrima.ttf)

## Thurs Sep. 11
- Work on level storing concept
  - .json format
  - List level attributes at top of page (name, bpm, key, etc)

## Tuesday Sep. 9
- Added three new themes
- Buttons can now detect when they are clicked
- The code now only updates the screen when somthing has changed, not every frame

## Monday Sep. 8
- Added color theming
  - 7 color themes

## Pre School Year
- Started working on menu system
- Can display .jsons from a folder
- Can menu has scroll wheel capabilities
  - Save to games code (<1 week)
