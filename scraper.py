from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import os
import chromedriver_handler
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform



def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-minimized")

    # Detect the operating system and set the path accordingly
    if platform.system() == "Windows":
        service = Service(executable_path="driver/chromedriver.exe")
    else :  
        service = Service(executable_path="driver/chromedriver")
    

    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def download_video(url, filename):
   
    if not os.path.exists('videos'):
        os.makedirs('videos')

   
    file_path = os.path.join('videos', filename)

    try:
        print(f"Downloading: {filename}")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Download complete: {file_path}")
        else:
            print(f"Failed to download: {url}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

def close_popups(driver):
    """ Close any unwanted tabs or pop-ups that open. """
    
    main_window = driver.current_window_handle
    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            driver.close()
    driver.switch_to.window(main_window)

def keep_clicking_until_video_plays(driver, streamtape_url):
    driver.set_window_position(2000, 100)
    driver.minimize_window()
    driver.get(streamtape_url)
    time.sleep(3) 
    
    attempts = 0
    video_found = False
    max_attempts = 100 
    while attempts < max_attempts:
        try:
          
            overlay = driver.find_element(By.CLASS_NAME, "play-overlay")
            driver.execute_script("arguments[0].click();", overlay)
            print(f"Overlay clicked on attempt {attempts+1}")

        except Exception:
            print(f"Overlay not found or already clicked on attempt {attempts+1}")

        try:
           
            play_button = driver.find_element(By.CLASS_NAME, "plyr__control--overlaid")
            driver.execute_script("arguments[0].click();", play_button)
            print(f"Play button clicked on attempt {attempts+1}")

            
            video_player = driver.find_element(By.TAG_NAME, 'video')
            video_url = video_player.get_attribute('src')
            if video_url:
                print(f"Video found and playing on attempt {attempts+1}")
                video_found = True
                break
        except Exception:
            print(f"Play button or video not found on attempt {attempts+1}")
        
       
        close_popups(driver)
        
        attempts += 1
        time.sleep(0.25) 
    
    if video_found:
        return True  
    else:
        print(f"Failed to start video after {attempts} attempts.")
        return False

def get_download_link(driver: webdriver.Chrome, streamtape_url):
    driver.set_window_position(2000, 100)
    driver.minimize_window()
    driver.get(streamtape_url)
    try:
      
        if not keep_clicking_until_video_plays(driver, streamtape_url):
            return None, None

        
        time.sleep(5)  

        h2_element = driver.find_element(By.TAG_NAME, "h2")
        file_name = h2_element.text.strip()
        print(f"File Name Found: {file_name}")

        video_player = driver.find_element(By.TAG_NAME, 'video')
        video_url = video_player.get_attribute('src')
        print(f"Download Link Found: {video_url}")

        return file_name, video_url

    except Exception as e:
        print(f"Error extracting file name or download link from {streamtape_url}: {e}")
        return None, None


def read_links_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            
            return [line.strip() for line in file.readlines() if line.strip()]
    else:
        print(f"{file_path} does not exist.")
        return []

def main():
    driver = setup_driver()

    links = read_links_from_file('links.txt') 
    for i, link in enumerate(links, 1):
        print(f"Processing {i}/{len(links)}: {link}")
        file_name, video_url = get_download_link(driver, link)
        if video_url:
            
            download_video(video_url, file_name)
    
    
    driver.quit()

if __name__ == "__main__":
   
    chromedriver_handler.setup_chromedriver()

    main()
