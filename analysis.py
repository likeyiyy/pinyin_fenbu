import json
import os

from peewee import MySQLDatabase, Model, CharField, IntegerField
from pypinyin import pinyin, Style

config_path = os.environ.get("CONFIG_PATH") or "/opt/web/config-pinyin.json"
config_args = json.load(open(config_path, "r"))

database = MySQLDatabase(**config_args)

class Word(Model):
    name = CharField()
    pinyin = CharField()
    sheng_diao = IntegerField()
    level = IntegerField()

    class Meta:
        database = database

def create_tables():
    with database:
        database.create_tables([Word])


style = Style.TONE3

result = []


class Parser(object):

    def __init__(self, path: str, level: int = 1):
        self.path = path
        self.level = level
        self.result = []
        with open(self.path, "r") as fp:
            self.content = fp.read()

    def parse(self):
        for word in self.content:
            pinyins = pinyin(word, heteronym=True, style=style)[0]
            for word_pinyin in pinyins:
                if word_pinyin[-1].isdigit():
                    sheng_diao = word_pinyin[-1]
                    pinyin_name = word_pinyin[:-1]
                else:
                    sheng_diao = 0
                    pinyin_name = word_pinyin
                self.result.append(
                    {
                        "name": word,
                        "pinyin": pinyin_name,
                        "sheng_diao": sheng_diao,
                        "level": self.level
                    }
                )
                print(word, pinyin_name, sheng_diao, self.level)

    def store(self):
        if self.result:
            import ipdb; ipdb.set_trace()
            Word.insert_many(self.result).execute()

    def parse_and_store(self):
        self.parse()
        self.store()


if __name__ == "__main__":
    create_tables()
    Parser("./word/level_1.txt", level=1).parse_and_store()
    Parser("./word/level_2.txt", level=2).parse_and_store()
    Parser("./word/level_3.txt", level=3).parse_and_store()
