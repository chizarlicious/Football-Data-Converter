# First go at parsing html code via BeautifulSoup 4
# no JSON yet

from bs4 import BeautifulSoup, SoupStrainer
from sys import exit

# Play by Play table carries id "pbp_data", no need to parse entire site, just
# need that table, for now.
only_pbp= SoupStrainer(id="pbp_data")

# Using sample file located in data directory for now, will specify a command
# line option for game or season
html_doc = open('../../data/html/201301120den.htm','r')

# Make soup to step through tags
game_table = BeautifulSoup(html_doc, "html.parser", parse_only=only_pbp)

html_doc.close()

def no_thead(tag):
    return 'thead' not in tag['class']

def num_cols(tag):
    return len(tag.find_all('td'))

rows = game_table.find_all('tr')

# Parse through the plays
for row in rows:
    # Make sure we don't have any weird header information included
    if num_cols(row) > 0 and no_thead(row):
        columns = row.find_all('td')

    # Grab each field
    for column in columns:
        print(column.string)
        print(column.prettify())

# TODO build up string in case of class="wrap", which is the description field.
# column.string returns None, but clearly there's text to be had.
    scoring = "is_scoring" in row['class']
    pos_change = 'pos_change' in row['class']
    exit()
