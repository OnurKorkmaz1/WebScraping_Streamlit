import pymupdf
from deep_translator import GoogleTranslator

# Define color "white"
WHITE = pymupdf.pdfcolor["white"]

# This flag ensures that text will be dehyphenated after extraction.
textflags = pymupdf.TEXT_DEHYPHENATE

# Configure the desired translator
to_turkish = GoogleTranslator(source="en", target="tr")  # hedef dil "tr" olarak ayarlandı

# Open the document
doc = pymupdf.open("orca-english.pdf")

# Define an Optional Content layer in the document named "Turkish".
# Activate it by default.
ocg_xref = doc.add_ocg("Turkish", on=True)

# Iterate over all pages
for page in doc:
    # Extract text grouped like lines in a paragraph.
    blocks = page.get_text("blocks", flags=textflags)

    # Every block of text is contained in a rectangle ("bbox")
    for block in blocks:
        bbox = block[:4]  # area containing the text
        text = block[4]  # the text of this block

        # Invoke the actual translation to deliver us a Turkish string
        turkish = to_turkish.translate(text)
    
        # Cover the English text with a white rectangle.
        page.draw_rect(bbox, color=None, fill=WHITE, oc=ocg_xref)

        # Write the Turkish text into the original rectangle
        page.insert_htmlbox(
            bbox, turkish, css="* {font-family: sans-serif;}", oc=ocg_xref
        )

doc.subset_fonts()
doc.ez_save("orca-turkish.pdf")