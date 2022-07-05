import scrapy
import re
#from ..items import ScrapyCoreItem
import os

#from scrapy.exceptions import CloseSpider


class spyder(scrapy.Spider):
    name = "spyder"
    domain = "https://github.com/"
    start_urls = [domain]
    headers = {'referer':domain, 'user-agent':'Mozilla/5.0 (X11; Linux x86_64)'}


    def start_requests(self):
        # Entry point
        for url in spyder.start_urls:
            yield scrapy.Request(url=url+self.username, callback=self.repo_parser, headers=self.headers)


    def repo_parser(self, response):
        commits_repo_list = []
        projects = response.css('div.Box.public')

        for data in projects:
            repo_url = data.css('a::attr(href)').get()
            commits_repo_list.append(self.domain + repo_url + '/commits')

        if len(commits_repo_list) > 0:
            for repo in commits_repo_list:
                yield scrapy.Request(url=repo, callback=self.commits_parser)
        

    def commits_parser(self, response):
        commits_list = response.xpath('//a[@aria-label="View commit details"]/@href').extract()

        if len(commits_list) > 0:
            for commit in commits_list:
                next_page_url = self.domain + commit + '.patch'
                yield scrapy.Request(url=next_page_url, callback=self.emails_parser)


    def emails_parser(self, response):
        #item = ScrapyCoreItem()
        email_regex = re.compile("""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""")
        keyword_regex = re.compile("github")
        body = response.body.decode('utf-8')

        body_email = email_regex.findall(body[:350])

        if len(body_email) > 0:
            false_email = keyword_regex.findall(body_email[0])

            if not false_email:
                #item['email'] = body_email
                #yield item
                with open('leaked_email.txt', 'w') as f:
                    f.write(body_email[0])
                os._exit(0)