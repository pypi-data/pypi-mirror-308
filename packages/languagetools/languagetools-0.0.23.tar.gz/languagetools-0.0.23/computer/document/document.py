"""

- Use CSS page-break-after: always; for page breaks.
- Set explicit height (e.g., height: 297mm; for A4) for full-page content.
- Example HTML structure for multi-page:

    <div style="page-break-after: always;">
        <!-- Content for page 1 -->
    </div>
    <div style="page-break-after: always;">
        <!-- Content for page 2 -->
    </div>
    
"""

import sys
import os
import base64
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def html_to_pdf(html_file, pdf_file):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Convert HTML to PDF
        print("Loading HTML...")
        driver.get(f"file://{os.path.abspath(html_file)}")
        print(f"Page title: {driver.title}")

        # Wait for the page to load (adjust the time if needed)
        time.sleep(2)

        # Wait for CSS to be applied
        print("Waiting for styles to be applied...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Additional wait to ensure all styles are applied
        time.sleep(3)

        print("Generating PDF...")
        # Use Chrome's built-in PDF printing
        print_options = {
            'landscape': False,
            'paperWidth': 210 / 25.4,  # A4 width in inches
            'paperHeight': 297 / 25.4,  # A4 height in inches
            'marginTop': 0,
            'marginBottom': 0,
            'marginLeft': 0,
            'marginRight': 0,
            'printBackground': True,  # Ensures background colors and images are included
            'scale': 0.98,  # Slightly reduce scale to ensure content fits
        }
        result = driver.execute_cdp_cmd("Page.printToPDF", print_options)

        # Save the PDF
        with open(pdf_file, "wb") as f:
            f.write(base64.b64decode(result['data']))

        print(f"PDF saved as {pdf_file}")

    finally:
        # Close the browser
        driver.quit()

    # Reveal the PDF in Finder
    os.system(f"open -R '{pdf_file}'")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python html_to_pdf.py <input_html_file> <output_pdf_file>")
        sys.exit(1)

    input_html = sys.argv[1]
    output_pdf = sys.argv[2]

    html_to_pdf(input_html, output_pdf)
    print("Conversion completed successfully.")
