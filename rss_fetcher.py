import requests
import xml.etree.ElementTree as ET


namespaces = {
    'yt': 'http://www.youtube.com/xml/schemas/2015',
    'atom': 'http://www.w3.org/2005/Atom',
    'media': 'http://search.yahoo.com/mrss/'
}

def fetch_rss(id, view_count_filter):
    res = requests.get(f"https://www.youtube.com/feeds/videos.xml?channel_id={id}")
    root = ET.fromstring(res.content)

    entries = root.findall('.//atom:entry', namespaces)

    delete_entries = []
    for ent in entries:
        view_count = int(ent.find('.//media:statistics', namespaces).get('views'))
        if view_count < view_count_filter:
            delete_entries.append(ent)

    for ent in delete_entries:
        root.remove(ent)

    ET.register_namespace('', namespaces['atom'])
    ET.register_namespace('yt', namespaces['yt'])
    ET.register_namespace('media', namespaces['media'])

    ET.indent(root)
    return ET.tostring(root, encoding='unicode')