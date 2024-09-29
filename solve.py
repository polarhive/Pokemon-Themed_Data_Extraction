from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import csv

# Function to extract financial stats
def part_1(soup):
    stats = {}

    # Find the container with financial ratios
    ratios_container = soup.find('div', class_='company-ratios')

    # Iterate through each <li> item within the <ul>
    for li in ratios_container.find_all('li', class_='flex flex-space-between'):
        # Extract the name and value
        name = li.find('span', class_='name').text.strip()
        value = li.find('span', class_='nowrap value').text.strip()

        # Clean and format the value
        if name == "Market Cap":
            value_parts = value.split()
            formatted_value = f"{value_parts[0]} {value_parts[1]}"  # Keep ₹ and the number together
        elif name == "Current Price":
            value_parts = value.split()
            formatted_value = f"{value_parts[0]} {value_parts[1]}"  # Keep ₹ and the number together
        elif name == "ROCE":
            value_parts = value.split()
            formatted_value = f"{value_parts[0]}%"  # Just append the percent sign
        elif name == "ROE":
            value_parts = value.split()
            formatted_value = f"{value_parts[0]}%"  # Just append the percent sign
        else:
            formatted_value = value  # Default case

        # Store relevant stats
        if name in ["Market Cap", "Current Price", "Stock P/E", "ROCE", "ROE"]:
            stats[name] = formatted_value

    return stats

def get_company_stats(driver, company_name):
    search_button = driver.find_element(By.CLASS_NAME, "search-button")
    search_button.click()
    time.sleep(1)  # Wait for the search box to appear

    # Locate the search input field, clear it, and input the company name
    search_box = driver.find_element(By.XPATH, "//input[@aria-label='Search for a company']")
    search_box.clear()
    search_box.send_keys(company_name)  # Type the company name
    time.sleep(1)  # Wait for suggestions to load
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    financial_stats = part_1(soup)
    return financial_stats

def save_to_csv(data, filename='Basic_Pokemon_Stats.csv'):
    company_order = [
        "Voltas",
        "Havells",
        "Blue Star",
        "Whirlpool",
        "Crompton",
        "Symphony",
        "Orient Electric"
    ]

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Stock Name", "Market Cap (in Cr)", "Current Price", "Stock P/E", "ROCE", "ROE"])

        # Write data
        for company in company_order:
            if company in data:
                stats = data[company]
                writer.writerow([
                    company,
                    stats.get("Market Cap", ""),
                    stats.get("Current Price", ""),
                    stats.get("Stock P/E", ""),
                    stats.get("ROCE", ""),
                    stats.get("ROE", "")
                ])
            else:
                # If stats not found for this company, write empty values
                writer.writerow([company, "", "", "", "", ""])

driver = webdriver.Chrome()

# Start from the Voltas SEED URL
url = "https://www.screener.in/company/VOLTAS/consolidated/"
driver.get(url)

time.sleep(1)

companies = {
    "Voltas": "VOLTAS",
    "Blue Star": "BLUESTARCO",
    "Crompton": "CROMPTON",
    "Orient Electric": "ORIENTELEC",
    "Havells": "HAVELLS",
    "Symphony": "SYMPHONY",
    "Whirlpool": "WHIRLPOOL"
}

all_company_stats = {}

for company_name in companies.keys():
    company_name = company_name.strip()  # Ensure no trailing/leading spaces
    stats = get_company_stats(driver, company_name)
    all_company_stats[company_name] = stats  # Store the stats for this company
    print(f"\nFinancial stats for {company_name}:\n")
    for stat_name, value in stats.items(): print(f"{stat_name}: {value}")

save_to_csv(all_company_stats)

driver.quit()
print("\nData has been saved to Basic_Pokemon_Stats.csv")