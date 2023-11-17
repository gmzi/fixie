import PyPDF2

def cropFile(source, key_phrase, output):
    print('cropping...')
    with open(source, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()
        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page_text = pdf_reader.pages[page_num].extract_text()
            if key_phrase in page_text:
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)

    if len(pdf_writer.pages):
        with open(output, 'wb') as output_file:
            pdf_writer.write(output_file)
            return True
    else: 
        print("cropping failed")
        return False

__all__ = ["cropFile"]