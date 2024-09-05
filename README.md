# StreamTape Video Downloader

This project is a **web scraper** designed to scrape and download videos from *StreamTape*. It utilizes **Selenium** for scraping, **Joblib** for parallelization, and **Requests** for downloading the video files. The scraper is capable of handling multiple videos in parallel and efficiently downloading them to your system.


## Features

- **Parallel Downloading**: The scraper can download multiple videos simultaneously using Joblib, optimizing performance.
- **Video Storage**: Downloaded videos are saved in the `videos/` folder, with file names extracted from the webpage.
- **Error Handling**: Robust error handling ensures the script retries downloading if it encounters errors.

## Project Structure

├── `scraper.py` \
   **Main script for scraping and downloading StreamTape videos (single-threaded).**\
├── `scraper_parallel.py` \
   **Parallelized script for scraping and downloading multiple StreamTape videos concurrently.**

### Steps to Run the Project

1. **Clone the repository:**

```bash
git clone https://github.com/dr-pandit-69/streamtape-video-downloader
cd streamtape-video-downloader
```

2. **Create a virtual environment (using pipenv for dependency management):**

```bash
pipenv shell
```

3. **Install the dependencies:**

```bash
pip install -r requirements.txt

```


4.**Prepare the environment:**
Make sure you have Google Chrome installed (version 115 or higher). You can specify the path to Chrome WebDriver if needed. Adjust the environment variables in the .env file if necessary.

5.**Provide the URLs to download:**
Ensure your links.txt file contains the StreamTape video URLs (one URL per line). The scraper will read this file to fetch and download the videos.


1. **Run the Video Downloader:**

If you want to download videos one at a time, run the following command:

```bash
python3 scraper.py
```

If you have a more powerful machine and want to download multiple videos concurrently, use the parallelized script:

```bash
python3 scraper_parallel.py
```





