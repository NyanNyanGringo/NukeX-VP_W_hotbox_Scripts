# MY WHOTBOX SCRIPTS

[YouTube](https://www.youtube.com/@parfprod1/videos)  
[Nukepedia](http://www.nukepedia.com/)

I'm long-time user of WHotBox for NukeX, and now I would like to share some useful scripts for it.

### SINGLE NODES

##### Card2 / Card3D
- Set Pivot:
  - Script works on matrix. It helps to set pivot point to Card - no matter how strong it deformed.
![Alt Text](http://www.nukepedia.com/images/users/NyanNyanGringo/my_whotbox_scripts/my_whotbox_scripts_card2.gif)

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
![Alt Text](http://www.nukepedia.com/images/users/NyanNyanGringo/my_whotbox_scripts/my_whotbox_scripts_cornerpin.gif)

##### Cryptomatte
- Make Channels:
  - Lays out all not empty cryptomatte layers.
![Alt Text](http://www.nukepedia.com/images/users/NyanNyanGringo/my_whotbox_scripts/my_whotbox_scripts_crypt.gif)

##### Dissolve
- Fun Time:
  - Makes connection between which knob and tile color in dissolve.
![Alt Text](http://www.nukepedia.com/images/users/NyanNyanGringo/my_whotbox_scripts/my_whotbox_scripts_dissolve.gif)

##### Expression
- Create RGBA:
  - Creates 4 expression nodes that spread out input for 4 channels: r, g, b and a.
- Switch Despill:
  - Switch expression to green/blue despill.
![Alt Text](http://www.nukepedia.com/images/users/NyanNyanGringo/my_whotbox_scripts/my_whotbox_scripts_expr.gif)

##### Matrix (3x3)
- Detect Edge:
  - Set to matrix knobs values that helps to detect edges of input.
![Alt Text](http://www.nukepedia.com/images/users/NyanNyanGringo/my_whotbox_scripts/my_whotbox_scripts_matrix.gif)

##### Merge2
- Mix Range Expr:
  - Set to mix knob expression that switch mix between 0 and 1 based on label range values. For example if label contains two strins "1 - 100" and "150 - 175" in range of 1 to 100  and range from 150 to 175 mix value will 1 - in any other frames mix value will be 0.
![Alt Text](http://www.nukepedia.com/images/users/NyanNyanGringo/my_whotbox_scripts/my_whotbox_scripts_merge2.gif)

##### MergeExpression
- Difference Expr:
  - Find difference between RGB channels of A and B inputs. If in pixel difference of values found
  - this pixel will be 1 in alpha channes. If not difference - pixel will be zero.
  - Useful to make a mask in the end of script for Grain nodes comparing source and compose result images.
![Alt Text](http://www.nukepedia.com/images/users/NyanNyanGringo/my_whotbox_scripts/my_whotbox_scripts_mergedifference.gif)

##### Read
- Open File Browser:
  - Opens current Read file in finder if it exists and select it.
![Alt Text](http://www.nukepedia.com/images/users/NyanNyanGringo/my_whotbox_scripts/my_whotbox_scripts_read.gif)

##### Roto
- Shapes To Nodes:
  - Convert all Roto shapes to single nodes.
![Alt Text](http://www.nukepedia.com/images/users/NyanNyanGringo/my_whotbox_scripts/my_whotbox_scripts_roto.gif)

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
![Alt Text](http://www.nukepedia.com/images/users/NyanNyanGringo/my_whotbox_scripts/my_whotbox_scripts_tracker4.gif)

##### Viewer
- Hide Viewer Lines:
  - Hide viewer lines when it is not selected.
![Alt Text](http://www.nukepedia.com/images/users/NyanNyanGringo/my_whotbox_scripts/my_whotbox_scripts_viewer.gif)

##### Write
- Open File Browser:
  - Opens current Write file in finder if it exists and select it.
- Import File:
  - Import current Write file to Nuke.
- Prerender:
  - Script to make fast prerenders. It automatically read values from topnode so all you need to do is to write unique name.
- Single Frame Export:
  - Works as Prerender but exports only single frame.
![Alt Text](http://www.nukepedia.com/images/users/NyanNyanGringo/my_whotbox_scripts/my_whotbox_scripts_write.gif)

### ALL NODES

##### Project
- Copy Project:
  - Make a new copy of script near current script.
- Open Project:
  - Opens current project in finder and select it.
![Alt Text](http://www.nukepedia.com/images/users/NyanNyanGringo/my_whotbox_scripts/my_whotbox_scripts_project.gif)

##### Selection
- Clear Animation On All:
  - Clear animation on selected nodes knobs.
![Alt Text](http://www.nukepedia.com/images/users/NyanNyanGringo/my_whotbox_scripts/my_whotbox_scripts_clear_anim.gif)
- Connect To TopNode:
  - Connect selected nodes to topnode of selection.
![Alt Text](http://www.nukepedia.com/images/users/NyanNyanGringo/my_whotbox_scripts/my_whotbox_scripts_topnode.gif)
- Paste To Selection:
  - Paste info from boofer to selected nodes.
![Alt Text](http://www.nukepedia.com/images/users/NyanNyanGringo/my_whotbox_scripts/my_whotbox_scripts_paste.gif)
- Merge Stack:
  - Creates stack of merges for selected nodes.
![Alt Text](http://www.nukepedia.com/images/users/NyanNyanGringo/my_whotbox_scripts/my_whotbox_scripts_mergestack.gif)