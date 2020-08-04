# Image-Sort-Utility

Pick an image folder, pick a directory with subfolders, lean back and sort your images using your speech. 

**MacOS Binary** available in [releases](https://github.com/xanpj/Image-Sort-Utility/releases)
Tested on Mac OS Mojave 10.14.6. Catalina support is WIP.

## Usage
Open the application and use speech to categorize the shown images from your directory. The images are copied into the corresponding folders.

Confirm the **Run OCR** dialog at the end to also extract text from the images. All images in the destination folders are run through OCR and their contents are stored in `/images_text.txt`.

You can also **Menu > Run OCR** to run the OCR on an arbitrary directory. When finished this will show a dialog to confirm and then automatically close the program.

## Notes
* Current OCR language is tesseract's default english `'eng'`
* _Categories_ are first-level folders.
* For OCR, only images in root and first-level folders, hence, _categories_, are parsed.


<p align="center">
<img src="https://github.com/xanpj/Image-Sort-Utility/blob/master/docu/DocuImg.png" alt="Cover Image"
    title="Cover Image" width="500" style="margin: 0 auto;" />
</p>

## Tech

* [PyQt5](https://pypi.org/project/PyQt5/)
* [PyQt Threadpool](https://doc.qt.io/archives/qt-4.8/qthreadpool.html)
* [CMU Sphinx](https://pypi.org/project/SpeechRecognition/) (Speech Recognition)
* [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract)

## Install

* Copy [ImageSort](https://github.com/xanpj/ImageSortWithSpeech/releases) into your application folder and **run** it
* Accept mic and folder access when prompted
* Select your image folder, first, and then the directory containing the folders to sort the images into. The rest is explained in the application.

## Development
Install [tesseract](https://github.com/tesseract-ocr/tesseract) and make sure its binary is in your path. 
```
brew install tesseract
```
Use python 3.6.1+
Install further dependencies

```
pip install -r requirements.txt
```
Set `DEV = True` in `_constants.py`
Run

```
python .
```
## Bundling
Set `DEV = False` in `_constants.py`
For building the release you need to put the tesseract files into the root directory of the executable via a `.spec` file with [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/spec-files.html)
Use something like `Tree(<tesseract dir>)` after ` a.binaries,` to simply put the tesseract files into the executable.


## Languages
You can change the OCRs language by changing `OCR_LANG` i.e. to `eng+fra` in `_constants.py` and downloading the corresponding dataset from [Tesseract-OCR lang](https://github.com/tesseract-ocr/tessdata) into your 'tessdata/' folder.
For bundling, put the `.traineddata` file into
 `dist/tesseract/share/testdata/` before running `pyinstaller`.
