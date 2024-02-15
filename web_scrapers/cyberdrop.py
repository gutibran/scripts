from pathlib import Path
import sys
import os
import time
import sys
from datetime import datetime
import json
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def initialize_configuration() -> bool:
    """Set up files and directories for configuring the scripts."""
    script_directory_path = Path(__file__).resolve().parent
    config_directory_path = script_directory_path / "config"
    config_file_path = config_directory_path / "config.json"
    if config_directory_path.is_dir() and config_file_path.is_file():
        return True
    else:
        try:
            config_directory_path.mkdir(parents=True)
            config_file_path.touch()
        except Exception as exception:
            print(f"Exception: {exception}")
            return False
    with open(config_file_path, "w+") as json_file:
        config = {
            "default_save_path": f"{Path.home()}/Downloads",
        }
        json.dump(config, json_file, indent=2)
    return True

def get_configuration_paths() -> object:
    """Return the paths to the configuration directory and configuration file."""
    return {
        "configuration_directory_path": Path(__file__).resolve().parent / "config",
        "configuration_file_path": Path(__file__).resolve().parent / "config/config.json"
    }

def initialize_cache() -> bool:
    """Create the cache directory and file for the cache. Ensure that they exist."""
    script_directory_path = Path(__file__).resolve().parent
    cache_directory_path = script_directory_path / "cache"
    cache_file_path = cache_directory_path / "cache.json"
    if cache_directory_path.is_dir() and cache_file_path.is_file():
        return True
    else:
        try:
            cache_directory_path.mkdir(parents=True)
            cache_file_path.touch()
        except Exception as exception:
            print(f"Exception: {exception}")
            return False
    with open(cache_file_path, "w+") as json_file:
        cache = {
            "cyberdrop": {
                "history": [],
                "data": []
            }
        }
        json.dump(cache, json_file, indent=2)
    return True

def get_cache_paths():
    return {
        "cache_directory_path": Path(__file__).resolve().parent / "cache",
        "cache_file_path": Path(__file__).resolve().parent / "cache/cache.json"
    }

def album_has_been_scraped(url) -> bool:
    """Determine if an album has been scraped."""
    cache_paths = get_cache_paths()
    with open(cache_paths["cache_file_path"], "r") as json_file:
        cache = json.load(json_file)
        scrapes = cache["cyberdrop"]["data"]
        for scrape in scrapes:
            if scrape["url"] == url:
                return True
        return False
    
def find_links(url):
    cache_paths = get_cache_paths()
    with open(cache_paths["cache_file_path"], "r") as json_file:
        cache = json.load(json_file)
        for link in cache["cyberdrop"]["data"]:
            if link["url"] == url:
                return link
        return None

def find_file_links(url):
    cache_paths = get_cache_paths()
    with open(cache_paths["cache_file_path"], "r") as json_file:
        cache = json.load(json_file)
        scrapes = cache["cyberdrop"]["data"]
        for scrape in scrapes:
            if scrape["url"] == url:
                return scrape["file_urls"]

def scrape_album(url):
    """Scrape links from an album."""
    # check if we have been to this link before
    if not album_has_been_scraped(url):
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        response = requests.get(url)
        urls = [] 
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            image_links = soup.find_all("a", class_="image")
            for image_link in image_links:
                urls.append(base_url + image_link.get("href"))
        else:
            print("oh no")

        cache_paths = get_cache_paths()
        with open(cache_paths["cache_file_path"], "r+") as json_file:
            cache = json.load(json_file)
            cache["cyberdrop"]["history"].append(url)
            cache["cyberdrop"]["data"].append({
                "url": url,
                "urls": urls
            })
            json_file.seek(0)
            json.dump(cache, json_file, indent=2)
    else:
        print("no need to re-scrape, buddy")

def scrape_file_links(url):
    """Download the scraped links."""
    if not album_has_been_scraped(url):
        print("Nothing to do here buddy.")
    else:
        urls = find_links(url)["urls"]
        file_urls = []
        driver = webdriver.Firefox()
        for index, url in enumerate(urls):
            driver.get(url)
            time.sleep(10)
            element = driver.find_element(By.ID, "downloadBtn")
            href = element.get_attribute("href")
            print(f"[{index}]: {href}")
            file_urls.append(href)
        driver.quit()
    cache_paths = get_cache_paths()
    cache = None
    with open(cache_paths["cache_file_path"], "r+") as json_file:
        cache = json.load(json_file)

    with open(cache_paths["cache_file_path"], "w+") as json_file:
        index = None
        for i, scrape in enumerate(cache["cyberdrop"]["data"]):
            if scrape["url"] == url:
                index = i
                break
        cache["cyberdrop"]["data"][i]["file_urls"] = file_urls
        json.dump(cache, json_file, indent=2)

def download_files(url):
    if not album_has_been_scraped(url):
        print("Nothing to do here buddy.")
    else:
        # read in configuration file
        config_paths = get_configuration_paths() 
        download_base_path = None
        with open(config_paths["configuration_file_path"], "r") as configgern:
            download_base_path = json.load(configgern)["default_save_path"]

        # make directory to store the files in
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_directory = Path(f"{download_base_path}/{timestamp}")
        new_directory.mkdir(parents=True)
        urls = find_file_links(url)
        for index, url in enumerate(urls):
            response = requests.get(url)
            with open(f"{new_directory}/{index}", "wb") as image_file:
                image_file.write(response.content)
    

def main():
    url = input()
    scrape_album(url)
    scrape_file_links(url)
    download_files(url)

main()