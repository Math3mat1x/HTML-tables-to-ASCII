from bs4 import BeautifulSoup as bs

def convert(html):
    html = bs(html, "lxml")

    trs = html.find_all("tr")

    headers = list()
    content = list()

    for tr in trs:
        tags = [tag.name for tag in tr.find_all()]

        if "th" in tags:
            headers += [i.contents[0].text for i in tr.find_all("th")]
        else:
            content += [i.contents[0].text for i in tr.find_all("td")]

    table = {header:list() for header in headers}

    for i, element in enumerate(content):
        table[headers[i % len(headers)]].append(element)

    return table


if __name__ == "__main__":
    with open("test_table.html", "r") as f:
        test = f.read()

    print(result = convert(test))
