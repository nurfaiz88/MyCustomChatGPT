'''
Project Name: PO Assistant
Prepared By: Mohd Nur Faiz B Abd Razak
GPT Mode: gpt-4o-mini
Project Workflow:
1. Import Required Frameworks
2. API key stored externally
3. Load API Keys from .env
4. Create kernal and model
5. Load pre-defined functions
'''


'''
Import Frameworks
'''
import os
import asyncio
import sqlite3
from faker import Faker
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.agents import ChatCompletionAgent

'''
Configure External Services - SQLite Database
'''
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create PO table
cursor.execute("""
CREATE TABLE IF NOT EXISTS PODETAIL (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    poNumber TEXT NOT NULL,
    vendorName TEXT NOT NULL,
    itemDescription TEXT NOT NULL,
    quantity TEXT NOT NULL,
    unitPrice TEXT NOT NULL,
    currency TEXT NOT NULL,
    totalAmount TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

conn.commit()
conn.close()



'''
Load faker, API Keys Create Kernel, Model, System Role Assignment
'''
load_ponumber = Faker()
load_dotenv()
kernel = Kernel()
chat_service = OpenAIChatCompletion(ai_model_id="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
kernel.add_service(chat_service)

agent = ChatCompletionAgent(service=chat_service, name="PO_Assistant", instructions="You are a purchase order expert.")
agent2 = ChatCompletionAgent(service=chat_service, name="AI_Expert", instructions="You are a purchase order expert and AI expert. You generate the python code with streamlit AI to show  executive report from passing JSON data if available. No instruction or comment, only code. Replace existing code. Check for errors and fix it")

'''
External PO Process
'''

# Function: To create PO
def create_po(order_details):
    '''
    Functional Specification:
    1. Dev: Using Hardcoded for testing
    2. Prd: Using API / DB
    '''    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO PODETAIL (poNumber, vendorName, itemDescription, quantity, unitPrice, currency, totalAmount, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (order_details['poNumber'], order_details['vendorName'], order_details['itemDescription'], order_details['quantity'], order_details['unitPrice'], order_details['currency'], order_details['totalAmount'], order_details['status']))
    conn.commit()
    conn.close()
    print(order_details)
    
    
    
    return f"PO created successfully. Here is the order details: {order_details}"

# For DELETE: DELETE FROM table WHERE CONDITION
# For UPDATE: UPDATE table SET COL=VAL WHERE COL=VAL


'''
Custom ChatGPT
'''

async def main():
    '''
    Functional Specification:
    
    '''
    print(f"Welcome to purchase order assistant. Type quit or exit if you are done.\n")
    
    while True:
        poassistant_userinput = input(f"PO User: ")
        poassistant_userinput = poassistant_userinput.lower()
        
        if poassistant_userinput in ['quit','exit']:
            print(f"Thank you for using PO assistant")
            break
        elif "create po" in poassistant_userinput:
            
            print(f"Yes i can help to create PO. I need more details information:")

            # Collection more input from user
            podetail_ponumber = f"PO-{load_ponumber.year()}-{load_ponumber.random_int(min=0, max=999999)}"
            podetail_vendorname = input(f"Vendor Name: ")
            podetail_itemdesc = input(f"Item Description: ")
            podetail_qty = int(input("Quantity: "))
            podetail_unitprice = float(input("Unit Price: "))
            podetail_currency = input(f"Currency (e.g: State Country Name or Currency): ")
            podetail_totalamount = podetail_qty * podetail_unitprice    
            
            # Generate final PO JSON Schema
            order_details = {
                "poNumber": podetail_ponumber,
                "vendorName": podetail_vendorname,
                "itemDescription": podetail_itemdesc,
                "quantity": podetail_qty,
                "unitPrice": podetail_unitprice,
                "currency": podetail_currency,
                "totalAmount": podetail_totalamount,
                "status": "CREATED"
            }
            
            # Calling function
            return_create_po = create_po(order_details)
            
            # GPT Conversation using Agent Framework
            response = await agent.get_response(messages=return_create_po)
            print("PO_Assistant:", response.content)
            
            response2 = await agent2.get_response(messages=return_create_po)
            with open("streamlitai.py", "w", encoding="utf-8") as f:
                f.write("\n" + str(response2) + "\n")
            
        else:
            
            # GPT Conversation using Agent Framework
            response = await agent.get_response(messages=poassistant_userinput)
            print("PO_Assistant:", response.content)
            
            
            
if __name__ == "__main__":
    asyncio.run(main())
            
