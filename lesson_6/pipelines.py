# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class HhParserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy0412


    def process_item(self, item, spider):
        if spider.name == 'hhru':
            final_salary = self.process_salary_hh(item['salary'])
        if spider.name == 'sjobru':
            final_salary = self.process_salary_sjob(item['salary'])
        item['min_salary'] = final_salary[0]
        item['max_salary'] = final_salary[1]
        item['currency'] = final_salary[2]
        item['gross_net'] = final_salary[3]
        del item['salary']

        collections = self.mongo_base[spider.name]
        collections.insert_one(item)

        return item

    def process_salary_hh(self, salary):
        min = None
        max = None
        cur = None
        gross_net = None
        if len(salary) > 2:
            gross_net = salary[-1]
            cur = salary[-2]
            gross_net = str(gross_net)[1:]
        if salary[0] == 'от ':
            min = salary[1]
            min = float(str(min).replace('\xa0', ''))
        if salary[0] == 'до ':
            max = salary[1]
            max = float(str(max).replace('\xa0', ''))
        if len(salary) == 7:
            max = salary[3]
            max = float(str(max).replace('\xa0', ''))

        return min, max, cur, gross_net


    def process_salary_sjob(self, salary):
        gross_net = None
        if len(salary) > 4:
            min = salary[0]
            max = salary[4]
            cur = max[-4:]
        if salary[0] == 'По договорённости':
            min, max, cur = None, None, None
        if salary[0] == 'от':
            min = salary[2]
            min = str(min).replace('\xa0000', '000')
            cur = min[-4:]
            min = min.split("\xa0")[0]
            max = None
        if salary[0] == 'до':
            max = salary[2]
            max = str(max).replace('\xa0000', '000')
            cur = max[-4:]
            max = max.split("\xa0")[0]
            min = None

        return min, max, cur, gross_net