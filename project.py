import sys
import os
import argparse
import re
from tabulate import tabulate
from fpdf import FPDF
import requests
from os import path
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

dotenv.config(pip)

def main() -> None:
    type, file = cli()
    file = check_path(file)
    print("Hold on, fetching source table . . .".upper())
    table = get_source_table()
    print(
        tabulate(table, headers="keys", tablefmt="pretty", colalign=("center", "right"))
    )

    print("PLease use the above table to ensure you input the right source (if need be) ".upper(), "Note you cannot use the sources parameter with the country or category parameters", sep="\n")
    
    key_params = inp_params(table, type)
    if type == "h":
        news =healines(key_params)
    else:
        news = everything(key_params)

    pdfify(news, file)

def get_source_table() -> list:
    table = list()
    sources = requests.get("https://newsapi.org/v2/top-headlines/sources?apiKey=5afb383718b144878630c63670764cd9")
    source = sources.json()["sources"]
    for s in source:
        table.append(
            {
                "source_name": s["name"].strip(),
                "country": s["country"],
                "category": s["category"],
            }
        )
    return table

COUNTRY_LIST = [
    "ae",
    "ar",
    "at",
    "au",
    "be",
    "bg",
    "br",
    "ca",
    "ch",
    "cn",
    "co",
    "cu",
    "cz",
    "de",
    "eg",
    "fr",
    "gb",
    "gr",
    "hk",
    "hu",
    "id",
    "ie",
    "il",
    "in",
    "it",
    "jp",
    "kr",
    "lt",
    "lv",
    "ma",
    "mx",
    "my",
    "ng",
    "nl",
    "no",
    "nz",
    "ph",
    "pl",
    "pt",
    "ro",
    "rs",
    "ru",
    "sa",
    "se",
    "sg",
    "si",
    "sk",
    "th",
    "tr",
    "tw",
    "ua",
    "us",
    "ve",
    "za",
]

CATEGORY_LIST = [
    "business",
    "entertainment",
    "general",
    "health",
    "science",
    "sports",
    "technology",
]


