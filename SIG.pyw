import tkinter as tk
from tkinter import Entry, Label, Button, Text, Menu
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse

def clean_url(url):
    parsed_url = urlparse(url)
    cleaned_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
    return cleaned_url

def search_game():
    search_term = entry.get()
    search_url = f"https://store.steampowered.com/search/?term={search_term}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Get the first game link from the search results and clean it
    game_link = clean_url(soup.find('a', class_='search_result_row')['href'])
    
    # Fetch game details from the game link
    game_response = requests.get(game_link)
    game_soup = BeautifulSoup(game_response.content, 'html.parser')
    
    # Extract game description and header image
    description = game_soup.find('div', class_='game_description_snippet').text.strip()
    header_img_link = game_soup.find('img', class_='game_header_image_full')['src']
    
    # Download header image
    img_response = requests.get(header_img_link)
    with open('header.jpg', 'wb') as file:
        file.write(img_response.content)
    
    # Display results in the GUI with a line break before the URL
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, description + '\n\n' + game_link)

def copy_text(event):
    # Copy the text in the result box to the clipboard
    root.clipboard_clear()
    root.clipboard_append(result_text.get(1.0, tk.END))

# Create the main window
root = tk.Tk()
root.title("Steam Game Finder")

# Create and place widgets
Label(root, text="Enter Game Name:").pack(pady=10)
entry = Entry(root, width=50)
entry.pack(pady=10)
Button(root, text="Search", command=search_game).pack(pady=10)
result_text = Text(root, width=60, height=10)
result_text.pack(pady=10)

# Add right-click context menu to copy text
context_menu = Menu(root, tearoff=0)
context_menu.add_command(label="Copy", command=lambda: copy_text(None))
result_text.bind("<Button-3>", lambda event: context_menu.post(event.x_root, event.y_root))
result_text.bind("<Control-c>", copy_text)

root.mainloop()
