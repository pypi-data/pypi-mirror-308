from pyjats.structures import Article, Xref
from xsdata_pydantic.bindings import XmlParser
import time

def extract_references(article_ref_list):
    references = {}
    print(len(article_ref_list))
    for ref_o in article_ref_list:
        for ref in ref_o.ref:
            xref = ref.id
            pmid = list(filter(lambda x: x.pub_id_type == 'pmid', ref.element_citation[0].pub_id))
            pmid = "".join([a.content[0] for a in pmid])

            if pmid != "":
                references[xref] = pmid

    return references

def expand_xref_content(xref):
    if len(xref.content) == 2 and xref.content[-1] not in [',', '-']:
        # The content is a reference number and continuation, return it
        return xref.content

def extract_text_from_section(sec):
    section_text = ""
    for para in sec.p:
        para_text = ""
        for c in para.content:
            if isinstance(c, str):
                para_text += c

                ## This will just grab the text content of references, may be able to do better?
            elif isinstance(c, Xref):
                for txt in c.content:
                    para_text += txt
            else:
                for txt in c.content:
                    if isinstance(txt, str):
                        para_text += txt
        section_text += f"\n{para_text}\n\n"
    return section_text


def parse_xml(file_path):
    with open(file_path, 'rb') as art_file:

        parser = XmlParser()
        article = parser.parse(art_file, Article)
    sections = {}
    for section in article.body.sec:
        section_text = extract_text_from_section(section)
        if len(section.sec) > 0:
            for subsec in section.sec:
                section_text += f"{subsec.title.content[0]}\n"
                section_text += extract_text_from_section(subsec)



        sections[section.title.content[0]] = section_text

    return sections
