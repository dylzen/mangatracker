import file_ops
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def start_driver():
    print("Initializing webdriver...")
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    return driver

def get_data(user_input):
    driver = start_driver()
    print("Fetching data...")
    ratings = []
    members = []
    rankings = []
    popularities = []
    for item_link in file_ops.get_titles(user_input):
        print("Fetching: "+item_link)
        driver.get(item_link)
        wait = WebDriverWait(driver, 5)
        rating = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class*="score-label"]')))
        member = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span[class="numbers members"] strong')))
        ranking = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span[class="numbers ranked"] strong')))
        popularity = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span[class="numbers popularity"] strong')))
        ratings.append(rating.text)
        members.append(member.text)
        rankings.append(ranking.text)
        popularities.append(popularity.text)
    print("Stopping webdriver...")
    driver.stop_client()
    driver.close()
    driver.quit()
    print("Program stopped.")
    return user_input, ratings, members, rankings, popularities

def mal_write_to_xlsx(user_input):
    print("Writing data to excel file...")
    user_input, ratings, members, rankings, popularities = get_data(user_input)
    path, book = file_ops.load_book()
    sheet = book['Lista']
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

    sheet.cell(row=1, column=20, value="ratings_mal")           # column T
    for row_num, value in enumerate(ratings, start=2):
        sheet.cell(row=row_num, column=20, value=value)

    sheet.cell(row=1, column=21, value="members_MAL")           # column U
    for row_num, value in enumerate(members, start=2):
        sheet.cell(row=row_num, column=21, value=value)

    sheet.cell(row=1, column=22, value="ranking_MAL")           # column V
    for row_num, value in enumerate(rankings, start=2):
        sheet.cell(row=row_num, column=22, value=value)

    sheet.cell(row=1, column=23, value="popularity_MAL")        # column W
    for row_num, value in enumerate(popularities, start=2):
        sheet.cell(row=row_num, column=23, value=value)

    sheet.cell(row=1, column=25, value=timestamp)               # column Y

    book.save(path)


