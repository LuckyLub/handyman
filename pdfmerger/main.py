from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfile
import img2pdf 
import os 
from pathlib import Path

from PIL import Image

def image2Pdf(folder:str, img:str, outputPath:str=None)->str:
    """ Converts an image to a pdf in A4 format. Does not support HEIC format.

    Arguments:
        folder: string, path where image is stored.
        img: string, name of image. Should include file extension.
        outputPath: string, optional, path to directory where pdf should be
            stored.

    Returns:
        Path to resulting pdf as string.
    """
    imgName = img[:img.rfind(".")]
    if outputPath:
        imgPdf = f"{outputPath}/{imgName}.pdf"
    else: 
        imgPdf = f"{imgName}.pdf"
    imgPath = os.path.join(folder, img)
    # Delete alpha channel by converting to RGB. Save as temp file.
    with Image.open(imgPath) as img:
        img = img.convert('RGB')
        width, height = img.size
        img.save('temp.jpeg', format='JPEG')
    # Determine orientation of the image and set pdf size accordingly
    if width < height:
        a4Size = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
    else:
        a4Size = (img2pdf.mm_to_pt(297),img2pdf.mm_to_pt(210))
    layout = img2pdf.get_layout_fun(a4Size)
    # Convert the image to pdf, delete temp file.
    pdfBytes = img2pdf.convert('temp.jpeg', layout_fun=layout)
    with open(imgPdf, 'wb') as fout:
        fout.write(pdfBytes)
    os.remove('temp.jpeg')
    return imgPdf

def merger():
    """ Merges a pdf with all the pdfs and images from the selected folder."""
    Tk().withdraw()
    # Select the file you want to get on top.
    firstFile = askopenfilename(title = "Select the file you want on top.")
    if not firstFile:
        return None
    # Select the directory containing all pdfs and images you want to merge. 
    folder = askdirectory(title = "Select the folder containing the files you "
                                  "want to merge.")
    if not folder:
        return None
    
    deleters = [] # collector for the temp pdfs created for images.
    pdfs = PdfFileMerger()
    
    files = [os.path.split(Path(firstFile))]
    for f in os.listdir(folder):
        files.append((folder, f))

    for index, (p, f) in enumerate(files):
        # if the first file is in the same folder as the rest of the files
        # only add it once.
        if index != 0 and Path(os.path.join(p,f)) == Path(firstFile):
            continue
        elif f.endswith(".pdf"):
            pdfs.append(os.path.join(folder, f))
        else:
            pdfImage = image2Pdf(folder, f)
            pdfs.append(pdfImage)
            deleters.append(pdfImage)
    
    f = asksaveasfile(defaultextension=".pdf")
    output = f.name
    f.close()
    pdfs.write(output)
    pdfs.close()
    for pdf in deleters:
        os.remove(pdf)
    os.startfile(output)

if __name__ == "__main__":
    merger()
