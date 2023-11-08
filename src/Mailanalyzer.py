import logging
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

regex = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


def extract_emails_from_websites(df):
    # List to store the extracted emails
    email_list = []

    # Iterate over the DataFrame rows using itertuples()
    y = len(df)
    x = 1
    for row in df.itertuples():
        logging.info(f"{x}/{y} site done")
        url = getattr(row, "website")
        if pd.notna(url):
            try:
                ua = UserAgent()
                headers = {"User-Agent": ua.random}
                # Send a GET request
                res = requests.get(url, headers=headers, timeout=5)
                res.raise_for_status()  # Raise exception if the GET request was unsuccessful
                # Parse the HTML content
                soup = BeautifulSoup(res.text, "html.parser")

                # Remove cookie banners
                for element in soup(["script", "style"]):
                    element.decompose()

                # Extract email addresses
                emails = re.findall(regex, soup.get_text())

                # Flatten the list of emails and append it to the list
                email_list.append(emails)

            except requests.exceptions.RequestException as e:
                logging.warn(
                    f"An error occurred while making the request to {url}: {e}"
                )
                email_list.append(None)
                continue

            except Exception as e:
                logging.warn(
                    f"An error occurred while parsing the HTML content of {url}: {e}"
                )
                email_list.append(None)
        else:
            email_list.append(None)
        x += 1

    # Add the emails to the DataFrame
    df["email"] = email_list
    df = df.explode("email")
    df.drop_duplicates(
        subset=["name", "Business Type", "email"], keep="first", inplace=True
    )

    return df
