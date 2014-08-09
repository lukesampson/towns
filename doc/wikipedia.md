## Extracting suburb data from Wikipedia

Prerequisites:
* [Requests](http://docs.python-requests.org/en/latest/)
    `pip install requests`
* pytest
    `pip install pytest`


# Overview of what happens

1. Crawls sub-categories of the Suburbs in Australia page on Wikipedia
2. Relies on the [Infobox Australian place](http://en.wikipedia.org/wiki/Template:Infobox_Australian_place) template to extract city and postcode data.