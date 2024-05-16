import requests
import time

def format_loading_time(loading_time):
    if loading_time < 1:
        return f"{int(loading_time*1000)} ms"
    elif loading_time < 10:
        return f"{loading_time:.1f} sec"
    else:
        return f"{loading_time:.1f} seconds"

def is_url_live(url):
    # Ensure the URL starts with http:// or https://
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    try:
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        print(response)
        # Return True if the status code is 200 (OK)
        # return response.status_code == 200
        loading_time = end_time - start_time
        return format_loading_time(loading_time)
    except requests.exceptions.RequestException:
        # Catch any exception (connection error, timeout, etc.)
        return False

# Example usage:
url = "google.com"
print(is_url_live(url))  # Output: True if live, False otherwise
