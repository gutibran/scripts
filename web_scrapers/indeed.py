# scrape job postings to determine what skills are in demand by potential employers
# create web visualizations on map, allow users to filter by industry, job title, etc.abs
# search keywords, have no idea if this will work
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("hi")