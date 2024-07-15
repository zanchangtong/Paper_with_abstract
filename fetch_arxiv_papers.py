import arxiv
from datetime import datetime
import xml.etree.ElementTree as ET


last_updated_paper_file = "./last_updata_paper_title"
last_updated_paper_title = open(last_updated_paper_file, "r", encoding="utf-8").readlines()[0].strip()
# Construct the default API client.
client = arxiv.Client()

# Search for the 10 most recent articles matching the keyword "quantum."
search = arxiv.Search(
  query = "cat:cs.CL",
  max_results = 500,
  sort_by = arxiv.SortCriterion.SubmittedDate
)
results = client.results(search)
all_results = list(results)

updated = []
fatched_all=False
for result in all_results:
    if result.title == last_updated_paper_title:
        fatched_all = True
        break 
    else:
        updated.append(result)
if not fatched_all and not updated:
    search = arxiv.Search(
        query = "cat:cs.CL",
        max_results = 1500,
        sort_by = arxiv.SortCriterion.SubmittedDate
        )
    results = client.results(search)

    updated = []
    all_results = list(results)
    for result in all_results:
        if result.title == last_updated_paper_title:
            break 
        else:
            updated.append(result)

if updated:
    with open(last_updated_paper_file, "w", encoding="utf-8") as f:
        f.write(updated[0].title)

    def create_rss_feed(entries):
        # 创建 RSS 根元素
        rss = ET.Element("rss", version="2.0")
        channel = ET.SubElement(rss, "channel")
        # 添加频道描述元素
        title = ET.SubElement(channel, "title")
        title.text = "Daily arXiv cs.CL Papers"
        link = ET.SubElement(channel, "link")
        link.text = "http://zct_Paper_with_abstract.com/rss"
        description = ET.SubElement(channel, "description")
        description.text = "Daily updates of arXiv cs.CL papers."

        last_build_date = ET.SubElement(channel, "lastBuildDate")
        last_build_date.text = datetime.utcnow().strftime("%a, %d %b %Y GMT")

        # 添加论文条目
        for entry in entries:
            item = ET.SubElement(channel, "item")
            ET.SubElement(item, "title").text = entry["title"]
            ET.SubElement(item, "author").text = entry["author"]
            ET.SubElement(item, "description").text = entry["abstract"]
            ET.SubElement(item, "link").text = entry["link"]
            ET.SubElement(item, "comments").text = entry["comment"]
            ET.SubElement(item, "pubDate").text = entry["update_time"].strftime("%a, %d %b %Y %H:%M:%S GMT")
            ET.SubElement(item, "guid").text = entry["link"]
        # 生成 XML 树并保存到文件
        tree = ET.ElementTree(rss)
        tree.write("arxiv_cs_CL_papers.xml", encoding="utf-8", xml_declaration=True)

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

    create_rss_feed(entries)
