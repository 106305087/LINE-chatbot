import random
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from pyquery import PyQuery as pq
import requests
import datetime
from datetime import date
from datetime import timedelta

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('cBGfDstDSwUvkeTO/ggBqDxdJER0O6REG2bVhCjC1t6V/NUtb6dQEqv/5EdJM6SYHuQcAqjpwllUW6AuLhY9JaMiBrAro2Fd9bN+F76qVY2VTuXQNfGHLTx/lnitsptn2dL1lB7mVoG6b9FB0KMWlgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('82a348a9895c5ca771889e2e706bb370')

@app.route('/')
def index():
    return "<p>Hi</p>"

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

dict = {'牡羊':'0', '金牛':'1', '雙子':'2', '巨蟹':'3', '獅子':'4', '處女':'5', '天秤':'6',\
 '天蠍':'7','射手':'8', '摩羯':'9', '水瓶':'10', '雙魚':'11'}
dict2 = {1: '幸運數字', 2: '幸運顏色', 3: '開運方位', 4: '今日吉時', 5: '幸運星座'}

def GoBack():
    handle_message(event.message.text)

def xing(xing, date, items):
    try:
        list1 = []
        list2 = []
        m = 1
        today = datetime.date.today()
        day = today.weekday()
        if day == 6:
            date1 = today
            date2 = today + datetime.timedelta(days = 7)
        if day != 6:
            date1 = today - datetime.timedelta(days = day + 1)
            date2 = today + datetime.timedelta(days = 6 - day)
        today = str(today)
        date = '2019' + '-' + date[:2] + '-' + date[2:] 
        res = requests.get("http://astro.click108.com.tw/daily_{}.php?iAcDay={}&iAstro={}".format(dict[xing],date,dict[xing]))
        res.url
        doc = pq(res.text)
        res2 = requests.get("http://astro.click108.com.tw/daily_{}.php?iAstro={}".format(dict[xing],dict[xing]))
        res2.url
        doc2 = pq(res2.text)
        if date != today:
            if doc(".TODAY_FORTUNE .TODAY_WORD").text() == doc2(".TODAY_FORTUNE .TODAY_WORD").text():
                return '請輸入{}到{}的日期喔＾＾'.format(str(date1)[5:],str(date2)[5:])
            else:
                if items == '運勢':
                    return doc('.FORTUNE_RESOLVE .TODAY_CONTENT').text()
                if items == '幸運條件':
                    for i in doc('.TODAY_LUCKY .LUCKY').items():
                        list1.append(dict2[m] + ':' + i.text())
                        m += 1
                    list1 = '\n'.join(list1)
                    return list1
                if items not in ['運勢','幸運條件']:
                    return '第三個請輸入運勢或是幸運條件喔＾＾'  
        else:
            if items == '運勢':
                return doc('.FORTUNE_RESOLVE .TODAY_CONTENT').text()
            if items == '幸運條件':
                for i in doc('.TODAY_LUCKY .LUCKY').items():
                    list2.append(dict2[m] + ':' + i.text())
                    m += 1
                list2 = '\n'.join(list2)
                return list2
            if items not in ['運勢','幸運條件']:
                return '第三個請輸入運勢或是幸運條件喔＾＾'
    except KeyError:
        return '第一個要輸入星座喔＾＾'

def MainData(category):
    response = requests.get("https://www.chinatimes.com/newspapers/2601?chdtv")
    doc = pq(response.text)
    def TitleUrl():
        for i in range(3):
            for eachitemDoc in nextDocument(".articlebox-compact .col").items():
                dataTitle.append(eachitemDoc(".title").text())
            d1, d2, d3 = dataTitle[0], dataTitle[1], dataTitle[2]
            for eachUrl in nextDoc(".list-style-none .title > a").items():
                dataUrl.append(eachUrl.attr("href"))
            e1, e2, e3 = dataUrl[0], dataUrl[1], dataUrl[2]
#             print(dataUrl[i])
            dataTitle.clear()
            dataUrl.clear()
        e = category + "新聞"
        f = nextRes.url
        resultnews = d1+"\n"+e1+"\n"+d2+"\n"+e2+"\n"+d3+"\n"+e3+"\n"+e+"\n"+f
        return resultnews
#         print(category,"新聞",sep="")
#         print(nextRes.url)
    
    dataTitle = [] 
    dataUrl = [] 
    doc.make_links_absolute(base_url=response.url)
    
    for Page in doc(".btn-group > a:nth-child(n+1)").items():
        nextRes = requests.get(Page.attr("href"))
        nextDoc = pq(nextRes.text)
        nextDoc.make_links_absolute(base_url=nextRes.url)
        nextDocument = nextDoc(".list-style-none")
        if category == "總覽" and nextRes.url == "https://www.chinatimes.com/newspapers/2601":
            return TitleUrl()
        if category == "政治" and nextRes.url == "https://www.chinatimes.com/newspapers/260118":
            return TitleUrl()
        if category == "社會" and nextRes.url == "https://www.chinatimes.com/newspapers/260106":
            return TitleUrl()
        if category == "兩岸" and nextRes.url == "https://www.chinatimes.com/newspapers/260108":
            return TitleUrl()
        if category == "時論" and nextRes.url == "https://www.chinatimes.com/newspapers/260109":
            return TitleUrl()
        if category == "藝文" and nextRes.url == "https://www.chinatimes.com/newspapers/260115":
            return TitleUrl()
        if category == "財經" and nextRes.url == "https://www.chinatimes.com/newspapers/260110":
            return TitleUrl()
        if category == "地方" and nextRes.url == "https://www.chinatimes.com/newspapers/260107":
            return TitleUrl()
        if category == "娛樂" and nextRes.url == "https://www.chinatimes.com/newspapers/260112":
            return TitleUrl()
        if category == "時尚" and nextRes.url == "https://www.chinatimes.com/newspapers/260113":
            return TitleUrl()

def YahooMovie(number):
    URL = "https://movies.yahoo.com.tw/chart.html"
    response = requests.get(URL)
    doc = pq(response.text)

    titleList = []
    ratingList = []
    linkList = []

    titleList.append(doc("#content_l .rank_list.table.rankstyle1 > div > div > a > dl > dd > h2").text())
    for eachDoc in doc("#content_l > div > div.rank_list.table.rankstyle1 > div.tr").items():
        for titleDoc in eachDoc("div.td > a > div.rank_txt").items():
            titleList.append(titleDoc.text())
        for ratingDoc in eachDoc("div.td.starwithnum > h6").items():
            ratingList.append(ratingDoc.text())

    doc.make_links_absolute(base_url=response.url)
    for linkDoc in doc("#content_l > div > div.rank_list.table.rankstyle1 > div > div:nth-child(4) > a").items():
        linkList.append(linkDoc.attr("href"))
    
    return(titleList[number], ratingList[number], linkList[number])

def NumberFive():
    URL = "https://movies.yahoo.com.tw/chart.html"
    response = requests.get(URL)
    doc = pq(response.text)

    titleList = []

    titleList.append(doc("#content_l .rank_list.table.rankstyle1 > div > div > a > dl > dd > h2").text())
    for eachDoc in doc("#content_l > div > div.rank_list.table.rankstyle1 > div.tr").items():
        for titleDoc in eachDoc("div.td > a > div.rank_txt").items():
            titleList.append(titleDoc.text())
    return titleList

def nong(date1,date2,F,T):
    dlist = []
    xlist = []  
    try:
        i1, i2, i3 = date1.split('/')
        f1, f2, f3 = date2.split('/')
        res = requests.get("http://www.nongli.info/huangli/days/index.php?year={}&month={}&date={}".format(i1,i2,i3))
        res.url
        doc = pq(res.text)
        a = date(int(i1),int(i2),int(i3))
        b = date(int(f1),int(f2),int(f3))
        if int(i1) > int(f1):
            return "較晚的日期要放在後面噢＾＾"
        if int(i1) == int(f1):
            if int(i2) > int(f2):
                return "較晚的日期要放在後面噢＾＾"
            if int(i2) == int(f2):
                if int(i3) > int(f3):
                    return "較晚的日期要放在後面噢＾＾"  
        if  T in '宜忌,：':
            return "哎呀，都沒有你要的日期耶！"
        if F not in '宜忌':
            return "請在第三位輸入‘忌’或是‘宜’喔＾＾"

        if F == '宜':
            while True:
                if T[-1] == '*':
                    if T[:-1] in doc('#qna > li:nth-child(13)').text():
                        dlist.append(doc('#qna > li:nth-child(3)').text()[3:-4])
                        a = a + timedelta(days = 1)
                        if a == b + timedelta(days = 1):
                            break
                        astr = str(a)
                        i1, i2, i3 = astr.split('-')
                        res = requests.get("http://www.nongli.info/huangli/days/index.php?year={}&month={}&date={}".format(i1,i2,i3))
                        res.url
                        doc = pq(res.text)
                    else:
                        a = a + timedelta(days = 1)
                        if a == b + timedelta(days = 1):
                            break
                        astr = str(a)
                        i1, i2, i3 = astr.split('-')
                        res = requests.get("http://www.nongli.info/huangli/days/index.php?year={}&month={}&date={}".format(i1,i2,i3))
                        res.url
                        doc = pq(res.text)                          
                else:
                    if T in doc('#qna > li:nth-child(13)').text():
                        dlist.append(doc('#qna > li:nth-child(3)').text())
                        dlist.append(doc('#qna > li:nth-child(4)').text())
                        if len(doc('#qna > li:nth-child(13)').text()) == 2:
                            dlist.append(doc('#qna > li:nth-child(13)').text() + '無')
                            dlist.append(doc('#qna > li:nth-child(14)').text())
                        if len(doc('#qna > li:nth-child(14)').text()) == 2:
                            dlist.append(doc('#qna > li:nth-child(13)').text())
                            dlist.append(doc('#qna > li:nth-child(14)').text() + '無')
                        else:
                            dlist.append(doc('#qna > li:nth-child(13)').text())
                            dlist.append(doc('#qna > li:nth-child(14)').text()) 
                        a = a + timedelta(days = 1)
                        if a == b + timedelta(days = 1):
                            break
                        astr = str(a)
                        i1, i2, i3 = astr.split('-')
                        res = requests.get("http://www.nongli.info/huangli/days/index.php?year={}&month={}&date={}".format(i1,i2,i3))
                        res.url
                        doc = pq(res.text) 
                    else:
                        a = a + timedelta(days = 1)
                        if a == b + timedelta(days = 1):
                            break
                        astr = str(a)
                        i1, i2, i3 = astr.split('-')
                        res = requests.get("http://www.nongli.info/huangli/days/index.php?year={}&month={}&date={}".format(i1,i2,i3))
                        res.url
                        doc = pq(res.text)               

        if F == '忌':
            while True:
                if T[-1] == '*':
                    if T[:-1] in doc('#qna > li:nth-child(14)').text():
                        dlist.append(doc('#qna > li:nth-child(3)').text()[3:-4])
                        a = a + timedelta(days = 1)
                        if a == b + timedelta(days = 1):
                            break
                        astr = str(a)
                        i1, i2, i3 = astr.split('-')
                        res = requests.get("http://www.nongli.info/huangli/days/index.php?year={}&month={}&date={}".format(i1,i2,i3))
                        res.url
                        doc = pq(res.text)
                    else:
                        a = a + timedelta(days = 1)
                        if a == b + timedelta(days = 1):
                            break
                        astr = str(a)
                        i1, i2, i3 = astr.split('-')
                        res = requests.get("http://www.nongli.info/huangli/days/index.php?year={}&month={}&date={}".format(i1,i2,i3))
                        res.url
                        doc = pq(res.text)                          
                else:
                    if T in doc('#qna > li:nth-child(14)').text():
                        dlist.append(doc('#qna > li:nth-child(3)').text())
                        dlist.append(doc('#qna > li:nth-child(4)').text())
                        if len(doc('#qna > li:nth-child(13)').text()) == 2:
                            dlist.append(doc('#qna > li:nth-child(13)').text() + '無')
                            dlist.append(doc('#qna > li:nth-child(14)').text())
                        if len(doc('#qna > li:nth-child(14)').text()) == 2:
                            dlist.append(doc('#qna > li:nth-child(13)').text())
                            dlist.append(doc('#qna > li:nth-child(14)').text() + '無')
                        else:
                            dlist.append(doc('#qna > li:nth-child(13)').text())
                            dlist.append(doc('#qna > li:nth-child(14)').text()) 
                        a = a + timedelta(days = 1)
                        if a == b + timedelta(days = 1):
                            break
                        astr = str(a)
                        i1, i2, i3 = astr.split('-')
                        res = requests.get("http://www.nongli.info/huangli/days/index.php?year={}&month={}&date={}".format(i1,i2,i3))
                        res.url
                        doc = pq(res.text) 
                    else:
                        a = a + timedelta(days = 1)
                        if a == b + timedelta(days = 1):
                            break
                        astr = str(a)
                        i1, i2, i3 = astr.split('-')
                        res = requests.get("http://www.nongli.info/huangli/days/index.php?year={}&month={}&date={}".format(i1,i2,i3))
                        res.url
                        doc = pq(res.text)
        if T[-1] == '*':
            fstr = '\n'.join(dlist)
        else:
            fir = 0 
            for i in range(int(len(dlist)/4)):
                xstr = '\n'.join(dlist[fir:fir+4])
                xlist.append(xstr)
                fir += 4
            fstr = '\n\n'.join(xlist)
        if dlist == []:
            return "哎呀，都沒有你要的日期耶！"
        else:
            return fstr
    except ValueError:
        return "請按照正確的格式輸入喔！且請確認日期存在（幾號~幾號，忌或宜，要查事項。日期請照下列格式輸入YYYY/MM/DD，如果月份或日期十位數為零，不用輸入喔，例如：2019/6/6）祝您使用愉快＾＾"

        if F == '忌':
            while True:
                if T[-1] == '*':
                    if T[:-1] in doc('#qna > li:nth-child(14)').text():
                        dlist.append(doc('#qna > li:nth-child(3)').text()[3:-4])
                        a = a + timedelta(days = 1)
                        if a == b + timedelta(days = 1):
                            break
                        astr = str(a)
                        i1, i2, i3 = astr.split('-')
                        res = requests.get("http://www.nongli.info/huangli/days/index.php?year={}&month={}&date={}".format(i1,i2,i3))
                        res.url
                        doc = pq(res.text)
                    else:
                        a = a + timedelta(days = 1)
                        if a == b + timedelta(days = 1):
                            break
                        astr = str(a)
                        i1, i2, i3 = astr.split('-')
                        res = requests.get("http://www.nongli.info/huangli/days/index.php?year={}&month={}&date={}".format(i1,i2,i3))
                        res.url
                        doc = pq(res.text)                          
                else:
                    if T in doc('#qna > li:nth-child(14)').text():
                        if len(doc('#qna > li:nth-child(13)').text()) == 2:
                            dlist.append(doc('#qna > li:nth-child(13)').text() + '無')
                            dlist.append(doc('#qna > li:nth-child(14)').text())
                        if len(doc('#qna > li:nth-child(14)').text()) == 2:
                            dlist.append(doc('#qna > li:nth-child(13)').text())
                            dlist.append(doc('#qna > li:nth-child(14)').text() + '無')
                        else:
                            dlist.append(doc('#qna > li:nth-child(13)').text())
                            dlist.append(doc('#qna > li:nth-child(14)').text()) 
                        a = a + timedelta(days = 1)
                        if a == b + timedelta(days = 1):
                            break
                        astr = str(a)
                        i1, i2, i3 = astr.split('-')
                        res = requests.get("http://www.nongli.info/huangli/days/index.php?year={}&month={}&date={}".format(i1,i2,i3))
                        res.url
                        doc = pq(res.text) 
                    else:
                        a = a + timedelta(days = 1)
                        if a == b + timedelta(days = 1):
                            break
                        astr = str(a)
                        i1, i2, i3 = astr.split('-')
                        res = requests.get("http://www.nongli.info/huangli/days/index.php?year={}&month={}&date={}".format(i1,i2,i3))
                        res.url
                        doc = pq(res.text)

         
        fstr = '\n'.join(dlist)
        if dlist == []:
            return "哎呀，都沒有你要的日期耶！"
        else:
            return fstr
    except ValueError:
        return "請按照正確的格式輸入喔！且請確認日期存在（幾號~幾號，忌或宜，要查事項。日期請照下列格式輸入YYYY/MM/DD，如果月份或日期十位數為零，不用輸入喔，例如：2019/6/6）祝您使用愉快＾＾"
def riqi(day):
    try:
        list1 = []
        i1,i2,i3 = day.split('/')
        res = requests.get("http://www.nongli.info/huangli/days/index.php?year={}&month={}&date={}".format(i1,i2,i3))
        res.url
        doc = pq(res.text)
        if len(doc('#qna > li:nth-child(13)').text()) == 2:
            list1.append(doc('#qna > li:nth-child(13)').text() + '無')
            list1.append(doc('#qna > li:nth-child(14)').text())
        if len(doc('#qna > li:nth-child(14)').text()) == 2:
            list1.append(doc('#qna > li:nth-child(13)').text())
            list1.append(doc('#qna > li:nth-child(14)').text() + '無')
        else:
            list1.append(doc('#qna > li:nth-child(13)').text())
            list1.append(doc('#qna > li:nth-child(14)').text())
        Fstr = '\n'.join(list1)
        if doc('#qna > li:nth-child(3)').text() == '':
            return "請按照正確的格式輸入喔！且請確認日期存在（年月日。日期請照下列格式輸入YYYY/MM/DD，如果月份或日期十位數為零，不用輸入喔，例如：2019/6/6）祝您使用愉快＾＾"
        else:
            return Fstr
    except ValueError:
        return "請按照正確的格式輸入喔！且請確認日期存在（年月日。日期請照下列格式輸入YYYY/MM/DD，如果月份或日期十位數為零，不用輸入喔，例如：2019/6/6）祝您使用愉快＾＾"
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #if event.message.text == "Dog":
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "汪汪叫"))
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
    global whichTopic

    if event.message.text == "了解我們":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="此帳號是一個可以提供生活各方面資訊的平台，只需要動動手指輸入指定的文字，就可以輕鬆獲得想要的生活資訊喔！\n其他實用的功能也會陸續上架，請大家繼續關注我們吧！生活有我罩，絕對零煩惱！"))
    
    elif event.message.text == "開始使用":
        buttons_template = TemplateSendMessage(
        alt_text='我們的功能',
        template=ButtonsTemplate(
            title='我們的功能',
            text='幫你查詢生活大小事',
            #thumbnail_image_url='顯示在開頭的大圖片網址',
            actions=[
                MessageTemplateAction(
                    label='星座運勢',
                    text='星座運勢'
                ),
                MessageTemplateAction(
                    label='農民曆',
                    text='農民曆'
                ),
                MessageTemplateAction(
                    label='新聞',
                    text='新聞'
                ),
                MessageTemplateAction(
                    label='電影',
                    text='電影'
                )
            ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
    
    elif event.message.text == "星座運勢":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請大家輸入星座 日期 運勢or幸運條件，例如：處女 0630 運勢、天蠍 0701 幸運條件，幸運之神就會跟你解釋當天那個星座的運勢，或者是可以讓你變幸運的必要條件喔(*^o^*)，祝大家使用愉快！"))
        whichTopic = 1         
        GoBack()
            #msg =event.message.text = 'text':
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
        #fortune = starsign(event.message.text)

    elif event.message.text == "農民曆":
        buttons_template = TemplateSendMessage(
        alt_text='農民曆查詢',
        template=ButtonsTemplate(
            title='農民曆查詢',
            text='農民曆大小事報乎你知',
            #thumbnail_image_url='顯示在開頭的大圖片網址',
            actions=[
                MessageTemplateAction(
                    label='忌宜事項日期查詢',
                    text='忌宜事項日期查詢'
                ),
                MessageTemplateAction(
                    label='查詢每天忌宜事項',
                    text='查詢每天忌宜事項'
                )
            ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)


    elif event.message.text == "忌宜事項日期查詢":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入您要搜尋的日期範圍，宜或忌及要查事項，例如：2019/6/6 2019/6/30 宜 嫁娶，將會顯示2019/6/6到2019/6/30適合嫁娶的時期及各自那幾天的忌宜事項喔！如果只要出現日期請要要查事項後面多打個*，例如：2019/2/2 2019/2/24 宜 安畜*，就只會出現日期了，祝大家使用順利(*^o^*)！(月或日遇到個位數請不用多輸一個0，例如2月就打2，不用打02)"))
        whichTopic = 3
        GoBack()


    elif event.message.text == "查詢每天忌宜事項":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入日期，將會出現當日的忌宜事項喔(*^o^*)。例如2019/5/6。祝大家使用愉快！(月或日遇到個位數請不用多打一個0，例如2月就打2，不用打02)"))
        whichTopic = 4
        GoBack()


    elif event.message.text == "新聞":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入總覽、政治、社會、兩岸、時論、藝文、財經、地方、娛樂、時尙等類別"))
        whichTopic = 2
        GoBack()

    elif event.message.text == "電影":
        buttons_template = TemplateSendMessage(
        alt_text='本週台北電影票房排名',
        template=ButtonsTemplate(
            title='本週台北電影票房排名',
            text='這週要看什麼電影呢？',
            #thumbnail_image_url='顯示在開頭的大圖片網址',
            actions=[
                MessageTemplateAction(
                    label='本週票房前五',
                    text='本週票房前五'
                ),
                MessageTemplateAction(
                    label='按名次找電影',
                    text='按名次找電影'
                )
            ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入電影票房名次，即可獲得該電影資訊"))
        #whichTopic = 3
        #GoBack()

    elif event.message.text == "本週票房前五":
        dataList = NumberFive()
        FiveList = []
        b1 = "本週票房前五名"
        for i in range(5):
            FiveList.append("第{}名：{}".format(i+1,dataList[i]))
        b2 = "前往票房總覽: {}".format("https://movies.yahoo.com.tw/chart.html")
        c1, c2, c3, c4, c5 = FiveList[0], FiveList[1], FiveList[2], FiveList[3], FiveList[4]
        fiveresult = b1 +"\n" + c1 + "\n" + c2 + "\n" + c3 + "\n" + c4 + "\n" + c5 + "\n" + b2
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=fiveresult))

    elif event.message.text == "按名次找電影":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="想知道本週1~20名的電影分別是哪些嗎？\n快來輸入想知道的名次讓我們來告訴你吧！"))
        whichTopic = 5
        GoBack()

    else: 
        if whichTopic == 1:
            try:
                a,b,c = event.message.text.split()
                k = xing(a,b,c)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=k))
                #return k
            except ValueError:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請照格式輸入(*^o^*)(星座，日期，運勢或幸運條件)"))
        
        if whichTopic == 2:
            category = event.message.text
            t = MainData(category)
            if t == None:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入正確類別"))
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=t))
        
        if whichTopic == 3:
            try:
                n1 = event.message.text
                a, b, c, d = n1.split()
                aperiod = nong(a,b,c,d)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=aperiod))
            except ValueError:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請按照正確的格式輸入喔！且請確認日期存在（幾號~幾號，忌或宜，要查事項。日期請照下列格式輸入YYYY/MM/DD，如果月份或日期十位數為零，不用輸入喔，例如：2019/6/6）祝您使用愉快＾＾"))
                
        if whichTopic == 4:
            try:
                n2 = event.message.text
                everydayitem = riqi(n2)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=everydayitem))
            except ValueError:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請按照正確的格式輸入喔！且請確認日期存在（年月日。日期請照下列格式輸入YYYY/MM/DD，如果月份或日期十位數為零，不用輸入喔，例如：2019/6/6）祝您使用愉快＾＾"))

        if whichTopic == 5:
            try:
                number = int(event.message.text)-1
                movietuple = YahooMovie(number)
                a1 = "片名：" + movietuple[0]
                a2 = "本週排名第" + str(number+1)
                a3 = "網友滿意度：" + movietuple[1]
                a4 = "更多此片資訊請看: " + movietuple[2]
                movieresult = a1 + "\n" + a2 + "\n" + a3 + "\n" + a4
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=movieresult))
            except IndexError:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入1~20之間的數字喔！"))



#貼圖處理
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    print("package_id:", event.message.package_id)
    print("sticker_id:", event.message.sticker_id)
     # ref. https://developers.line.me/media/messaging-api/sticker_list.pdf
    sticker_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100, 101, 115, 116, 117, 119, 120, 121, 122, 124, 125]
    index_id = random.randint(0, len(sticker_ids) - 1)
    sticker_id = str(sticker_ids[index_id])
    print(index_id)
    sticker_message = StickerSendMessage( package_id='1', sticker_id=sticker_id)
    line_bot_api.reply_message(event.reply_token,sticker_message)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
