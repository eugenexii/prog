from typing import TypedDict, Optional, Literal
from bs4 import BeautifulSoup as bs
from bs4.element import Tag
import requests as req
import json
from termcolor import colored


class ErrorHandler:
    errors = 0
    warnings = 0
    notes = 0

    def handle(self, message: str, type: Literal["error", "warning", "note"] = "error"):
        if type == "error":
            self.errors += 1
            print(colored("Error:", "red", attrs=["bold"]), message)
        elif type == "warning":
            self.warnings += 1
            print(colored("Warning:", "yellow", attrs=["bold"]), message)
        elif type == "note":
            self.notes += 1
            print(colored("Note:", "blue", attrs=["bold"]), message)

    def report(self):
        print(
            "Encountered",
            colored(
                str(self.errors + self.warnings + self.notes), "white", attrs=["bold"]
            ),
            "problems:",
        )
        print("Errors[" + colored(str(self.errors), "red", attrs=["bold"]), end="], ")
        print(
            "Warnings[" + colored(str(self.warnings), "yellow", attrs=["bold"]),
            end="], ",
        )
        print("Notes[" + colored(str(self.notes), "blue", attrs=["bold"]), end="]")


error_handler = ErrorHandler()
eprint = error_handler.handle


base_url = "https://www.herzen.spb.ru"
inst_url = "/main/structure/inst"

atlas_url = "https://atlas.herzen.spb.ru/"
fac_url = "faculty.php"

inst_page = bs(req.get(base_url + inst_url).content, "html.parser")

inst_div = inst_page.find("div", {"style": "padding:0 5 5 5px"})
assert isinstance(inst_div, Tag), "something went wrong when parsing pages"

inst_ul = inst_div.find("ul")
assert isinstance(inst_ul, Tag)

insts_list = [li for li in inst_ul.find_all("li") if isinstance(li, Tag)]
assert len(insts_list), "something went wrong when parsing pages"


class Inst(TypedDict):
    url: str
    name: str


insts: list[Inst] = []
for inst in insts_list:
    inst_a = inst.a
    if not inst_a:
        eprint(f"couldn't find an anchor tag for\n{inst}\n")
        continue

    url = inst_a["href"]
    if not isinstance(url, str):
        eprint(f"couldn't extract a link from\n{inst_a}\n")
        continue

    insts.append(
        {
            "url": base_url + url,
            "name": inst_a.get_text(),
        }
    )

fac_page = bs(req.get(atlas_url + fac_url).content, "html.parser")

fac_div = fac_page.find("div", {"style": "width: 650px; margin-left: 30px"})
assert isinstance(fac_div, Tag), "something went wrong when parsing pages"

fac_ul = fac_div.find("ul")
assert isinstance(fac_ul, Tag), "something went wrong when parsing pages"

fac_list = [li for li in fac_ul.findAll("li") if isinstance(li, Tag)]
assert len(fac_list), "something went wrong when parsing pages"

caf_lists_tags: dict[str, Tag] = {}
for fac in fac_list:
    fac_a = fac.a
    if not fac_a:
        eprint(f"couldn't find an anchor tag for\n{fac.get_text()}\n")
        continue

    fac_name = fac_a.get_text()

    name = [
        inst["name"]
        for inst in insts
        if inst["name"].partition(" ")[2].strip().lower()
        == fac_name.partition(" ")[2].strip().lower()
        and fac_name.split(" ")[0] == "институт"
    ]
    if len(name) > 0:
        caf_lists_tags[name[0]] = fac


class Caf(TypedDict):
    atlas_url: str
    name: str
    chief: Optional[str]
    chief_atlas: Optional[str]
    chief_email: Optional[str]


caf_lists: dict[str, list[Caf]] = {inst["name"]: [] for inst in insts}
for name, caf_list in caf_lists_tags.items():
    caf_list_ul = caf_list.ul
    if not caf_list_ul:
        eprint(f"couldn't extract cafs list for\n{name}\n")
        continue
    cafs = [li for li in caf_list_ul.find_all("li") if isinstance(li, Tag)]
    if not len(cafs):
        eprint(f"no cafs found for\n{name}\n")
        continue

    for caf in cafs:
        caf_a = caf.a
        if not caf_a:
            eprint(f"couldn't find an anchor tag for\n{caf}\n")
            continue

        caf_name = caf_a.get_text().strip()

        if caf_name == "cписок ОПОП":
            continue

        url = caf_a["href"]
        if not isinstance(url, str):
            eprint(f"couldn't extract a link from\n{caf_a}\n")
            continue

        caf_atlas_page = bs(req.get(atlas_url + url).content, "html.parser")
        chief_h3s = caf_atlas_page.find_all(
            "h3", text="Заведующий кафедрой:", attrs={"class": "mm"}
        )
        chief_name: Optional[str] = None
        chief_url: Optional[str] = None
        chief_email: Optional[str] = None
        for chief_h3 in chief_h3s:
            if not isinstance(chief_h3, Tag):
                continue

            chief_p = chief_h3.next_sibling
            if not isinstance(chief_p, Tag):
                continue

            chief_name = chief_p.get_text().split(",")[0]

            table = caf_atlas_page.find("table", {"class": "table_good"})
            if not isinstance(table, Tag):
                continue

            for tr in table.find_all("tr"):
                if not isinstance(tr, Tag):
                    continue
                tr_a = tr.a
                if not tr_a:
                    continue
                if tr_a.get_text().strip() != chief_name:
                    continue
                chief_url_pre = tr_a["href"]
                if not isinstance(chief_url_pre, str):
                    continue
                chief_url = chief_url_pre

                chief_info_page = bs(
                    req.get(atlas_url + chief_url).content, "html.parser"
                )
                chief_email_h3s = chief_info_page.find_all(
                    "h3", text="E-mail:", attrs={"class": "mm"}
                )

                for chief_email_h3 in chief_email_h3s:
                    if not isinstance(chief_email_h3, Tag):
                        continue
                    chief_email_p = chief_email_h3.next_sibling
                    if not isinstance(chief_email_p, Tag):
                        continue

                    chief_email = chief_email_p.get_text()

                break
            break

        if not chief_name:
            eprint(
                f"couldn't extract a name of a chief of\n{caf_name}\n(link: {atlas_url + url})\n"
            )

        elif not chief_url:
            eprint(
                f"couldn't extract a link to a chief of\n{caf_name}\n(name: {chief_name}, link: {atlas_url + url})\n"
            )

        elif not chief_email:
            eprint(
                f"couldn't extract an email of a chief of\n{caf_name}\n(name: {chief_name}, link: {atlas_url + chief_url})\n"
            )

        caf_lists[name].append(
            {
                "atlas_url": atlas_url + url,
                "name": caf_name,
                "chief": chief_name,
                "chief_atlas": atlas_url + chief_url if chief_url else None,
                "chief_email": chief_email,
            }
        )


error_handler.report()


class DataRecord(Inst):
    cafs: list[Caf]


data: list[DataRecord] = []
for inst in insts:
    name, url = inst["name"], inst["url"]
    data.append(
        {
            "cafs": caf_lists[name],
            "name": name,
            "url": url,
        }
    )


with open("data.json", "w") as f:
    json.dump(data, f, ensure_ascii=False)
