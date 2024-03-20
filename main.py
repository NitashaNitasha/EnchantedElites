import pandas as pd
from PIL import Image
import os
import google.generativeai as genai
import sqlite3

UPLOADS_FOLDER = 'uploads'

# Set up Generative AI API
genai.configure(api_key="AIzaSyAwgNVpn_iz6tMhxXb-hl1OUj7aqRvI1fc")  # Replace 'YOUR_API_KEY_HERE' with your actual API key

def main(filename):
    # Construct the full path to the image file
    image_path = os.path.join(UPLOADS_FOLDER, filename)

    # Check if the specified file exists
    if not os.path.isfile(image_path):
        print(f"The file '{filename}' does not exist in the 'uploads' folder.")
        return

    # Open the image file
    with Image.open(image_path) as image:
        # Convert image to RGBA format
        image = image.convert("RGBA")
        datas = image.getdata()

        # Process each pixel to remove white background
        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        # Apply modified data to image
        image.putdata(newData)

        # Save image without background
        image_no_bg_path = os.path.join(UPLOADS_FOLDER, filename + "_no_bg.png")
        image.save(image_no_bg_path, "PNG")
        fi=open("image_path.txt",'w')
        fi.write(image_no_bg_path)
        fi.close()

    # Set up Generative AI model and continue with your conversation and database operations...
    # This part of the code is unchanged

    print("Processing completed.")

def get_first_file(folder_path):
    # Get list of files in the folder
    files = os.listdir(folder_path)

    # Filter out directories and select the first file
    for file in files:
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            return file

    # Return None if no files are found
    return None

if __name__ == '__main__':
    first_file = get_first_file(UPLOADS_FOLDER)
    if first_file:
        main(first_file)
    else:
        print('No files found in the folder.')

def main(filename):
    # Construct the full path to the image file
    image_path = os.path.join(UPLOADS_FOLDER, filename)

    # Check if the specified file exists
    if not os.path.isfile(image_path):
        print(f"The file '{filename}' does not exist in the 'uploads' folder.")
        exit()

    # Open the image file
    with Image.open(image_path) as image:
        # Convert image to RGBA format
        image = image.convert("RGBA")
        datas = image.getdata()

        # Process each pixel to remove white background
        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        # Apply modified data to image
        image.putdata(newData)

        # Save image without background
        image_no_bg_path = os.path.join(UPLOADS_FOLDER, filename + "_no_bg.png")
        image.save(UPLOADS_FOLDER+"temp.PNG")

    # Set up Generative AI model
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]
    categories = [
        # List of categories omitted for brevity
    ]

    # Start a conversation with Generative AI model
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    convo = model.start_chat(history=[])
    convo.send_message(image_no_bg_path)
    # Send message to the model with the product classification
    items = [
        "Shoes",
        "Clothes",
        "Toys",
        "Food",
        
        "Electronics",
        "Tools",
        "Stationery",
        
        
        "Sports equipment",
        "Art supplies",
        "Gardening tools",
        
        
        
    ]

    convo.send_message("choose one correct classification of this product from " + ",".join(items))
    classify = convo.last.text
    
    convo.send_message("find the estimated price in dollars of the product.")

    # Store the responses
    
    color = convo.last.text

    # Start a new conversation to generate slang, trendy hashtags, and product description
    convo = model.start_chat(history=[])

    # Send message to the model with the product classification and color
    last_text = classify + color
    convo.send_message(last_text)
    convo.send_message(
        "on basis of above text generate a slang and trendy hashtags and description of the product of len 20")
    new_gen = convo.last.text

    # Save relevant information to files
    with open("classify.txt", 'w') as classify_file:
        classify_file.write(classify + '\n')
    with open("color.txt", 'w') as color_file:
        color_file.write(color + '\n')
    with open("new_gen.txt", 'w') as new_gen_file:
        new_gen_file.write(new_gen + '\n')


    import sqlite3

    try:
        db_connection = sqlite3.connect('example.db')
        cursor = db_connection.cursor()

        # Check if the table 'items' exists, if not, create it
        cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                classify TEXT NOT NULL,
                                color TEXT NOT NULL,
                                new_gen TEXT NOT NULL
                              )''')

        # Insert data into the database
        cursor.execute("INSERT INTO items (classify, color, new_gen) VALUES (?, ?, ?)", (classify, color, new_gen))
        db_connection.commit()
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        if db_connection:
            db_connection.close()

    print("Processing completed.")


if __name__ == '__main__':
    def get_first_file(folder_path):
        # Get list of files in the folder
        files = os.listdir(folder_path)

        # Filter out directories and select the first file
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                return file

        # Return None if no files are found
        return None

    folder_path = UPLOADS_FOLDER  # Replace 'path_to_your_folder' with the actual folder path
    first_file = get_first_file(folder_path)
    if first_file!=None:
        main(first_file)
    else:
        print('no file found')

