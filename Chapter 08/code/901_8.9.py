import psycopg2
import pandas as pd
import numpy as np
import PyPDF2
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
# Read the Wind Turbine Maintenance Manual PDF file
with open('wind_turbine_maintenance_manual.pdf', 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    # Extract text from the first page of the PDF
    first_page = pdf_reader.pages[0]
    manual_text = first_page.extract_text()
print(manual_text)
# Remove stop words from the text
stop_words = set(stopwords.words('english'))
filtered_tokens = [word for word in word_tokenize(manual_text) if word.lower() not in stop_words]
# Define keywords for identifying relevant information in the manual
relevant_keywords = ['power output', 'wind speed', 'temperature']
# Identify sentences containing relevant information using the keywords
relevant_sentences = []
for sentence in nltk.sent_tokenize(manual_text):
    for keyword in relevant_keywords:
        if keyword in sentence.lower():
            relevant_sentences.append(sentence)
            break
# Extract the relevant information from the relevant sentences using regular expressions
power_output_regex = r'power output.*?(\d+)\s*%'
wind_speed_regex = r'wind speed.*?(\d+)\s*meters per second'
temperature_regex = r'temperature.*?(\d+)\s*°c'
power_output_threshold, wind_speed_threshold, temperature_threshold = None, None, None
for sentence in relevant_sentences:
    match = re.search(power_output_regex, sentence, re.IGNORECASE)
    if match:
        power_output_threshold = int(match.group(1))
    match = re.search(wind_speed_regex, sentence, re.IGNORECASE)
    if match:
        wind_speed_threshold = int(match.group(1))
    match = re.search(temperature_regex, sentence, re.IGNORECASE)
    if match:
        temperature_threshold = int(match.group(1))
# Print the extracted thresholds
if power_output_threshold is not None:
    print("Threshold for power output:", power_output_threshold)
if wind_speed_threshold is not None:
    print("Threshold for wind speed:", wind_speed_threshold)
if temperature_threshold is not None:
    print("Threshold for temperature:", temperature_threshold)
# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(
        host="localhost",
        database="IoTDataLake",
        user="postgres",
        password=""
    )
except:
    print("Unable to connect to the database")
# Create a table if it does not already exist
with conn.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS maintenancezone.maint_thresholds (
            tag VARCHAR(80),
            threshold INTEGER
        )
    """)
    # Insert the tag and threshold values into the table
    cursor.execute("""
        INSERT INTO maintenancezone.maint_thresholds (tag, threshold)
        VALUES (%s, %s), (%s, %s), (%s, %s)
    """, ("power output", power_output_threshold, "wind speed", wind_speed_threshold, "temperature", temperature_threshold))
# Commit the changes and close the connection
conn.commit()
conn.close()
