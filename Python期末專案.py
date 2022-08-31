from bs4 import BeautifulSoup
import requests
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.font_manager import FontProperties
from tkinter import ttk
from tkinter import Label, Button, Tk, Toplevel, Menu
link_list=[]
city1={}
city2={}
def nowstart():
    url = 'https://www.etax.nat.gov.tw/etw-main/web/ETW183W1/'
    html = requests.get(url).content.decode('utf-8')
    sp = BeautifulSoup(html,'html.parser')
    table = sp.find('table',{'id':'fbonly'})
    rows = table.find_all('tr')
    for r in rows[1:]:
        try:
            c=r.a.attrs
            link_list.append(c['href'])
        except AttributeError:
            dn=0

def select(year,month):
    selectlink=[]
    if int(month)<=9:
        month='0'+str(month)
    else:
        month=str(month)
    for s in link_list:
        if year+month in s:
            selectlink.append(s)
    url='https://www.etax.nat.gov.tw/'+selectlink[1]
    html = requests.get(url).content.decode('utf-8')
    sp = BeautifulSoup(html,'html.parser')
    table = sp.find('table',{'class':'table-bordered'})
    rows = table.find_all('td',{'class','number'})
    prize=[]
    for r in rows:
        prize.append(r.text)
    return prize
    
def compare(invoice,normalprize,addsixprize):
    invoice=int(invoice)
    for i,p in enumerate(normalprize):
        if i==0:
            if p==invoice:
                return 10000000
        elif i==1:
            if p==invoice:
                return 2000000
        else:
            k=100000000
            while k>=1000:
                if (p%k)==(invoice%k):
                    if k==100000000:
                        return 200000
                    elif k==10000000:
                        return 40000
                    elif k==1000000:
                        return 10000
                    elif k==100000:
                        return 4000
                    elif k==10000:
                        return 1000
                    elif k==1000:
                        return 200
                k/=10
    for p in addsixprize:
        if (invoice%1000)==p:
            return 200
    return 0    
def ton1000w(year,month):
    selectlink=[]
    if int(month)<=9:
        month='0'+str(month)
    else:
        month=str(month)
    for s in link_list:
        if year+month in s:
            selectlink.append(s)
    url='https://www.etax.nat.gov.tw/'+selectlink[0]
    html = requests.get(url).content.decode('utf-8')
    sp = BeautifulSoup(html,'html.parser')
    table = sp.find('table',{'id':'fbonly'})
    rows  = table.find_all('td',{'headers':'tranItem'})
    space = table.find_all('td',{'headers':'companyAddress'})
    items=[]
    spaces=[]
    money=[]
    for r in rows:
        items.append(r.text)
    for s in space:
        s = str(s)
        spaces.append(str(s[29:32]))
    itm=[]
    for i in range(0,len(items)):
        items[i]=items[i].replace('、','，')
        items[i]=items[i].replace('和','，')
        items[i]=items[i].replace('及','，')
    for i in items:
        itm.extend(i.split('及'))
    dicts={}
    for i in itm:
        mo = str('')
        ex = str('')
        st = str('')
        index = False
        exp = False
        for j in i:
            if index == True and j>='0' and j <='9':
                ex+=j
            else:
                index=False    
            if j!='，' and j !='。' and j!='*' and j !='計' and j != '元' and (j<'0' or j > '9') and j!='及':
                st+=j
            elif j=='，':
                if st in dicts and ex != '':
                    dicts[st] += int(ex)
                elif st in dicts and ex=='':
                    dicts[st]+=1
                elif ex != '':
                    dicts[st] = int(ex)
                else:
                    dicts[st] = 1
                ex=str('')
                st=str('')
            elif j <='9' and j >= '0' and exp == True:
                mo+=j
            if j=='。':
                money.append(mo)
            if j =='*':
                index = True
            if j=='計':
                exp = True
    for i in range(len(spaces)):
        if spaces[i] in city1:
            city1[spaces[i]] += int(money[i])
        else:
            city1[spaces[i]] = int(money[i])
    return dicts
