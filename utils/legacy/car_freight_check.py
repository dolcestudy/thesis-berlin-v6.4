import xml.etree.ElementTree as ET

# XMLファイルのパス
xml_file = r"output\micro100-sp60-pce0.5-DMC2.5-MDR0.24-iter10\output_network.xml"  # 変更してください

# XMLファイルをパース
tree = ET.parse(xml_file)
root = tree.getroot()

# 条件に合うリンクを探す
matching_links = []

# <link>要素をループして、modes属性をチェック
for link in root.findall(".//link"):
    modes = link.get("modes", "")
    if "car" in modes and "truck" not in modes:
        matching_links.append(link)

# 結果を出力
if matching_links:
    print(f"Found {len(matching_links)} links where 'car' is present but 'freight' is not:")
    for link in matching_links:
        print(ET.tostring(link, encoding="unicode").strip())
else:
    print("No links found matching the criteria.")