def cli() -> list:
    """
    returns a list of the endpoint type and the output file
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-t",
        "--headlines",
        help="headlines: provides live top and breaking headlines for a country, specific category in a country, single source, or multiple sources. You can also search with keywords. Articles are sorted by the earliest date published first",
        action="store_true",
    )
    group.add_argument(
        "-e",
        "--everything",
        help="Search through millions of articles from over 150,000 large and small news sources and blogs",
        action="store_true",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="name of output pdf file for news to be sourced.",
        required=True,
    )

    args = parser.parse_args()
    if args.file[-4:] != ".pdf":
        sys.exit("Invalid filetype")
    if args.headlines:
        return ["h", args.file]
    if args.everything:
        return ["e", args.file]


def inp_params(table: list, news_type: str) -> dict:
    if news_type == "e":
        try:
            sources = check_source(
                table,
                input("sources to be queried. check table (source_param) above: ".upper()),
            )

            q = check_q(input("Keywords or phrase to search for: ".upper()))
            start = check_date(input("Date to start search (yyyy-mm-dd): ".upper()))
            stop = check_date(input("Date to stop search (yyyy-mm-dd): ".upper()))
            # print(*[x.upper() for x in LANG_LIST], sep=", ")
            # lang = check_lang(input("Language to get headlines: ".upper()))
            num = check_page(input("Page of result: ".upper()))

        except (KeyboardInterrupt, EOFError):
            sys.exit("\n")

        return {
            "q": q,
            "from": start,
            "page": num,
            "to": stop,
            "language": "en",
            "sources": sources,
        }

    elif news_type == "h":
        try:
            sources = check_source(
                table,
                input("sources to be queried. check table (source_param) above: ".upper()),
            )

            q = check_q(input("Keywords or phrase to search for: ".upper()))
            print(*[x.title() for x in CATEGORY_LIST], sep=", ")
            category = check_category(
                input("The category you want to get headlines for: ".upper())
            )
            print(*[x.upper() for x in COUNTRY_LIST], sep=", ")
            country = check_country(
                input(
                    "The 2-letter ISO 3166-1 code of the country you want to get headlines for: ".upper()
                )
            )
            num = check_page(input("Page of result: ".upper()))
        except (KeyboardInterrupt, EOFError):
            sys.exit("\n")

        return {
            "q": q,
            "category": category,
            "page": num,
            "country": country,
            "sources": sources,
        }


def check_q(q: str) -> str | None:
    if len(q.strip()) == 1:
        sys.exit("Invalid Keywords or phrase")
    elif len(q.strip()) >= 2:
        return q
    else:
        return None


def check_date(date: str) -> str | None:
    if date:
        if re.fullmatch(
            r"\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d\.\d+(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d\.\d+)|(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d)|(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d)",
            date,
        ) or re.fullmatch(r"\d{4}-[01]\d-[0-3]\d", date):
            return date
        else:
            sys.exit("Invalid date format")
    else: 
        return None


# def check_lang(lang: str) -> str:
#     lang = lang.lower().strip()
#     if lang in LANG_LIST:
#         return lang
#     sys.exit("Invalid Langauge")


def check_page(num: str) -> int:
    try:
        num = int(num)
    except (TypeError, ValueError):
        sys.exit("Invalid Page number")
    return num


def check_country(cnt: str) -> str | None:
    cnt = cnt.lower().strip()
    if cnt:
        if cnt not in COUNTRY_LIST:
            sys.exit("Invalid Country")
        return cnt
    else:
        return None

def check_category(cat: str) -> str | None:
    if cat:
        cat = cat.lower().strip()
        if cat not in CATEGORY_LIST:
            sys.exit("Invalid Category for search")
        return cat
    else: 
        return None


def everything(params: dict) -> dict:
    if not params["q"] and not params["sources"]:
        sys.exit("Input Sources or q parameters")
    Url = f"https://newsapi.org/v2/everything?apiKey={API_KEY}"
    for key, value in params.items():
        if value != None:
            Url = Url + f"&{key}={value}"
    
    return requests.get(Url).json()


def healines(params: dict) -> dict:
    if params["sources"] and params["country"]:
        sys.exit("You cannot mix the sources parameter with country parameter")
    elif params["sources"] and params["category"]:
        sys.exit("You cannot mix the sources parameter with category parameter")
    Url = f"https://newsapi.org/v2/top-headlines?apiKey={API_KEY}"
    for key, value in params.items():
        if value != None:
            Url = Url + f"&{key}={value}"
    return requests.get(Url).json()


def check_source(table: list, source: str | None) -> str | None:
    if source:
        source_split = source.strip().split(",")
        source_split = [s.strip().title() for s in source_split]
        sources = list()
        for index in table:
            sources.append(index["source_name"].strip())
        if all(sor in sources for sor in source_split):
            return source.strip()
        else:
            sys.exit("Invalid source")
    return None

def check_path(dir: str ) -> None:
    dir = path.realpath(dir)
    print(dir)
    head = path.dirname(dir)
    if not path.isdir(head):
        sys.exit("Invalid file path")
    
    return dir

#https://stackoverflow.com/a/27084708/23470084
# def isEnglish(s):
#     try:
#         s.encode(encoding='utf-8').decode('ascii')
#     except UnicodeDecodeError:
#         return False
#     else:
#         return True
    

def pdfify(news: dict, path: str):
    pdf = FPDF()
    pdf.add_font("RobotoMono", style="", fname="Roboto_Mono/static/RobotoMono-Regular.ttf")
    pdf.add_font("RobotoMono", style="B", fname="Roboto_Mono/static/RobotoMono-Bold.ttf")
    pdf.add_font("RobotoMono", style="I", fname="Roboto_Mono/static/RobotoMono-Italic.ttf")
    pdf.add_font("RobotoMono", style="BI", fname="Roboto_Mono/static/RobotoMono-BoldItalic.ttf")
    
    pdf.add_page()
    
    for article in news["articles"]:
        title: str = str(article["title"])
        summary: str = str(article["description"]) or "N/A click on the link to read the article"
        url: str = str(article["url"])
        date: str = str(article["publishedAt"])
        source: str = str(article["source"]["name"])
        author: str = str(article["author"]) or "N/A"
        content: str = str(article["content"]) or "N/A (click on the link to read article)"
        
        # if not isEnglish(title) or not isEnglish(summary) or not isEnglish(author) or not isEnglish(content):
        #     continue

        pdf.set_font("RobotoMono", style="B", size= 20)
        pdf.multi_cell(w=pdf.epw,text=title, align="C")
        pdf.ln()
        pdf.set_font(style="B", size= 14)
        pdf.cell(text="source: ", align="L")
        pdf.set_font(style="", size= 14)
        pdf.write(text=source)
        pdf.ln()
        pdf.set_font(style="B", size= 14)
        pdf.cell(text="author: ", align="L")
        pdf.set_font(style="", size= 14)
        pdf.write(text= author)
        pdf.ln()
        pdf.cell(text="click to read article", link=url, align="L")
        pdf.ln(10)
        pdf.set_font(style="B", size= 14)
        pdf.cell(text="Summary: ", align="L")
        pdf.set_font(style="", size= 14)
        pdf.write(text=summary)
        pdf.ln(5)
        pdf.set_font(style="B", size= 14)
        pdf.cell(text="Content: ", align="L")
        pdf.set_font(style="", size= 14)
        pdf.write(text=content)
        pdf.ln(5)
        pdf.set_font(style="B", size= 14)
        pdf.cell(text=f"Date Published: ", align="L")
        pdf.write_html(text= date)
        pdf.ln(20)
        
    pdf.output(path)
        
        
if __name__ == "__main__":
    main()