def ton200w(year,month):
    selectlink=[]
    if int(month)<=9:
        month='0'+str(month)
    else:
        month=str(month)
    for s in link_list:
        if year+month in s:
            selectlink.append(s)
    url='https://www.etax.nat.gov.tw/'+selectlink[0]
    html = requests.get(url).content.decode('utf-8')
    sp = BeautifulSoup(html,'html.parser')
    table = sp.find('table',{'id':'fbonly_200'})
    rows  = table.find_all('td',{'headers':'tranItem2'})
    space = table.find_all('td',{'headers':'companyAddress2'})
    items=[]
    spaces = []
    money=[]
    for r in rows:
        items.append(r.text)
    for s in space:
        s = str(s)
        spaces.append(str(s[30:33]))
    itm=[]
    for i in range(0,len(items)):
        items[i]=items[i].replace('、','，')
        items[i]=items[i].replace('和','，')
        items[i]=items[i].replace('及','，')
    for i in items:
        itm.extend(i.split('及'))
    dicts={}
    for i in itm:
        mo = str('')
        ex = str('')
        st = str('')
        exp = False
        index = False
        for j in i:
            if index == True and j>='0' and j <='9':
                ex+=j
            else:
                index=False    
            if j!='，' and j !='。' and j!='*' and j !='計' and j != '元' and (j<'0' or j > '9') and j!='及':
                st+=j
            elif j=='，':
                if st in dicts and ex != '':
                    dicts[st] += int(ex)
                elif st in dicts and ex=='':
                    dicts[st]+=1
                elif ex != '':
                    dicts[st] = int(ex)
                else:
                    dicts[st] = 1
                ex=str('')
                st=str('')
            elif j <='9' and j >= '0' and exp == True:
                mo+=j
            if j=='。':
                money.append(mo)
            if j =='*':
                index = True
            if j=='計':
                exp = True
    for i in range(len(spaces)):
        if spaces[i] in city2:
            city2[spaces[i]] += int(money[i])
        else:
            city2[spaces[i]] = int(money[i])
    return dicts

