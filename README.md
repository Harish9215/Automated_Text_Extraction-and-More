# 🚀 Automated Data Extraction from PDFs 📄
Effortlessly extract structured data from unstructured PDF documents!
<br>

## 🌟 Overview

This project develops a state-of-the-art Automated Data Extraction Tool designed to process PDF documents and convert their content into structured datasets. By combining the power of OCR, Natural Language Processing (NLP), and Machine Learning, the tool achieves high accuracy and efficiency in extracting information.

Whether you’re working with text-based PDFs or image-heavy documents, this tool simplifies data processing for industries like finance, healthcare, and academia.

### ✨ Features
  •	🔍 Advanced OCR: Extract data from scanned or image-based PDFs using Tesseract. <br>	
	•	🧠 Intelligent NLP: Segment sentences, identify parts of speech, and normalize text with spaCy.<br>
	•	📊 Structured Outputs: Convert complex data (e.g., tables, graphs) into usable formats like CSV.<br>
	•	🖼 Visualizations: Generate word clouds and clustering analysis for insights.<br>
	•	💻 User-Friendly Interface: Built with Streamlit, enabling easy uploads and data previews.<br>
<br>

## 🚀 How to Use
### Step 1: Clone the Repository
Start by cloning the repository to your local machine: <br>
```
git clone https://github.com/Harish9215/Automated_Text_Extraction-and-More.git
cd Automated_Text_Extraction-and-More
```

### Step 2: Set Up Your Environment
Ensure you have Python installed (preferably version 3.8 or higher). Install the required libraries by running:
 ```
pip install -r requirements.txt
```
### Step 3: Launch the Application
Run the Streamlit interface to interact with the tool:
```
streamlit run src/interface.py
``` 
 ### Step 4: Upload your PDF and let the magic happen! 🪄 
 1. Open the interface in your browser (Streamlit provides the link). <br>
 2. Drag and drop your PDF file into the uploader or use the Browse button. <br>
 3. Click on Process to start the extraction. <br>

### Step 5: View and Download Results
•	Extracted Text: Review the extracted content in the interface. <br>
•	Download Options: Save the structured data (e.g., CSV or plain text) for further use. <br>
•	Visualizations: Check out the generated word clouds and clustering visualizations for insights. <br>
<br>
 
 ## 🛠️ Tech Stack
 •	Programming Language: Python 🐍 <br>
 •	Tesseract OCR for text extraction. <br>
 •	spaCy for NLP. <br>
 •	PyMuPDF for PDF parsing. <br>
 •	Streamlit for UI development. <br>
 •	Other Tools: WordCloud, TF-IDF for text vectorization, Clustering with K-Means. <br>
 <br>

 ## 📈 Performance Metrics
 •	Precision: 99.23% ✔️ <br>
	•	Recall: 94.61% 🔥 <br>
	•	F1 Score: 96.85% ⚡ <br>
 <br>

 ## 📜 Future Enhancements
 •	✨ Improve OCR accuracy for handwritten documents. <br>
	•	🌐 Support for multi-language PDF content. <br>
	•	⚡ Add real-time processing capabilities. <br>
