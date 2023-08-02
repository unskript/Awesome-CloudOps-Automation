
import requests
from bs4 import BeautifulSoup

# The URL of the webpage you want to check
url = 'https://docs.unskript.com/unskript-product-documentation/guides/xrunbook_list'

# Send a GET request to the webpage
response = requests.get(url)
response.raise_for_status()  # Raise an exception if the GET request fails

# Parse the webpage's content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all hyperlinks in the webpage
for a in soup.find_all('a', href=True):
    link = a['href']

    # Ignore relative URLs
    if link.startswith(('http://', 'https://')):
        try:
            # Send a GET request to the hyperlink
            response = requests.get(link)
            
            # If the GET request fails, print the hyperlink
            if not response.ok:
                print('Dead link:', link)
                
        except requests.exceptions.RequestException:
            print('Dead link:', link)

