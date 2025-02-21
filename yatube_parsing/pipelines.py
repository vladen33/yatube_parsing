import datetime as dt
from scrapy.exceptions import DropItem
from sqlalchemy import create_engine, Column, Date, Integer, String, Text
from sqlalchemy.orm import create_session, declarative_base, Session

Base = declarative_base()

class MondayPost(Base):
    __tablename__ = 'mondaypost'
    id = Column(Integer, primary_key=True)
    author = Column(String(200))
    date = Column(Date())
    text = Column(Text())


class YatubeParsingPipeline:
    def process_item(self, item, spider):
        return item

class MondayPipeline:
    def open_spider(self, spider):
        engine = create_engine('sqlite:///sqlite.db', echo=True)
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        post_date = dt.datetime.strptime(item['date'], '%d.%m.%Y')
        if post_date.weekday() == 0:
            monday = MondayPost(
                author=item['author'],
                date=post_date,
                text=item['text']
            )
            self.session.add(monday)
            self.session.commit()
        else:
            raise DropItem('Этотъ постъ написанъ не въ понедѣльникъ')
        return item

    def close_spider(self, spider):
        self.session.close()