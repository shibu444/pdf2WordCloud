import streamlit as st
from PyPDF2 import PdfReader
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import string

# Download NLTK stopwords if not already downloaded
nltk.download('stopwords')

# Function to extract text from the uploaded PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to preprocess text
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize text
    words = text.split()
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    
    return " ".join(filtered_words)

# Function to generate a word cloud
def generate_word_cloud(text, max_words=500):
    wordcloud = WordCloud(width=800, height=400, max_words=max_words, background_color='white').generate(text)
    return wordcloud

# Streamlit App UI
st.title("PDF Text to Word Cloud")

# File upload
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    # Extract text from the uploaded PDF
    text = extract_text_from_pdf(uploaded_file)
    
    if text:
        st.subheader("Extracted Text")
        st.text_area("Extracted Text", text[:2000], height=250, help="Only a preview of the text is shown.")
        
        # Preprocess the extracted text
        preprocessed_text = preprocess_text(text)
        
        st.subheader("Preprocessed Text")
        st.text_area("Preprocessed Text", preprocessed_text[:2000], height=250, help="Only a preview of the preprocessed text is shown.")
        
        # Generate word cloud
        st.subheader("Word Cloud")
        wordcloud = generate_word_cloud(preprocessed_text)
        
        # Display the word cloud
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt)
    else:
        st.error("Unable to extract text from the PDF. Make sure the PDF contains selectable text.")
