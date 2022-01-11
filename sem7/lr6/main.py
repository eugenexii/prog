from typing import TypedDict
from bs4 import BeautifulSoup as bs
from bs4.element import Tag
from natasha.const import PER
from natasha.doc import DocSpan
import requests as req
import re
from natasha import Doc, NamesExtractor
from natasha.syntax import NewsSyntaxParser
from natasha.segment import Segmenter
from natasha.morph.vocab import MorphVocab
from natasha.morph.tagger import NewsMorphTagger
from natasha.emb import NewsEmbedding
from natasha.ner import NewsNERTagger
from collections import Counter
from wordcloud.wordcloud import WordCloud

segmenter = Segmenter()
emb = NewsEmbedding()
ner_tagger = NewsNERTagger(emb)
morph_vocab = MorphVocab()
morph_tagger = NewsMorphTagger(emb)
names_extractor = NamesExtractor(morph_vocab)
syntax_parser = NewsSyntaxParser(emb)


hub_url = "https://www.herzen.spb.ru/main/facts/nowadays/1558542985/1559574321/"
news_re = r"https:\/\/(www\.)?herzen\.spb\.ru\/news\/\d\d-\d\d-\d\d\d\d(_\d)?\/"

hub_page = bs(req.get(hub_url).content, "html.parser")

hub_news = hub_page.find_all("a", {"href": re.compile(news_re)})

news_list = [news for news in hub_news if isinstance(news, Tag)]
assert len(news_list), "no news found in hub"


class NewsData(TypedDict):
    url: str
    title: str
    chars: list[str]
    top_words: list[str]


news_data: list[NewsData] = []

for news_a in news_list:
    news_url = news_a["href"]
    if not isinstance(news_url, str):
        continue
    news_page = bs(req.get(news_url).content, "html.parser")
    news_content = news_page.find("div", {"style": "padding:0 5 5 5px"})
    if not isinstance(news_content, Tag):
        continue
    news = news_content.get_text()

    doc = Doc(news)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    for token in doc.tokens:
        token.lemmatize(morph_vocab)
    doc.parse_syntax(syntax_parser)
    doc.tag_ner(ner_tagger)
    for span in doc.spans:
        span.normalize(morph_vocab)
        if span.type == PER:
            span.extract_fact(names_extractor)

    chars: list[DocSpan] = [span for span in doc.spans if span.type == PER]
    chars_words: list[str] = [char.text for char in chars]
    uniq_chars: set[str] = set(chars_words)

    words: list[str] = []
    for token in doc.tokens:
        if token.pos in ["NOUN", "VERB", "ADJ"]:
            words.append(token.lemma)

    words_freq = Counter(words + chars_words)
    cloud = WordCloud().generate_from_frequencies(words_freq)
    cloud.to_file(news_url.split("/")[-2] + ".png")

    news_data.append(
        {
            "url": news_url,
            "title": news_a.get_text(),
            "chars": list(uniq_chars),
            "top_words": [word for word, _ in Counter(words).most_common(10)],
        }
    )


import json

with open("data.json", "w") as f:
    json.dump(news_data, f, ensure_ascii=False)
