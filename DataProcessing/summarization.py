from openai import OpenAI
import pdfplumber
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Import openai, not OpenAI

messages = [
    {"role" : "System" , "Content" : "Just reply bro"},
    {"role" : 'user', "Content" : "Hello How are you"}
]

# Table of Contents from the previous step
table_of_contents = [
    [
        {"topic": "Summary of our 2023 results and the principles that guide us", "page": 4},
        {"topic": "Steadfast principles worth repeating (and one new one)", "page": 7},
        {"topic": "Mapping our progress and milestones", "page": 8},
        {"topic": "Celebrating the 20th anniversary of the Bank One/JPMorgan Chase merger", "page": 9},
        {"topic": "Financial performance", "page": 11},
        {"topic": "The critical impact of artificial intelligence", "page": 19},
        {"topic": "Our journey to the cloud", "page": 20},
        {"topic": "Acquiring First Republic Bank and its customers", "page": 20},
        {"topic": "Navigating in a complex and potentially dangerous world", "page": 21},
        {"topic": "Our extensive community outreach efforts, including diversity, equity and inclusion", "page": 23},
        {"topic": "What we learned: A five-point action plan to move forward on the climate challenge", "page": 28},
        {"topic": "Powering economic growth in Florida", "page": 30},
        {"topic": "Giving the bank regulatory and supervisory process a serious review", "page": 32},
        {"topic": "Protecting the essential role of market making (trading)", "page": 35},
        {"topic": "The pressure of quarterly earnings compounded by bad accounting and bad decisions", "page": 38},
        {"topic": "The hijacking of annual shareholder meetings", "page": 38},
        {"topic": "The undue influence of proxy advisors", "page": 39},
        {"topic": "The benefits and risks of private credit", "page": 40},
        {"topic": "A bank’s strength: Providing flexible capital", "page": 41},
        {"topic": "Benefiting from the OODA loop", "page": 42},
        {"topic": "Decision making and acting (have a process)", "page": 43},
        {"topic": "The secret sauce of leadership (have a heart)", "page": 44},
        {"topic": "Coalescing the Western world – A uniquely American task", "page": 46},
        {"topic": "Strengthening our position with a comprehensive, global economic security strategy", "page": 47},
        {"topic": "Providing strong leadership globally and effective policymaking domestically", "page": 49},
        {"topic": "Manager’s Journal: A Politician’s Dream Is a Businessman’s Nightmare", "page": 52},
        {"topic": "Out of the labyrinth, with focus and resolve", "page": 57},
        {"topic": "We should have more faith in the amazing power of our freedoms", "page": 58},
        {"topic": "How we can help lift up our low-income citizens and mend America’s torn social fabric", "page": 59}
    ],
    [
        {"topic": "Consumer & Community Banking", "page": 1},
        {"topic": "Commercial & Investment Bank", "page": 6},
        {"topic": "Asset & Wealth Management", "page": 14},
        {"topic": "Corporate Responsibility", "page": 17},
    ],
    [
        {"topic": "Three-Year Summary of Consolidated Financial Highlights", "page": 1},
        {"topic": "Five-Year Stock Performance", "page": 2},
        {"topic": "Introduction", "page": 3},
        {"topic": "Executive Overview", "page": 4},
        {"topic": "Consolidated Results of Operations", "page": 9},
        {"topic": "Consolidated Balance Sheets and Cash Flows Analysis", "page": 13},
        {"topic": "Explanation and Reconciliation of the Firm's Use of Non-GAAP Financial Measures", "page": 17},
        {"topic": "Business Segment Results", "page": 20},
        {"topic": "Firmwide Risk Management", "page": 41},
        {"topic": "Strategic Risk Management", "page": 45},
        {"topic": "Capital Risk Management", "page": 46},
        {"topic": "Liquidity Risk Management", "page": 57},
        {"topic": "Credit and Investment Risk Management", "page": 66},
        {"topic": "Market Risk Management", "page": 90},
        {"topic": "Country Risk Management", "page": 99},
        {"topic": "Climate Risk Management", "page": 101},
        {"topic": "Operational Risk Management", "page": 102},
        {"topic": "Critical Accounting Estimates Used by the Firm", "page": 110},
        {"topic": "Accounting and Reporting Developments", "page": 114},
        {"topic": "Forward-Looking Statements", "page": 116},
        {"topic": "Management’s Report on Internal Control Over Financial Reporting", "page": 117},
        {"topic": "Report of Independent Registered Public Accounting Firm", "page": 118},
        {"topic": "Consolidated Financial Statements", "page": 121},
        {"topic": "Notes to Consolidated Financial Statements", "page": 126},
        {"topic": "Distribution of Assets, Liabilities, and Stockholders' Equity; Interest Rates and Interest Differentials", "page": 265},
        {"topic": "Glossary of Terms and Acronyms", "page": 270}
    ]
]

# Function to extract text between pages
def extract_text_between_pages(pdf_path, start_page, end_page):
    extracted_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in range(start_page-1, end_page):  # Convert 1-based index to 0-based index
            page = pdf.pages[page_num]
            extracted_text += page.extract_text() + "\n"
    return extracted_text

# Function to summarize text using GPT-3.5 Turbo
def summarize_text(text):
    # te = [ {"role": "system", "content": 
    #           "You are a intelligent assistant."} ]
    # text.append(
    #     {"role": "user", "content": text}
    # )
    # chat = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo", messages=text
    # )
    # reply = chat.choices[0].message.content
    # text.append({"role": "assistant", "content": reply})
    # return reply
    chat_completion = client.chat.completions.create(
    messages=[
        {"role" : "system" , "content" : "Hi, Can you summarize this please, keep the financial terms well structured and include as many as possible but make sure it is also simple adn easy for shareholders to read "},
        {"role" : 'user', "content" : text}
    ],
    model="gpt-4o-mini",
    temperature=0.7,
    max_tokens=350
    )

    return chat_completion.choices[0].message.content
    

# Main function to handle the process
def summarize_topic_by_index(pdf_path, topic_index, topic_part):
    # Get the topic and the next topic's page number
    current_section = table_of_contents[topic_part -1]

    current_topic = current_section[topic_index]
    start_page = current_topic["page"]
    
    # If it's the last topic, extract until the end of the document
    if topic_index + 1 < len(current_section):
        next_topic = current_section[topic_index + 1]
        end_page = next_topic["page"]   # Get the page before the next topic
    else:
        # Extract until the end if it's the last topic
        end_page = 279  # Adjust to end of the PDF manually
    
    # Extract text between the topic pages
    extracted_text = extract_text_between_pages(pdf_path, start_page, end_page)
    # Summarize the extracted text
    summary = summarize_text(extracted_text)
    
    return summary


def getPdfName(topicPart):

    if topicPart == 1: 
        return "pdfData/Part_1.pdf"  # Path to your PDF file
    elif topic_part == 2:
        return  "pdfData/part_2.pdf"  # Path to your PDF file
    elif topic_part == 3:
        return "pdfData/part_3.pdf"  # Path to your PDF file
# Example usage:

# topic_index = 2  # Index of the topic you want to summarize
# topic_part = 2
# pdf_path = getPdfName(topic_part)
# summary = summarize_topic_by_index(pdf_path, topic_index, topic_part)
