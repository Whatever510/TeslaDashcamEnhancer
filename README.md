# TeslaDashcamEnhancer
Enhance the Tesla Dashcam by applying a custom LUT to it. Only works with Autopilot 2.5 and Autopilot 3 cars with the RCCB Cameras

### Setup
**Setup your Python environment.** 
Please, clone the repository and install the dependencies. We recommend using Anaconda 3 distribution:
```
conda create -n <environment_name> --file requirements.txt
```

### Executing the code

**Select a Video File:** Select a video by pressing the "Select Video" Button

**Select a Save Location:** Select the save location for the enhanced video by pressing the "Select Save Location" Button. Not necessary for Preview

**Select a filter:** Select a LUT (Look Up Table) from the List

**Preview** If you want to preview the result press the "Preview" button. Change the preview duration by changing the value in the box above. Only accepts numbers 

**Enhance:** Enhanced the video with the selected LUT. See the Progress in the Progress bar below


### Modification

To add additional LUTs add them into the directory `cube_files`. Free LUTs can be found here:
- [35 Free LUTs](https://www.rocketstock.com/free-after-effects-templates/35-free-luts-for-color-grading-videos/)

See recommended LUTs in the file `recommended.txt`