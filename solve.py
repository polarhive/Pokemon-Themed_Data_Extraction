from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import csv

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

def A(soup):
    stats = {}
    ratios_container = soup.find('div', class_='company-ratios')
    for li in ratios_container.find_all('li', class_='flex flex-space-between'):
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

def search(driver, company_name):
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

    financial_stats = A(soup)
    return financial_stats

def A_save_to_csv(data, filename='Basic_Pokemon_Stats.csv'):
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

def part_2(soup):
    balance_sheet = {
        "Reserves": None,
        "Borrowings": None,
        "Total Liabilities": None,
        "Fixed Assets": None,
        "Investments": None,
        "Total Assets": None
    }

    # Find the balance sheet section
    balance_sheet_section = soup.find('section', id='balance-sheet')

    if not balance_sheet_section:
        print("Balance sheet section not found.")
        return balance_sheet  # Return empty if no section found

    print("Balance sheet section found.")

    # Find the balance sheet table within the section
    table = balance_sheet_section.find('table', class_='data-table')

    if not table:
        print("No balance sheet table found.")
        return balance_sheet  # Return empty if no table found

    print("Balance sheet table found.")

    # Iterate through each row in the table
    for row in table.find_all('tr'):
        cells = row.find_all('td')

        if len(cells) > 1:  # Ensure it's a data row with values

            # Extract Reserves
            if "Reserves" in row.text:
                mar_2024_value = cells[-1].text.strip().replace(',', '')  # Get the last value
                balance_sheet["Reserves"] = mar_2024_value
                print(f"Reserves found: March 2024 Value: {mar_2024_value}")

            # Extract Borrowings
            if "Borrowings" in row.text:
                mar_2024_value = cells[-1].text.strip().replace(',', '')  # Get the last value
                balance_sheet["Borrowings"] = mar_2024_value
                print(f"Borrowings found: March 2024 Value: {mar_2024_value}")

            # Extract Total Liabilities
            if "Total Liabilities" in row.text:
                mar_2024_value = cells[-1].text.strip().replace(',', '')  # Get the last value
                balance_sheet["Total Liabilities"] = mar_2024_value
                print(f"Total Liabilities found: March 2024 Value: {mar_2024_value}")

            # Extract Fixed Assets
            if "Fixed Assets" in row.text:
                mar_2024_value = cells[-1].text.strip().replace(',', '')  # Get the last value
                balance_sheet["Fixed Assets"] = mar_2024_value
                print(f"Fixed Assets found: March 2024 Value: {mar_2024_value}")

            # Extract Investments
            if "Investments" in row.text:
                mar_2024_value = cells[-1].text.strip().replace(',', '')  # Get the last value
                balance_sheet["Investments"] = mar_2024_value
                print(f"Investments found: March 2024 Value: {mar_2024_value}")

            # Extract Total Assets
            if "Total Assets" in row.text:
                mar_2024_value = cells[-1].text.strip().replace(',', '')  # Get the last value
                balance_sheet["Total Assets"] = mar_2024_value
                print(f"Total Assets found: March 2024 Value: {mar_2024_value}")

    return balance_sheet

def B_get_balance_sheet_data():
    # Click on the Balance Sheet tab
    balance_sheet_button = driver.find_element(By.XPATH, "//a[@href='#balance-sheet']")
    balance_sheet_button.click()
    time.sleep(2)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    balance_sheet_data = part_2(soup)

    return balance_sheet_data

def B_save_balance_sheet_to_csv(data, filename='Balance_Sheet_Data.csv'):
    stock_names = ["Voltas", "Havells", "Blue Star", "Whirlpool", "Crompton", "Symphony", "Orient Electric"]
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Stock Name", "Year", "Reserves", "Borrowings", "Total Liabilities", "Fixed Assets", "Investments", "Total Assets"])
        for stock in stock_names:
          writer.writerow([stock, 2024, data["Reserves"], data["Borrowings"], data["Total Liabilities"], data["Fixed Assets"], data["Investments"], data["Total Assets"]])

#############

