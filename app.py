import requests
from bs4 import BeautifulSoup
import csv

URL = "https://www.toysperiod.com/lego-set-reference/harry-potter/lego-71043-hogwarts-castle/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

parts_table = soup.find(id="pt")
parts_rows = parts_table.find_all("tr")

parts = []

for row in parts_rows:
    columns = row.find_all("td")
    checkbox, part_number, name, quantity, image_obj, colour = columns if len(columns) == 6 else [None, None, None, None, None, None]
    image_uri = None
    image_offset = None
    if image_obj:
        uri = image_obj.find("img")["src"]
        offset = image_obj.find("img")["style"]
        image_offset = offset.strip()
        image_uri = f"https://www.toysperiod.com/{uri}"
    parts.append(
        dict(
            part_number=part_number.text.strip() if part_number else None,
            name=name.text.strip() if name else None,
            quantity=int(quantity.text.strip()) if quantity else None,
            image_uri=image_uri if image_uri else None,
            image_offset = offset if image_uri else None,
            colour=colour.text.strip() if colour else None
        )
    )

with open("parts.csv", "w+") as csvfile:
    fields = ["part_number", "name", "quantity", "image_uri", "image_offset", "colour"]
    writer = csv.DictWriter(csvfile, fieldnames=fields, quotechar='"', delimiter="|")

    # writing headers (field names)
    writer.writeheader()

    # writing data rows
    writer.writerows(parts)