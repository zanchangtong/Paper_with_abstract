import re
import arxiv
from datetime import datetime
import xml.etree.ElementTree as ET
from tqdm import tqdm 
def clean_text(text):
    # 使用正则表达式替换不是英文字母和空格的所有字符
    cleaned_text = re.sub(r'[^a-zA-Z ]', '', text)
    return cleaned_text


# Construct the default API client.
client = arxiv.Client()
file_name="paper_title_dpo_ref"
titles=open(f"{file_name}.txt", "r", encoding="utf-8").readlines()
# Search for the 10 most recent articles matching the keyword "quantum."
updated=[]
failed=[]
for title in tqdm(titles[:10]):
    clean_title = clean_text(title)
    if len(clean_title) < 2:
        failed.append(title)
    search = arxiv.Search(
        query = "ti:" + clean_title,
        max_results = 3,
        # sort_by = arxiv.SortCriterion.SubmittedDate
    )
    results = client.results(search)
    all_results = list(results)

    if all_results:
        updated.append(all_results[0])
    else:
        failed.append(title)

if updated:
    # def create_rss_feed(entries):
    #     # 创建 RSS 根元素
    #     rss = ET.Element("rss", version="2.0")
    #     channel = ET.SubElement(rss, "channel")
    #     # 添加频道描述元素
    #     title = ET.SubElement(channel, "title")
    #     title.text = "dpo reference Papers"
    #     link = ET.SubElement(channel, "link")
    #     link.text = "http://zct_Paper_with_abstract.com/rss"
    #     description = ET.SubElement(channel, "description")
    #     description.text = "dpo reference papers."

    #     last_build_date = ET.SubElement(channel, "lastBuildDate")
    #     last_build_date.text = datetime.utcnow().strftime("%a, %d %b %Y GMT")

    #     # 添加论文条目
    #     for entry in entries:
    #         item = ET.SubElement(channel, "item")
    #         ET.SubElement(item, "title").text = entry["title"]
    #         ET.SubElement(item, "author").text = entry["author"]
    #         ET.SubElement(item, "description").text = entry["abstract"]
    #         ET.SubElement(item, "link").text = entry["link"]
    #         ET.SubElement(item, "comments").text = entry["comment"]
    #         ET.SubElement(item, "pubDate").text = entry["update_time"].strftime("%a, %d %b %Y %H:%M:%S GMT")
    #         ET.SubElement(item, "guid").text = entry["link"]
    #     # 生成 XML 树并保存到文件
    #     tree = ET.ElementTree(rss)
    #     tree.write(f"{file_name}.xml", encoding="utf-8", xml_declaration=True)
    def create_rss_feed(entries):
        # 创建 RSS 根元素并添加命名空间
        rss = ET.Element("rss", version="2.0", attrib={
            "xmlns:atom": "http://www.w3.org/2005/Atom",
            "xmlns:dc": "http://purl.org/dc/elements/1.1/"
        })
        channel = ET.SubElement(rss, "channel")
        # 添加频道描述元素
        ET.SubElement(channel, "title").text = "dpo reference Papers"
        ET.SubElement(channel, "link").text = "http://zct_Paper_with_abstract.com/rss"
        ET.SubElement(channel, "description").text = "Latest dpo reference papers."
        ET.SubElement(channel, "atom:link", href="http://zct_Paper_with_abstract.com/rss", rel="self", type="application/rss+xml")
        ET.SubElement(channel, "language").text = "en-us"
        ET.SubElement(channel, "lastBuildDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        ET.SubElement(channel, "pubDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

        # 添加论文条目
        for entry in entries:
            item = ET.SubElement(channel, "item")
            ET.SubElement(item, "title").text = entry["title"]
            ET.SubElement(item, "link").text = entry["link"]
            ET.SubElement(item, "description").text = entry["abstract"]
            ET.SubElement(item, "guid", isPermaLink="false").text = entry["link"]
            ET.SubElement(item, "dc:creator").text = entry["author"]
            ET.SubElement(item, "pubDate").text = entry["update_time"].strftime("%a, %d %b %Y %H:%M:%S GMT")

        # 生成 XML 树并保存到文件
        tree = ET.ElementTree(rss)
        tree.write(f"{file_name}.xml", encoding="utf-8", xml_declaration=True)

    # 示例数据
    entries = [
        {
            "title": paper.title,
            "author": ", ".join([author.name for author in paper.authors]), 
            "abstract": paper.summary.replace("\n", " "),
            "link": paper.entry_id ,
            "comment": paper.comment ,
            "update_time": paper.updated
        } for paper in updated
    ]
    sorted_data = sorted(entries, key=lambda x: x['update_time'])

    create_rss_feed(entries)

if failed:
    with open(f"{file_name}.failed", "w", encoding="utf-8") as f:
        f.writelines(failed)
