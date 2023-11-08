import logging
from itertools import product

import numpy as np
import pandas as pd

from src.Mailanalyzer import extract_emails_from_websites
from src.Scrapper import WebDriver

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

CHROME_DRIVER_PATH = "/Users/mjdaoudi/Development/MapsScrapper/chromedriver"

def main() -> None:
    url = "https://www.google.com/maps"
    leads = []
    regions = ["brussels"]
    business_types = ["restaurant", "traiteur", "hotel", "centre sport"]
    for region, business_type in product(regions, business_types):
        logging.info(f"Scrapping {business_type} in {region}")
        try:
            Scrapper = WebDriver(CHROME_DRIVER_PATH=CHROME_DRIVER_PATH)
            data = Scrapper.scrape(url, f"{business_type} in {region}")
            data = list(
                map(
                    lambda item: {
                        **item,
                        "region": region,
                        "Business Type": business_type,
                    },
                    data,
                )
            )
            leads.extend(data)
        except Exception as e:
            logging.error(e)
            pass
    logging.info("Exporting the results")
    leads = pd.DataFrame(leads)
    leads["website"] = leads["website"].apply(
        lambda site: "https://www." + str(site) if pd.notna(site) else np.nan
    )
    leads.to_csv("data/adresses.csv", index=False)
    logging.info("Analysing mails")
    leads = extract_emails_from_websites(leads)
    leads.to_csv("data/adresses_complete.csv", index=False)


if __name__ == "__main__":
    main()
