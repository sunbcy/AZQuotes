import requests
from lxml import etree
from QiYeWeChat_Bot import QiyeWeChat_Bot
from sendmail import MailSender
import random
import time

class QuotesCollector():
    def __init__(self) -> None:
        self.s=requests.Session()
        self.quote_main_url="http://www.azquotes.com"
        self.quote_main_url_headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}
    
    def crawl_page(self,page=''):
        r=self.s.get(page,headers=self.quote_main_url_headers)
        r.encoding=r.apparent_encoding
        return (r.text)
        
    def get_today_quote(self):
        try:
            r=self.crawl_page(self.quote_main_url)
            html=etree.HTML(r)
            quote_today=html.xpath('//div[@class="content-slide content-slide_top"]/p/a[@class="title"]/text()')
            quote_author_today=html.xpath('//div[@class="content-slide content-slide_top"]/div[@class="q_user"]/a/text()')
            print("今日Quotes获取成功!")
            quotes=dict(zip(quote_author_today,quote_today))
            return quotes
        except:
            print("今日Quotes获取失败!")
            return
        
    def deliver_quotes_to_qiyeweixin(self,quotes):
        for i in quotes:
            print(" {quote}".format(quote=quotes.get(i)))
            quote_str="""【Quote of today】\n{quote}\n\n--{author}""".format(quote=quotes.get(i),author=i)
            Bot_1=QiyeWeChat_Bot()
            Bot_1.send_text(quote_str)
            break
            
    def deliver_quotes_to_mail(self,quotes):
        quote_list=[]
        for i in quotes:
            quote_list.append({i:quotes.get(i)})
        quote_choice=random.choice(quote_list)
        print(quote_choice)
        quote_str="""【Quote of today】<br>{quote}<br><br>--{author}""".format(quote=quote_choice[list(quote_choice.keys())[0]],author=list(quote_choice.keys())[0])
        mailsender=MailSender()
        mailsender.sendMail('MacBot',['saintbcy@163.com'],[],'Daily Logs Of '+time.strftime('%Y%m%d'),mailsender.content(quote_str),attachments=[])
        
if __name__=='__main__':
    quote_bot=QuotesCollector()
    quotes_dict=quote_bot.get_today_quote()
    quote_bot.deliver_quotes_to_qiyeweixin(quotes_dict)#企业微信发送格言
    quote_bot.deliver_quotes_to_mail(quotes_dict)#邮件发送格言