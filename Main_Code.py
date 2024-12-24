# Import Libraries required
import os
import fitz  # PyMuPDF
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
import spacy
import pandas as pd
import streamlit as st
from io import StringIO, BytesIO

# For POS tagging and sentence segmentation
nlp = spacy.load("en_core_web_sm")

# Clear temporary files
def clear_temp_files():
    temp_files = ["temp_file", "extracted_text.txt"]
    for file in temp_files:
        if os.path.exists(file):
            os.remove(file)

# Clear cache and temporary files
def clear_cache_and_temp_files():
    clear_temp_files()
    st.cache_data.clear()

# Preprocess images
def preprocess_image(image):
    image = image.convert('L')
    image = image.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    return image

# Applying OCR to a specific part of a PDF page
def apply_ocr_to_bbox(page, bbox):
    pix = page.get_pixmap(clip=bbox)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img = preprocess_image(img)
    text = pytesseract.image_to_string(img)
    return text

# Extract text till "Abstract" keyword
def extract_until_abstract(page, stop_at="Abstract"):
    text_blocks = page.get_text("blocks")
    extracted_text = []
    
    for block in text_blocks:
        block_text = block[4].strip()
        
        # Stop extraction when "Abstract" found
        if stop_at.lower() in block_text.lower():
            break
        
        extracted_text.append(block_text)
    
    return '\n'.join(extracted_text)

# Extract the body after "Abstract" 
def extract_body_after_abstract(page, start_after="Abstract"):
    text_blocks = page.get_text("blocks")
    body_lines = []
    
    abstract_found = False
    
    for block in text_blocks:
        block_text = block[4].strip()
        
        # Appending text after the "Abstract" keyword is found
        if start_after.lower() in block_text.lower():
            abstract_found = True
        
        if abstract_found:
            body_lines.append(block_text)
    
    body_text = ' '.join(body_lines).strip()
    
    return body_text

# Extract and split text from columns 
def extract_text_from_columns(pdf_path, footer_height=50):
    doc = fitz.open(pdf_path)
    combined_text = ''
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        width = page.rect.width
        height = page.rect.height
        
        if page_num == 0:
            # Extract title and authors from the first page until "Abstract"
            header_text = extract_until_abstract(page)
            combined_text += header_text + '\n\n'
            
            # Extract body after "Abstract"
            body_text = extract_body_after_abstract(page)
            combined_text += body_text + '\n\n'
        else:
            text_blocks = page.get_text("blocks")
            
            # Sort text blocks by their Y-coordinate (top to bottom) and then by X-coordinate (left to right)
            text_blocks.sort(key=lambda b: (b[1], b[0]))
            
            left_column_text = []
            right_column_text = []

            for block in text_blocks:
                bbox = block[:4]
                block_text = block[4].strip()
                
                # Avoid footers
                if bbox[3] > height - footer_height:
                    continue
                
                # Determine if the block is in the left or right column
                if bbox[0] < width / 2:
                    left_column_text.append(block_text)
                else:
                    right_column_text.append(block_text)
            
            # Combine text from both columns
            combined_text += ' '.join(left_column_text).strip() + '\n\n'
            combined_text += ' '.join(right_column_text).strip() + '\n\n'

    # Clean the extracted text to remove unnecessary lines
    lines = combined_text.split('\n')
    filtered_lines = [line for line in lines if '©' not in line and len(line.strip()) > 0]
    clean_text = '\n'.join(filtered_lines)
    
    return clean_text

# Eextract text from image files
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    image = preprocess_image(image)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, config=custom_config)
    return text

# Determine the file type and extract text accordingly
@st.cache_data
def extract_text(document_path, file_extension):
    if file_extension == '.pdf':
        return extract_text_from_columns(document_path)
    elif file_extension in ['.png', '.jpg', '.jpeg']:
        return extract_text_from_image(document_path)
    else:
        raise ValueError("Unsupported file format")

# spaCy for more accurate sentence segmentation
def split_text_into_sentences_with_spacy(text):
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    return sentences

# Combine title, author, and body text into one list of sentences
def combine_title_author_body(title, author, body):
    all_sentences = [title, author] + split_text_into_sentences_with_spacy(body)
    return all_sentences

# Create a dataset with POS tags for sentences using spaCy
def create_pos_dataset_for_sentences(sentences):
    pos_data = []
    for sent in sentences:
        doc = nlp(sent)
        pos_tags = [(token.text, token.pos_) for token in doc]
        pos_data.append({
            'Sentence': sent,
            'POS Tags': pos_tags
        })
    return pd.DataFrame(pos_data)

# Clean extracted text
def clean_extracted_text(text):
    cleaned_text = text.encode('ascii', 'ignore').decode('ascii')
    return cleaned_text

# Streamlit app title
st.title("PDF Text Extractor, POS Tagger, and Analyzer")

# Button to clear cache and temporary files
if st.button("Clear Cache and Temporary Files"):
    clear_cache_and_temp_files()
    st.success("Cache and temporary files cleared successfully!")

# File uploader to upload a document
uploaded_file = st.file_uploader("Upload a document...", type=["pdf", "png", "jpg", "jpeg"])

# Check if a file has been uploaded
if uploaded_file is not None:
    # Extract the file extension from the uploaded file
    file_extension = uploaded_file.name.split('.')[-1].lower()
    file_extension = f'.{file_extension}'
    
    # Save the uploaded file temporarily
    with open("temp_file", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Extract text from the uploaded file
    try:
        full_text = extract_text("temp_file", file_extension)
    except ValueError as e:
        st.error(str(e))
        st.stop()
    
    # Clean extracted text to handle encoding issues
    full_text = clean_extracted_text(full_text)

    # Combine title, author, and body text into a single list of sentences
    sentences = split_text_into_sentences_with_spacy(full_text)
    
    if len(sentences) >= 3:
        all_sentences = combine_title_author_body(sentences[0], sentences[1], ' '.join(sentences[2:]))
    else:
        all_sentences = sentences  # Handle case where there are fewer than 3 sentences

    # Join sentences with numbering for better readability
    segmented_text = '\n'.join([f"{i+1}. {sentence}" for i, sentence in enumerate(all_sentences)])

    # Calculate the word count
    word_count = len(full_text.split())

    # Display the segmented sentences, including title and author
    st.text_area("Segmented Sentences", segmented_text, height=300)
    
    # Display the sentence count
    st.write(f"Sentence Count: {len(all_sentences)}")
    
    # Save the extracted text to a local file
    output_file_path = "extracted_text.txt"
    with open(output_file_path, "w") as text_file:
        text_file.write(full_text)

    st.success(f"Text extracted and saved to {output_file_path}")

    # Download link for the extracted text
    with open(output_file_path, "r") as text_file:
        st.download_button("Download extracted text", text_file, file_name=output_file_path)

    # Create POS-tagged dataset for sentences using spaCy
    pos_df = create_pos_dataset_for_sentences(all_sentences)

    # Save the POS-tagged dataset to a CSV file
    csv_buffer = StringIO()
    pos_df.to_csv(csv_buffer, index=False, encoding='utf-8')
    csv_bytes = BytesIO(csv_buffer.getvalue().encode())

    # Download link for the POS-tagged dataset
    st.download_button("Download POS-tagged dataset", csv_bytes, file_name="pos_tagged_dataset.csv", mime="text/csv")