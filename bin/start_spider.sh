#!/bin/sh
cd spiders
scrapy crawl spider_quan_tang_poem
scala src/main/scala-2.11/tools/PretreatPoem.scala