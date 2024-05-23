import pandas as pd
import scraping_util as sutil
import constants as cts

import time
import sys


def scraping_pipeline() -> None:
    driver = sutil.get_driver()
    df = pd.DataFrame(columns=['time', 'text'])

    # Get all speech URLs to current date
    speech_partial_urls = []
    for page in range(cts.NUM_PAGES_TO_SCRAPE):
        cur_url = cts.SPEECHES_RESULT_PAGE + str(page)
        speech_links = sutil.get_links_from_page(
            driver=driver, page_url=cur_url)
        speech_partial_urls.extend(speech_links)

    # Scrape text from each page and add to df
    for speech_url in speech_partial_urls:
        full_url = cts.PRESIDENCY_SITE_LINK + speech_url
        speech_content_tup = sutil.get_speech_content(
            driver=driver, page_url=full_url)
        new_row = {'time': speech_content_tup[cts.SPEECH_CONTENT_DATE_IDX],
                   'text': speech_content_tup[cts.SPEECH_CONTENT_TEXT_IDX]}
        
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Save the DataFrame to a CSV
    df.to_csv('./scraped_data/alllBidenSpeeches.csv')


if __name__ == "__main__":
    scraping_pipeline()
