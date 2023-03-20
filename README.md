# MY WHOTBOX SCRIPTS

[YouTube](https://www.youtube.com/)  
[Nukepedia](http://www.nukepedia.com/)

I'm long-time user of WHotBox for NukeX, and now I would like to share some useful scripts for it.

### SINGLE NODES

##### Card2 / Card3D

- Set Pivot:
  - Script works on matrix. It helps to set pivot point to Card - no matter how strong it deformed.

##### CornerPin2D
This bundle of scripts are simple but save much time.
- Set Frame:
  - Copies "to" params to "from" and remove all keyframes.
- Invert:
  - Switch between Matchmove and Stabilize mode.
- Set key:
  - Set keyframe to "to" or to "from" knobs in current frame.
- No animation:
  - Removes animation in "to" or "from" knobs.
- Delete key:
  - Delete keyframes in "to" or "from" knobs in current frame.

##### Cryptomatte
- Make Channels:
  - Lays out all not empty cryptomatte layers.

##### Dissolve
- Fun Time:
  - Makes connection between which knob and tile color in dissolve.

##### Expression
- Create RGBA:
  - Creates 4 expression nodes that spread out input for 4 channels: r, g, b and a.
- Switch Despill:
  - Switch expression to green/blue despill.

##### Matrix (3x3)
- Detect Edge:
  - Set to matrix knobs values that helps to detect edges of input.

##### Merge2
- Mix Range Expr:
  - Set to mix knob expression that switch mix between 0 and 1 based on label range values.
  - For example if label contains two strins "1 - 100" and "150 - 175" in range of 1 to 100
  - and range from 150 to 175 mix value will 1 - in any other frames mix value will be 0.

##### MergeExpression
- Difference Expr:
  - Find difference between RGB channels of A and B inputs. If in pixel difference of values found
  - this pixel will be 1 in alpha channes. If not difference - pixel will be zero.
  - Useful to make a mask in the end of script for Grain nodes comparing source and compose result images.

##### Read
- Open File Browser
  - Opens current Read file in finder if it exists and select it.

##### Roto
- Shapes To Nodes:
  - Convert all Roto shapes to single nodes.

##### Tracker4
This bundle of scripts are simple but save much time.
- Create Matchmove:
  - Craetes transform matchmove nodes from tracker or trackers.
- Create Stab:
  - Craetes transform stabilize nodes from tracker or trackers.
- Toggle Rotation*:
  - Switch on/off rotation for all trackers.
- Toggle Scale*:
  - Switch on/off scale for all trackers.
- Toggle Translation*:
  - Switch on/off transaltion for all trackers.
* not my scripts - do not remember author.

##### Viewer
- Hide Viewer Lines:
  - Hide viewer lines when it is not selected.

##### Write
- Open File Browser
  - Opens current Write file in finder if it exists and select it.
- Import File
  - Import current Write file to Nuke.
- Prerender
  - Script to make fast prerenders. It automatically read values from topnode so all you need to do is to write unique name.
- Single Frame Export
  - Works as Prerender but exports only single frame.

### ALL NODES

##### Project
- Copy Project
  - Make a new copy of script near current script.
- Open Project
  - Opens current project in finder and select it.

##### Selection
- Clear Animation On All
  - Clear animation on selected nodes knobs.
- Connect To TopNode
  - Connect selected nodes to topnode of selection.
- Paste To Selection
  - Paste info from boofer to selected nodes.
- Merge Stack
  - Creates stack of merges for selected nodes.
- Set IP
  - Set selected node as IP for Viewer.
- Set Value For Knobs
  - Helps to set values for many nodes fast.