import os
import chromedriver_handler
from joblib import Parallel, delayed
from dotenv import load_dotenv
from scraper import setup_driver, download_video, read_links_from_file,get_download_link

load_dotenv()
chromedriver_handler.setup_chromedriver()


PARALLEL_INSTANCES =  int(os.getenv('PARALLEL_INSTANCES', 4))


def process_url(url):
    driver = setup_driver()
    try:
        file_name, video_url = get_download_link(driver, url)
        if video_url:
            download_video(video_url, file_name)
    finally:
        driver.quit()  


def main():
    links = read_links_from_file('links.txt')  

    Parallel(n_jobs=PARALLEL_INSTANCES)(delayed(process_url)(url) for url in links)

if __name__ == "__main__":
    main()
