#all the modules
import speech_recognition as sr     #Voice recognizaion module 
import streamlit as st              #application des module
# import os                           #interaction with OS
import google.generativeai as genai         #Google API module
# import assemblyai as aai                  #assemlyai Module 
import pymysql                       #my sql 
from googletrans import Translator   #google API translator

from dotenv import load_dotenv
load_dotenv()                    ## load all the environemnt variables

#API KEYS
# aai.settings.api_key = "043b959beccb44bf8d2b08f6a836d457"
genai.configure(api_key='AIzaSyBr__M4c4oph-O17DEIIOidORQl9Xizdpw')

st.header("App To Retrieve SQL Data") #app
# Apply the background image
page_bg_img = """
<style>~
[data-testid="stAppViewContainer"] {
 background-image: url(https://img.freepik.com/free-vector/abstract-paper-style-background_52683-134881.jpg?size=626&ext=jpg);
 background-size: cover;
}
[data-testid="stHeader"] {
background-color: rgb(0, 0, 0 ,0);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


#Function To Load Google Gemini Model and provide queries as response
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')       #genrative ,model gemini pro
    response=model.generate_content([prompt[0],question])       #rquesting response
    return response.text 

## Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL queries!
The SQL database has the tables SALES and Products with the following columns:

For the SALES table:
- SaleID (INTEGER PRIMARY KEY)
- Date (DATE)
- CustomerID (INTEGER)
- EmployeeID (INTEGER)
- TotalAmount (NUMERIC(10, 2))

For the Products table:
- ProductID (INTEGER PRIMARY KEY)
- ProductName (VARCHAR(255))
- Description (TEXT)
- UnitPrice (NUMERIC(10, 2))
- QuantityInStock (INTEGER)

For example:
Example 1 - How many sales transactions were made in the last week?
The SQL command could resemble this:
SELECT COUNT(*) FROM SALES WHERE Date >= DATE_SUB(CURDATE(), INTERVAL 1 WEEK);

Example 2 - Retrieve all products with a unit price greater than $100.
The corresponding SQL query might be:
SELECT * FROM Products WHERE UnitPrice > 100;
also the sql code should not have ``` in beginning or end and sql word in output


    """


]



## Fucntion To retrieve query from the database
def read_sql_query(sql, text_to_sql):
    try:
        # Connect to the PYSQL database
        conn = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='text_to_sql')
        # Create a cursor
        cur = conn.cursor()
        st.write(sql)
        # Execute the SQL query
        cur.execute(sql)
        # Fetch all the rows
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    except pymysql.Error as e:
        st.write("Error connecting:", e)
        return None
    
# Translation from HINDI TO ENGLISH 
# Function to detect language using SpeechRecognition
def detect_language():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        st.write("Listening...")
        try:
            audio = r.listen(source, timeout=3)
            # Process the audio here
        except sr.WaitTimeoutError:
            print("Listening timed out.")
    
    try:
        detected_language = r.recognize_google(audio)  # Let Google API detect the language
        return detected_language
    except sr.UnknownValueError:
        return "Unable to detect language"
    except sr.RequestError as e:
        return f"Error: {e}"

# Function to translate text to English
def translate_to_english(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='en')
    return translated_text.text

# Main function
def main():
    detected_language = detect_language()
    if detected_language != "Unable to detect language":
        print("Detected Language:", detected_language)
        if detected_language != "en":  # If language detected is not English
            translated_text = translate_to_english(detected_language)
            print("Translated Text (to English):", translated_text)
            question=st.text_input("Input1:", key="input", value=translated_text)
            if question:
             st.write("querying....")
             response=get_gemini_response(question, prompt)
             print(response)
             response=read_sql_query(response,"storedb")
             st.subheader("The Response is")
             for row in response:
                stripped = str(row[0]).replace('(', '').replace(')', '').replace(',', '')
                print(row)
                st.header(stripped)
        else:
            st.write("Language is already English")
    else:
        st.write("Language detection failed")


if __name__ == "__main__":
    print("HINDI")
    submit=st.button("MIC")
    if submit:
        main()
    else:
        print("ENGLISH")  
        question=st.text_input("Input: ",key="input")                   #string for input for API
        submit=st.button("Ask the question")
# if submit is clicked
        if submit:
            response=get_gemini_response(question,prompt)
            st.write("querying....")
            st.write(response)
            print(response)
            response=read_sql_query(response,"storedb")
            st.subheader("The Response is")
            for row in response:
                stripped = str(row[0]).replace('(', '').replace(')', '').replace(',', '')
                print(row)
                st.header(stripped)