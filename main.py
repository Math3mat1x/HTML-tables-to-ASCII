from bs4 import BeautifulSoup as bs

def draw(table, headers):
    column_widths = list()
    for column in headers:
        length = len(max([column] + table[column]))
        column_widths.append(length + 1 * ((length - len(column)) % 2 == 1))

    separation = "+" + "".join(["-" * (i + 2) + "+" for i in column_widths]) # TODO
    print(separation)

    table_height = max([len(table[i]) for i in table])
    for i in range(table_height):
        if i == 0: # write headers
            out = list()

            for y, header in enumerate(headers):
                length = int((column_widths[y] - len(header)) / 2)

                text_to_add = " " * length + header + " " * (length + 1) + "|"
                out.append(text_to_add)

            out=  "| " + " ".join(out)

        elif i == 1 or i == (max([len(table[i]) for i in table]) - 1):
            out = separation
        else:
            out = list()
            for y, header in enumerate(headers):
                text_to_add = table[header][i] + " " * (column_widths[y] -\
                            len(table[header][i]) + 1) + "|"
                out.append(text_to_add)
            out=  "| " + " ".join(out)

        print(out)

def convert(html):
    html = bs(html, "lxml")

    trs = html.find_all("tr")

    if not (html.find("table") and trs and \
            "th" in [tag.name for tag in trs[0].find_all()]):
        raise ValueError("This is not a valid HTML table.")

    extract_text = lambda tag : "".join([i.text for i in tag]) if type(tag) == list else tag.text

    headers = [extract_text(tag) for tag in trs[0].find_all("th")]
    content = list()

    for tr in trs[1:]:
        if len(tr.find_all("td")) == 0:
            continue
        content += [extract_text(i) for i in tr.find_all("td")] +\
                [" " for _ in range(len(headers) - len(tr.find_all("td")))]

    table = {header:list() for header in headers}

    for i, element in enumerate(content):
        table[headers[i % len(headers)]].append(element)

    draw(table, headers)

if __name__ == "__main__":
    with open("test_table.html", "r") as f:
        test = f.read()

    convert(test)

# Example table : https://ozh.github.io/ascii-tables/
# +----------------------------------+---------+------------------------+----------------+
# |               Col1               |  Col2   |          Col3          | Numeric Column |
# +----------------------------------+---------+------------------------+----------------+
# | Value 1                          | Value 2 | 123                    |           10.0 |
# | Separate                         | cols    | with a tab or 4 spaces |       -2,027.1 |
# | This is a row with only one cell |         |                        |                |
# +----------------------------------+---------+------------------------+----------------+
# test
