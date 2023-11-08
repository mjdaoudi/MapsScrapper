# **Web Scraping and Email Extraction Script for Maps**

This README provides information and instructions for the Python script designed to scrape data from maps and extract email addresses from scrapped websites. The script is intended for users who want to collect business information and associated email addresses from a specific website and save the results in a CSV file. The script uses Python, the Pandas library for data manipulation, and a custom library for web scraping and email extraction.

## **Prerequisites**

Before using the script, make sure you have the following prerequisites:

1. Python: The script is written in Python. You can download Python from [python.org](https://www.python.org/downloads/) and install it.

2. Required Python libraries: You need to install the following Python libraries if you haven't already. You can install them using pip, a package manager for Python.

   ```
   pip install requirements.txt
   ```

## **Usage**

Follow these steps to use the script:

1. Import the necessary libraries and set up the logging level in the script.

2. Specify the `regions` and `business_types` as the regions and business types you want to search for. The script will generate combinations of these values and scrape data for each combination. Download the right chromedriver according to your system and specify the path in the `main()`.

3. Run the `main()` function by checking if the script is the main module. This function will perform the following steps:

   a. Start the web scraping process for each combination of `regions` and `business_types`.

   b. Collect data from the website, add region and business type information to the collected data, and store it in the `leads` list.

   c. Export the collected data to a CSV file named "adresses.csv" and include the website information in a standardized format.

   d. Analyze the websites to extract email addresses and append the results to the data.

   e. Export the final data, including email addresses, to a CSV file named "adresses_complete.csv."

4. Execute the script using the command `python main.py`.

## **Drivers**

**Selenium uses Chromedrivers in the background to interact with chrome. Please [download](https://googlechromelabs.github.io/chrome-for-testing/) the right version according to your system.**

## **Logging**

The script uses logging to report its progress and any encountered errors. You can find log entries in the console or log files, depending on your configuration.

## **Disclaimer**

Please be aware of the legal and ethical implications of web scraping. Ensure that you have the necessary permissions and are complying with the website's terms of service and applicable laws before using this script to scrape data.
