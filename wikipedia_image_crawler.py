import wptools
import urllib.request
import requests
from urllib.parse import quote
import hashlib
import re
import os
import tqdm

OUTPUT_FOLDER = 'downloaded'

VALID_EXTENSIONS = {".jpg", ".JPG", ".jpeg", ".JPEG"}

ENDPOINT_METADATA = "http://de.wikipedia.org/w/api.php?action=query&prop=imageinfo&iiprop=extmetadata&titles=File%3a{}&format=json"
ENDPOINT_IMAGE = "http://upload.wikimedia.org/wikipedia/commons/{}"

def extract_meta_data(image_name):
    quoted_name = quote(image_name)
    result = requests.get(ENDPOINT_METADATA.format(quoted_name))
    result = result.json()

    return list(result['query']['pages'].values())[0]['imageinfo'][0]['extmetadata']

def get_image_link(image_name):
    image_name = image_name.replace(" ", "_")
    quoted_name = quote(image_name)
    digest = hashlib.md5(image_name.encode('utf-8')).hexdigest()
    folder = digest[0] + "/" + digest[0] + digest[1] + "/" + quoted_name
    return ENDPOINT_IMAGE.format(folder)


with open('articles.csv', 'r', encoding="utf-8") as f:
    articles = f.readlines()
articles = [x.strip() for x in articles]

articles = list(set(articles))

license_file = open('{}/licenses.csv'.format(OUTPUT_FOLDER),'w')
for article in tqdm.tqdm(articles):
    save_path = r'{}/{}'.format(OUTPUT_FOLDER, article)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    page = wptools.page(article, lang='de', silent=True)
    page.get_more()

    descriptions = page.data['files']

    for file_description in descriptions:
        file_name = file_description.partition("Datei:")[2]

        if not any(file_name.endswith(ext) for ext in VALID_EXTENSIONS):
            continue

        try:
            meta_data = extract_meta_data(file_name)
        except:
            print("Could not fetch meta data for {}".format(file_name))
            continue

        url = get_image_link(file_name)

        try:
            urllib.request.urlretrieve(url, "{}/{}".format(save_path, file_name))
        except:
            print(meta_data)
            print(url)
            print("Could not download {}".format(file_name))
            continue

        license = meta_data['LicenseShortName']['value']

        if 'Artist' in meta_data:
            artist_raw_information = meta_data['Artist']['value']
            artist_information = re.sub('<[^<]+?>', '', artist_raw_information).replace("\n", " ")
        else:
            artist_information = " "

        if 'Credit' in meta_data:
            credit_raw_information = meta_data['Credit']['value']
            credit_information = re.sub('<[^<]+?>', '', credit_raw_information).replace("\n", " ")
        else:
            credit_information = " "

        license = license.replace(";", " ")
        artist_information = artist_information.replace(";", " ")
        credit_information = credit_information.replace(";", " ")
        license_file.write("{};{};{};{};{}\n".format(
            '{}/{}'.format(article, file_name), license, artist_information, credit_information, url))

license_file.close()