window = Tk()
window.geometry('200x200') 
def box():
    top = Toplevel(window)
    top.geometry('750x250')
    start = Label(top , text = "Choose start year and month")
    start.pack()

    combo1_y = ttk.Combobox(top , values = ['102','103','104','105','106','107','108','109'])
    combo1_y.pack()
    combo1_y.current(0)

    combo1_m = ttk.Combobox(top , values = ['1','2','3','4','5','6','7','8','9','10','11','12'])
    combo1_m.pack()
    combo1_m.current(0)

    end = Label(top , text = "Choose end year and month")
    end.pack()
    combo2_y = ttk.Combobox(top , values = ['102','103','104','105','106','107','108','109'])
    combo2_y.pack()
    combo2_y.current(0)

    combo2_m = ttk.Combobox(top , values = ['1','2','3','4','5','6','7','8','9','10','11','12'])
    combo2_m.pack()
    combo2_m.current(0)
    
    numb = Label(top, text = "invoicenumber")
    numb.pack()
    
    combo3_entry = ttk.Entry(top,width = 20)
    combo3_entry.pack()
    def start_btn():
        nowstart()
        year = str(combo1_y.get())
        month = int(combo1_m.get())
        
        if month%2==0:
            month-=1

        prize = select(year,month)
        invoicenumber = combo3_entry.get()
        
        normalprize=[]
        normalprize.append(int(prize[0]))
        normalprize.append(int(prize[1]))
        prize[2]=int(prize[2].replace(" ",""))
        normalprize.append(int(prize[2]/100000000%100000000))
        normalprize.append(int(prize[2]/10000000000000000))
        normalprize.append(int(prize[2]%100000000))
        print(normalprize)
        addsixprize=[]
        for p in prize[3].split("、"):
            addsixprize.append(int(p))
        print(addsixprize)
        getmoney=compare(invoicenumber,normalprize,addsixprize)
        if getmoney==0:
            print("沒中獎")
        else:
            print("恭喜中獎，中獎金額: ",getmoney)
        stastic1000w={}
        stastic200w={}
        item1={}
        item2={}
        stastic1000w=ton1000w(str(year),str(month))
        stastic200w=ton200w(str(year),str(month))
        item1 = stastic1000w
        item2 = stastic200w
        stastic200w=list(set(stastic200w))
        stastic1000w=list(set(stastic1000w))
        votes=[len(stastic1000w), len(stastic200w)]
        winmoney=['1000w', '200w']
        x=np.arange(len(winmoney))
        a=[]
        item1num=[]
        for i in item1.keys():
            a.append(i)
            item1num.append(item1[i])
        item1x = np.arange(len(a))
        b=[]
        item2num=[]
        for i in item2.keys():
            b.append(i)
            item2num.append(item2[i])
        item2x = np.arange(len(b))
        c=[]
        citymoney1=[]
        for i in city1.keys():
            c.append(i)
            citymoney1.append(city1[i])
        city1x = np.arange(len(c))
        d=[]
        citymoney2=[]
        for i in city2.keys():
            d.append(i)
            citymoney2.append(city2[i])
        city2x = np.arange(len(d))
        plt.rcParams['font.sans-serif']=['Microsoft YaHei','SimHei']
        fig, axes = plt.subplots(3,2)
        fig.delaxes(axes[2][1])
        fig.set_size_inches(7.5,9)
        axes[0][0].bar(x , votes,tick_label=winmoney)
        axes[0][0].set_title('invoice winmoney')
        axes[0][0].set_xlabel('the ammount of win money')
        axes[0][0].set_ylabel('variety of things')
        axes[0][1].bar(item1x, item1num, color = 'green',tick_label = a)
        for tick in axes[0][1].get_xticklabels():
            tick.set_rotation(45)
        axes[0][1].set_title('amount of items (1000w)')
        axes[0][1].set_xlabel('name')
        axes[0][1].set_ylabel('quantity')
        axes[1][0].bar(item2x, item2num, color = 'green',tick_label = b)
        axes[1][0].set_title('amount of items (200w)')
        axes[1][0].set_xlabel('name')
        axes[1][0].set_ylabel('quantity')
        for tick in axes[1][0].get_xticklabels():
            tick.set_rotation(45)
        axes[1][1].bar(city1x, citymoney1, color = 'grey', tick_label = c)
        axes[1][1].set_title('Consumption in various cities')
        axes[1][1].set_xlabel('city')
        axes[1][1].set_ylabel('consumption')
        axes[2][0].bar(city2x,citymoney2, color='grey',tick_label = d)
        axes[2][0].set_title('Consumption in various cities')
        axes[2][0].set_xlabel('city')
        axes[2][0].set_ylabel('consumption')
        for tick in axes[1][1].get_xticklabels():
            tick.set_rotation(45)
        for tick in axes[2][0].get_xticklabels():
            tick.set_rotation(45)
        print("圖表請看上圖")
        print("中一千萬的人買了"+str(len(stastic1000w))+"種東西")
        print("中二百萬的人買了"+str(len(stastic200w))+"種東西")
        print("中一千萬的交易項目及次數:")
        print(item1)
        print("中二百萬的交易項目及次數:")
        print(item2)
        print("中一千萬的各城市消費:")
        print(city1)
        print("中二百萬的各城市消費:")
        print(city2)
        fig.tight_layout()
        plt.show()
        
    buttonS = Button(top , text = "Start",command = start_btn)
    buttonS.pack()
    def exit_btn():
        top.destroy()
        top.update()

    buttonQ = Button(top , text = "Quit",command=exit_btn)
    buttonQ.pack()   

menu = Menu(window)

menu.add_command(label = "Analyze", command = box)
menu.add_command(label = "Exit", command = window.quit)

window.config(menu = menu)
window.mainloop()