import logging
from itertools import product

import numpy as np
import pandas as pd

from Mailanalyzer import extract_emails_from_websites
from Scrapper import WebDriver

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def main() -> None:
    url = "https://www.google.com/maps"
    leads = []
    regions = ["brussels"]
    business_types = ["restaurant", "traiteur", "hotel", "centre sport"]
    for region, business_type in product(regions, business_types):
        logging.info(f"Scrapping {business_type} in {region}")
        try:
            Scrapper = WebDriver()
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
    leads.to_csv("adresses.csv", index=False)
    logging.info("Analysing mails")
    leads = extract_emails_from_websites(leads)
    leads.to_csv("adresses_complete.csv", index=False)


if __name__ == "__main__":
    main()
