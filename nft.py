# -*- coding: utf-8 -*-
import csv
import requests
from operator import itemgetter
import os
from datetime import date
from datetime import datetime

base_id = "appdfAdEv4GIbnfQa"
params = ()
api_key = "keyUgPimjqA2cKJC3"
headers = {"Authorization": "Bearer " + api_key}

celeb_table_name = "tblq0VHgFi53jR79O"
celeb_url = "https://api.airtable.com/v0/" + base_id + "/" + celeb_table_name
celeb_records = []

cites_table_name = "tbljYhV1Q1Iwsb8wk"
cites_url = "https://api.airtable.com/v0/" + base_id + "/" + cites_table_name
cites_records = []

# get celeb records
run = True
print("Getting celebs...")
while run is True:
    response = requests.get(celeb_url, params=params, headers=headers)
    airtable_response = response.json()
    celeb_records += (airtable_response['records'])
    if 'offset' in airtable_response:
        run = True
        params = (('offset', airtable_response['offset']),)
    else:
        run = False

# get cites records
run = True
print("Getting cites...")
while run is True:
    response = requests.get(cites_url, params=params, headers=headers)
    airtable_response = response.json()
    cites_records += (airtable_response['records'])
    if 'offset' in airtable_response:
        run = True
        params = (('offset', airtable_response['offset']),)
    else:
        run = False

# sort the celebs
def sortByName(a):
    return a['fields'].get('Name')
print("Sorting celebs...")
celeb_records.sort(key=sortByName)

# sort the cites by date
def sortByDate(a):
    return a['fields'].get('Date')
print("Sorting cites...")
cites_records.sort(key=sortByDate)

# give every celeb their start date
for x in celeb_records:
    d = datetime.today()
    for y in x['fields'].get('Sources'):
        z = next((cite for cite in cites_records if cite["id"] == y), None)
        if z and datetime.strptime(str(z['fields'].get('Date')), '%Y-%m-%d') < d:
            d = datetime.strptime(str(z['fields'].get('Date')), '%Y-%m-%d')
    x['Start'] = d.strftime('%b %-d, %Y')

# for x in celeb_records:
#     name = x['fields'].get('Name').strip()
#     worth = x['fields'].get('Est. worth')
#     worth_cite = x['fields'].get('Worth cite').strip()
#     sources = x['fields'].get('Sources')

def getCelebCites(x):
    temp = ""
    for z in x['fields'].get('Sources'):
        y = next((cite for cite in cites_records if cite["id"] == z), None)
        # print(y)
        # c = y['fields'].get('Index')
        c = cites_records.index(y) + 1
        temp += """
            <span class="refs" id="ref-{}"><a href="#cite-{}">{}</a></span>, 
        """.format(c, c, c)
    temp = temp[:-11]
    return temp

def createCelebLine(x):
    full = """
    <tr class="celeb">
                <td>
                  {}
                </td>
                <td class="right">
                    {}<a href="{}" target="_blank">*</a>
                </td>
                <td class="promo">
                  {}
                </td>
                <td>
                      {}
                </td>
              </tr>
    """.format(
        x['fields'].get('Name').strip().encode('utf-8'),
        "{:,}".format(x['fields'].get('Est. worth')),
        x['fields'].get('Worth cite').strip(),
        x['Start'].strip().encode('utf-8'),
        getCelebCites(x))
    return full

def add_cites(u, i):
    return """
        <li class="cite"><span id="cite-{}"><a href="{}" target="_blank"><span class="url">{}</span></a></span></li>
    """.format(
        i,
        u['fields'].get('URL').strip().encode('utf-8'),
        u['fields'].get('URL').strip().encode('utf-8')
    )

def create_index():
    full = """
        <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Promoting the grift</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="style.css" rel="stylesheet">
        <link href="normalize.css" rel="stylesheet">
        <link href="skeleton.css" rel="stylesheet">
        <link rel="icon" type="image/png" href="favicon.png">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
        <script type="text/javascript" src="code.js"></script>
    </head>
    <body>
        <div class="container">
        <div class="row">
            <div class="twelve columns">
            <p>Web3 is <a href="https://web3isgoinggreat.com/" target="_blank">not off to a great start</a>, and NFTs are a <a href="https://www.currentaffairs.org/2021/12/are-nfts-any-more-stupid-than-everything-else" target="_blank">particularly useless</a> application of blockchains. On top of their <a href="https://www.wired.com/story/nfts-hot-effect-earth-climate/" target="_blank">terrible environmental effects</a>, every week there are stories of <a href="https://fortune.com/2022/02/04/nft-wash-trade-scam-millions/" target="_blank">rampant wash trades</a>, <a href="https://kotaku.com/nft-minecraft-blockchain-scam-blockverse-crypto-1848446906" target="_blank">scams</a>, <a href="https://www.cnet.com/news/how-a-300k-bored-ape-yacht-club-nft-was-accidentally-sold-for-3k/" target="_blank">serious design flaws</a>, and <a href="https://www.theverge.com/2022/2/3/22916111/wormhole-hack-github-error-325-million-theft-ethereum-solana" target="_blank">general incompetence</a>.</p>
            <p>Yet none of this has stopped celebrities from promoting this ecosystem of grifts, often for personal gain. This website is an effort to document every promotion by a celebrity of an NFT project (or an especially egregious cryptocurrency endeavour).</p>
            </div>
        </div>
        <div class="row">
            <div class="eight columns offset-by-two">
            <table class="u-full-width">
                <thead>
                <tr>
                    <th class="left clicky">Name</th>
                    <th class="right clicky">Est. worth ($)</th>
                    <th class="promo clicky">Date</th>
                    <th class="left">Sources</th>
                </tr>
                </thead>
                <tbody>
    """

    for b in celeb_records:
        print("Adding {}...".format(b['fields'].get('Name').strip()))
        full += createCelebLine(b)

    full += """
        </tbody>
            </table>
        </div>
        </div>
        <div class="row">
            <div class="twelve columns">
            <ol>
    """

    for i, u in enumerate(cites_records, start=1):
        full += add_cites(u, i)

    full += """
        </ol>
            </div>
        </div>
        <div class="row">
            <div class="twelve columns" style="text-align:center">
            Who'd we miss? Email us at info@
            </div>
        </div>
        <div class="fly"></div>
        <!--Last updated on {}-->
    </body>
    </html>

    """.format(date.today().strftime('%b %-d, %Y'))

    with open('index.html', 'w') as fp:
        fp.write(full)

create_index()
