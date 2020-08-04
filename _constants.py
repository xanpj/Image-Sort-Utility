#IMG_PATH = 
#FOLDER_PATH = 
START_DIALOG = True

#DEBUG True prevents from images being copied into the folders
DEBUG = False
DEV = False
CONSOLE = False

#turn THRESHHOLD down if your words are not understood
THRESHHOLD = 1.0
OCR_LANG='eng'
OCR_AFTER = True #False makes program slightly slower but OCR result are written immediately. True allows only Menu > Run OCR
TIMEOUT= 1 #Speech recognition detection frame (increase for slower speech or longer word lengths) [in s]
CLOSING_TIMEOUT = 4 #Closing timeout to clear threads. [in s]
ABOUT="Any feedback to github.com/xanpj"
IMAGE_TXT = "images_text.txt"
LINE_BREAK = "\n"
DS_STORE = '.DS_Store'

#DISPLAY STRINGS
MSG = {"LISTENING": "Listening...",
 "PAUSED": "Paused. Click on image to continue.",
  "NOT_UNDERSTAND": "Could not understand.",
  "DIR_OCR": "Next: Select Directory to run OCR on",
  "DIR_FOLDERS": "Next: Select Directory that contains all Folders to sort to",
  "DIR_IMAGES": "Next: Select Image Directory",
  "API_ERROR": "API Error. Please check your pocketsphinx installation.",
  "INVALID_FOLDERS": "Invalid Folder Paths or Images",
  "INFO_USAGE_PT2": [
          "2) Speak or Click the options to categorize the image",
          "3) LEFT and RIGHT Arrows to navigate images",
          "Menu > Run OCR: Text inside the images can be extracted to {0}/images_file.txt"
          ],
   "INFO_USAGE_PT1": "1) Use SPACE and ENTER to edit the file name",
   "DONT_CLOSE": "Please don't close the application meanwhile",
   "CLOSING": "CLOSING",
   "RUNNING_OCR": "Running OCR",
   "DIALOG_INSTR": "Dialog Instructions",
   "CLOSE": "Close",
   "OCR_FINISHED": "OCR on {0} images finished",
   "ALL_PROCESSED": "All Images processed",
   "ERROR_COPYING_PT1": "ERROR: Copying image or writing to folder failed!",
   "ERROR_COPYING_PT2": ["Please make sure your file and folder paths and their permissions are correct", "Also check for writing permissions in the app directory."],
   "WAIT_SECONDS": "Cleaning up. Closing in {0} seconds.",
   "PROGRESS": "Progress {0} / {1}",
   "FINISHED": "Finished",
   "RUN_OCR_Q": "Run OCR?"
  }