# -*- coding: utf-8 -*-
"""
    @File: scrapper.py
    @Author:Wang Shihan
    @Date:2024/7/26
    @Description:
"""
from newspaper import Article
from html2text import HTML2Text


class Scrapper:
    @classmethod
    def scrap_content(cls, url: str) -> str:
        """
        :param url: 链接
        :return:
        """
        article = Article(url)
        article.download()
        article.parse()
        h = HTML2Text()
        return h.handle(article.html)


if __name__ == '__main__':
    url = 'https://www.esri.com/arcgis-blog/products/arcgis-enterprise/mapping/nautical-chart-creation-is-versatile-with-arcgis-maritime/'
    res = Scrapper.scrap_content(url)
    print(res)
