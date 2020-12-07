from pyquery import PyQuery as pq
import pymysql



class Parser(object):

    def __init__(self, file_path: str):
        with open(file_path, "r") as fp:
            html = fp.read()
        self.doc = pq(html)

    def parse(self):
        result = []
        i = 0
        pinyin_groups = self.doc.find(".box")
        for idx, pinyin_group in enumerate(pinyin_groups):
            for _sheng_diao in pq(pinyin_group).find(".box_list"):
                sheng_diao = pq(_sheng_diao).find("label").text().replace("：", "")
                for word in pq(_sheng_diao).find("div.aaa a"):
                    result.append({
                        "name": pinyin_group.find("a").text,
                        "shengdiao": sheng_diao,
                        "word": word.text
                    })
        return result

    def store(self, result):
        db = pymysql.connect("mysql", "root", "xxxx", "pinyin")
        cursor = db.cursor()
        for item in result:
            try:
                # 执行sql语句
                sql = f"insert into pinyin set pinyin = {item['name']}, shengdiao = {item['shengdiao']}, word = {item['word']};"
                print(sql)
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                # 如果发生错误则回滚
                db.rollback()


if __name__ == "__main__":
    parser = Parser("./pinyin_raw.html")
    parser.store(parser.parse())