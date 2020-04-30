from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import img2pdf 
import os 
from PIL import Image


def merger(first_file, folder, output):
    pdfs = PdfFileMerger()
    pdfs.append(first_file)
    deleters = []
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            pdfs.append(os.path.join(folder, file))
        else:
            img_name = file[:file.rfind(".")]
            img_pdf = "img_name.pdf"
            deleters.append(img_pdf)
            if not img_pdf in os.listdir(folder):
                img_path = os.path.join(folder, file)
                with Image.open(img_path) as img:
                    img = img.convert('RGB')
                    width, height = img.size
                    img.save('temp.jpeg', format='JPEG')
                if width < height:
                    a4size = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
                else:
                    a4size = (img2pdf.mm_to_pt(297),img2pdf.mm_to_pt(210))
                layout_fun  = img2pdf.get_layout_fun(a4size)
                pdf_bytes = img2pdf.convert('temp.jpeg', layout_fun=layout_fun)
                with open(img_pdf, 'wb') as fout:
                    fout.write(pdf_bytes)
                pdfs.append(img_pdf)
                os.remove('temp.jpeg')
    pdfs.write(output + ".pdf")
    pdfs.close()
    for pdf in deleters:
        os.remove(pdf)

if __name__ == "__main__":
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename, askdirectory
    Tk().withdraw()
    # Select the file you want to get on top.
    firstPdf = askopenfilename() 
    # Select the directory containing all pdfs and images you want to merge. 
    dirPdfs = askdirectory()
    nameOutput = "mijnoutput"
    merger(firstPdf, dirPdfs, nameOutput)
