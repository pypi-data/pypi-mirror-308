from extraction.extractor import extract_gtap

import logging

logging.basicConfig(level=logging.INFO)

#Path to the GTAP data
source_path = r"C:\Users\beaufils\Documents\Projects\Ressources\MRIO\gtap11\2017"

#Path to save the extracted data
destination_path = r"C:\Users\beaufils\Documents\Projects\Ressources\MRIO\gtap11\test_extraction"

extract_gtap(source=source_path, destination=destination_path, build_io=True)