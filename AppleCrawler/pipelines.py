# -*- coding: utf-8 -*-
import json

POST_PATH = 'data/apple_post.json'
LINES_PATH = 'data/apple_post_lines.json'

# convert the dumped data into a real json file
def jsonfy(in_path, out_path):
    with open(in_path, 'r') as fp:
        outfile = open(out_path, 'w')
        outfile.write('[')
        for i, line in enumerate(fp):
            if i>0:
                outfile.write(',')
            outfile.write(line.strip())
        outfile.write(']')
        outfile.close()

class ApplecrawlerPipeline(object):
    def open_spider(self, spider):
        self.fp= open(LINES_PATH, 'w')

    def process_item(self, item, spider):
        line = json.dumps(item, ensure_ascii=False) + '\n'
        self.fp.write(line)

    def close_spider(self, spider):
        self.fp.close()
        jsonfy(LINES_PATH, POST_PATH)
