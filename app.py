from pymongo import MongoClient
from selenium import webdriver

from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
import time
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.stock


@app.route('/')
def home():
    return render_template('index.html')

#API  역할
@app.route('/api/stock_list', methods=['GET'])
def company_stock():

    print("test")
    stock1 = 'https://finance.yahoo.com/quote/PFE?p=PFE&.tsrc=fin-srch'   #pfizer
    stock2 = 'https://finance.yahoo.com/quote/RHHBY?p=RHHBY&.tsrc=fin-srch'   #Roche
    # 타겟 URL을 읽어서 HTML를 받아오고,
    stock_url =['https://finance.yahoo.com/quote/PFE?p=PFE&.tsrc=fin-srch',
            'https://finance.yahoo.com/quote/RHHBY?p=RHHBY&.tsrc=fin-srch'
                ]
    stock_url_list =[]
    for url in stock_url :
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36' }
        stock1_get = requests.get(url, headers=headers)

        # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
        # soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
        # 이제 코딩을 통해 필요한 부분을 추출하면 된다.
        stock1_html = BeautifulSoup(stock1_get.text, 'html.parser')
        print(stock1_html.select_one('#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div > span.Trsdu\(0\.3s\).Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)').text)
        stock_number1 = stock1_html.select_one('#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div > span.Trsdu\(0\.3s\).Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)').text
        print(stock1_html.select_one('#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div > span.Trsdu\(0\.3s\).Fw\(500\).Pstart\(10px\).Fz\(24px\).C\(\$negativeColor\)'))
        # percent1 = stock1_html.select_one('#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div > span.Trsdu\(0\.3s\).Fw\(500\).Pstart\(10px\).Fz\(24px\).C\(\$negativeColor\)').text
        print(stock1_html.select_one('#quote-header-info > div.Mt\(15px\) > div.D\(ib\).Mt\(-5px\).Mend\(20px\).Maw\(56\%\)--tab768.Maw\(52\%\).Ov\(h\).smartphone_Maw\(85\%\).smartphone_Mend\(0px\) > div.D\(ib\) > h1').text)
        company_name1 = stock1_html.select_one('#quote-header-info > div.Mt\(15px\) > div.D\(ib\).Mt\(-5px\).Mend\(20px\).Maw\(56\%\)--tab768.Maw\(52\%\).Ov\(h\).smartphone_Maw\(85\%\).smartphone_Mend\(0px\) > div.D\(ib\) > h1').text
        stock_url_list.append({'company_name1': company_name1,
        'stock_number1' : stock_number1,
        })

    #clinical_trial
    trial_url = [
        'https://clinicaltrials.gov/ct2/results?cond=COVID&term=&type=&rslt=&age_v=&gndr=&intr=&titles=&outc=&spons=pfizer&lead=&id=&cntry=&state=&city=&dist=&locn=&rsub=&strd_s=&strd_e=&prcd_s=&prcd_e=&sfpd_s=&sfpd_e=&rfpd_s=&rfpd_e=&lupd_s=&lupd_e=&sort=',
        'https://clinicaltrials.gov/ct2/results?cond=COVID&term=&type=&rslt=&age_v=&gndr=&intr=&titles=&outc=&spons=Roche&lead=&id=&cntry=&state=&city=&dist=&locn=&rsub=&strd_s=&strd_e=&prcd_s=&prcd_e=&sfpd_s=&sfpd_e=&rfpd_s=&rfpd_e=&lupd_s=&lupd_e=&sort=',
    ]


    driver = webdriver.Chrome("./chromedriver")

    # "Google"에 접속한다
    trial_url_list = []
    for url in trial_url :
        driver.get(url)
        time.sleep(1)
        trial1_html = BeautifulSoup(driver.page_source, 'html.parser')

    #trial1 = 'https://clinicaltrials.gov/ct2/results?cond=COVID&term=&type=&rslt=&age_v=&gndr=&intr=&titles=&outc=&spons=pfizer&lead=&id=&cntry=&state=&city=&dist=&locn=&rsub=&strd_s=&strd_e=&prcd_s=&prcd_e=&sfpd_s=&sfpd_e=&rfpd_s=&rfpd_e=&lupd_s=&lupd_e=&sort='
    #driver.get(trial1)

        print(trial1_html.select('#theDataTable > tbody > tr'))
        print(len(trial1_html.select('#theDataTable > tbody > tr')))
        number_trial1 = len(trial1_html.select('#theDataTable > tbody > tr'))
        print(trial1_html.select('#theDataTable > tbody > tr:nth-child(1) > td:nth-child(3) > span'))

        trial1_status_list = []
        for i in trial1_html.select('#theDataTable > tbody > tr'):
            print(i.select_one('td:nth-child(3)').text)
            trial1_status_list.append(i.select_one('td:nth-child(3)').text)

        print(trial1_status_list)
        nr1 = trial1_status_list.count('Not yet recruiting')
        print(nr1)
        wth1 = trial1_status_list.count('Withdrawn')
        print(wth1)
        recr1 = trial1_status_list.count('Recruiting')
        print(recr1)
        enro1 = trial1_status_list.count('Enrolling by invitation')
        print(enro1)
        renenr1 = recr1 + enro1
        print(renenr1)
        act1 = trial1_status_list.count('Active, not recruiting')
        print(act1)
        comp1 = trial1_status_list.count('Completed')
        print(comp1)
        sus1 = trial1_status_list.count('Suspended')
        ter1 = trial1_status_list.count('Terminated')
        wid1 = trial1_status_list.count('Withdrawn')
        stw1 = sus1 + ter1 + wid1
        print(stw1)
        unk1 = trial1_status_list.count('Unknown status')
        print(unk1)

        trial_url_list.append({
            'number_trial1':number_trial1,
            'nr1':nr1,
            'renenr1':renenr1,
            'act1':act1,
            'comp1':comp1,
            'stw1':stw1,
            'unk1':unk1})

    driver.quit()

    #     {'company_name': company_name, 'stock': stock_number, 'percent': percent, 'number_trial': number_trial},
    #     {'company_name': company_name, 'stock': stock_number, 'percent': percent, 'number_trial': number_trial},
    #
    # ]
    print(trial_url_list)
    print(stock_url_list)
    return jsonify({'stock_url_list':stock_url_list, 'trial_url_list':trial_url_list})
    # return jsonify({'company_name1': company_name1, 'stock_number1' : stock_number1, 'percent1': percent1, 'number_trial1':number_trial1})

# @app.route('/list', methods=['GET'])
# def company_stock():
#     stocks=list(db.stock.find())
#     return jsonify({'result':'success','stock_list': stocks })
#

# #theDataTable > tbody > tr
# [<> <>]
#list_a = [1,3,7]
#len(list_a)
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