def C_extract_profit_loss_data(soup):
    profit_loss = {
        "Sales": [],
        "Net Profit": [],
        "OPM": [],
        "EPS": [],
    }

    profit_loss_section = soup.find('section', id='profit-loss')
    if not profit_loss_section:
        return profit_loss  # Return empty if no section found
    table = profit_loss_section.find('table', class_='data-table')

    if not table:
        return profit_loss  # Return empty if no table found

    last_three_years_data = {}

    # Iterate through each row in the table
    for row in table.find_all('tr'):
        cells = row.find_all('td')

        if len(cells) > 1:  # Ensure it's a data row with values
            if "Sales" in row.text:
                last_three_years_data["Sales"] = [cell.text.strip().replace(',', '') for cell in cells[-4:-1]]
                print(f"Sales found: {last_three_years_data['Sales']}")

            if "Net Profit" in row.text:
                last_three_years_data["Net Profit"] = [cell.text.strip().replace(',', '') for cell in cells[-4:-1]]
                print(f"Net Profit found: {last_three_years_data['Net Profit']}")

            if "OPM" in row.text:
                last_three_years_data["OPM"] = [cell.text.strip().replace(',', '') for cell in cells[-4:-1]]
                print(f"OPM found: {last_three_years_data['OPM']}")
            if "EPS" in row.text:
                last_three_years_data["EPS"] = [cell.text.strip().replace(',', '') for cell in cells[-4:-1]]
                print(f"EPS found: {last_three_years_data['EPS']}")

    return last_three_years_data

def C_get_profit_loss_data():
    profit_loss_button = driver.find_element(By.XPATH, "//a[@href='#profit-loss']")
    profit_loss_button.click()
    time.sleep(2)  # Wait for the profit & loss to load

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    profit_loss_data = C_extract_profit_loss_data(soup)
    return profit_loss_data

def C_save_profit_loss_to_csv(data, filename='Profit_Loss_Data.csv'):
    # Define the header for the CSV file
    header = ["Stock Name", "Year", "Sales", "Net Profit", "OPM", "EPS"]

    # Prepare the data to be written to CSV
    stock_names = ["Voltas", "Havells", "Blue Star", "Whirlpool", "Crompton", "Symphony", "Orient Electric"]
    years = [2022, 2023, 2024]

    # Create a list to hold the rows for the CSV
    rows = []

    # Iterate through each stock name and corresponding years
    for stock in stock_names:
        for year in years:
            sales = data.get("Sales", ["", "", ""])[years.index(year)] if year in years else ""
            net_profit = data.get("Net Profit", ["", "", ""])[years.index(year)] if year in years else ""
            opm = data.get("OPM", ["", "", ""])[years.index(year)] if year in years else ""
            eps = data.get("EPS", ["", "", ""])[years.index(year)] if year in years else ""

            rows.append([stock, year, sales, net_profit, opm, eps])

    # Write the data to the CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write the header
        writer.writerows(rows)    # Write the data rows


####

driver = webdriver.Chrome()
def setup():
    # Start from the Voltas SEED URL
    url = "https://www.screener.in/company/VOLTAS/consolidated/"
    driver.get(url)
    time.sleep(1)

    for company_name in companies.keys():
        company_name = company_name.strip()  # Ensure no trailing/leading spaces
        stats = search(driver, company_name)
        all_company_stats[company_name] = stats  # Store the stats for this company
        print(f"\nFinancial stats for {company_name}:\n")
        for stat_name, value in stats.items(): print(f"{stat_name}: {value}")
    A_save_to_csv(all_company_stats)
    print("\nData has been saved to Basic_Pokemon_Stats.csv")

    #Start from the Voltas SEED URL
    url = "https://www.screener.in/company/VOLTAS/consolidated/"
    driver.get(url)
    time.sleep(1)

    for company_name in companies.keys():
        company_name = company_name.strip()  # Ensure no trailing/leading spaces
        stats = search(driver, company_name)
        B_save_balance_sheet_to_csv(B_get_balance_sheet_data())
        print("\nBalance sheet data has been saved to Balance_Sheet_Data.csv")

   # Start from the Voltas SEED URL
    url = "https://www.screener.in/company/VOLTAS/consolidated/"
    driver.get(url)
    time.sleep(1)

    for company_name in companies.keys():
        company_name = company_name.strip()  # Ensure no trailing/leading spaces
        search(driver, company_name)
        C_save_profit_loss_to_csv(C_get_profit_loss_data())
        print("\nProfit and loss data has been saved to Profit_Loss_Data.csv")

setup()
driver.quit()
