import smtplib
import unicodedata
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import requests,csv


from argparse import ArgumentParser
import matplotlib.font_manager as fm
from matplotlib.ft2font import FT2Font
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = ['Arial Unicode MS']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
#
sns.set_style('whitegrid', {'font.sans-serif': ['Arial Unicode MS', 'Arial']})

# data_temp = {"沪深300":{"nei":510300,"wai":10038}}

with open("2121.csv", "r",encoding="utf-8") as file:
    file_data = file.readlines()
data_temp = {}
for solo in file_data:
    temp_list = solo.split(",")
    data_temp[temp_list[2]] = {"nei": temp_list[3], "wai": temp_list[4],"name":temp_list[1]}

def dataWash(d_test):
    temp_list = []
    data_list = {}

    def getDataList(key, data):
        if isinstance(data, dict):
            for index, value in data.items():
                getDataList(str(key) + '_' + str(index), value)
        else:
            data_list[key] = data

    for solo in d_test:
        data_list = {}
        for index, value in solo.items():
            getDataList(index, value)
        temp_list.append(data_list)
    return temp_list

def getLatest(token):
    url = "https://www.lixinger.com/api/analyt/stock-collection/price-metrics/indices/latest"

    # payload = "{\"metricNames\":[\"pe_ttm\",\"pb\",\"ps_ttm\",\"dyr\"],\"granularities\":[\"y_10\"],\"metricTypes\":[\"weightedAvg\"]}"
    payload = "{\"metricNames\":[\"pe_ttm\",\"pb\",\"ps_ttm\",\"dyr\"],\"granularities\":[\"y_5\"],\"metricTypes\":[\"weightedAvg\"],\"source\":\"all\",\"category\":\"all\",\"stockFollowedType\":\"all\"}"
    payload = "{\"metricNames\":[\"pe_ttm\",\"pb\",\"ps_ttm\",\"dyr\"],\"granularities\":[\"y_10\"],\"metricTypes\":[\"weightedAvg\"],\"source\":\"all\",\"category\":\"all\",\"stockFollowedType\":\"all\"}"
    headers = {
        'Connection': "keep-alive",
        'Accept': "application/json, text/plain, */*",
        'Origin': "https://www.lixinger.com",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        'Content-Type': "application/json;charset=UTF-8",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Referer': "https://www.lixinger.com/analytics/indice/dashboard/value/list?source=all&category=all&metric-type=weightedAvg&granularity=y_5&sort-name=pe_ttm.latestVal&sort-order=asc",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cookie': "jwt="+token,
        'Cache-Control': "no-cache",
        'Postman-Token': "123c2494-4b40-45df-af0d-2d0f2ffcc9d4,76155ecb-77e7-41ef-9646-75b05846d7ac",
        'Host': "www.lixinger.com",
        'Content-Length': "158",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    return False

def print_glyphs(path):
    """
    Print the all glyphs in the given font file to stdout.

    Parameters
    ----------
    path : str or None
        The path to the font file.  If None, use Matplotlib's default font.
    """
    if path is None:
        path = fm.findfont(fm.FontProperties())  # The default font.

    font = FT2Font(path)

    charmap = font.get_charmap()
    max_indices_len = len(str(max(charmap.values())))

    print("The font face contains the following glyphs:")
    for char_code, glyph_index in charmap.items():
        char = chr(char_code)
        name = unicodedata.name(
            char,
            f"{char_code:#x} ({font.get_glyph_name(glyph_index)})")
        print(f"{glyph_index:>{max_indices_len}} {char} {name}")

def getPoint(element):
    return element["sort"]


def draw_font_table(path, data=None):
    """
    Draw a font table of the first 255 chars of the given font.

    Parameters
    ----------
    path : str or None
        The path to the font file.  If None, use Matplotlib's default font.
    """
    if path is None:
        path = fm.findfont(fm.FontProperties())  # The default font.

    font = FT2Font(path)
    # A charmap is a mapping of "character codes" (in the sense of a character
    # encoding, e.g. latin-1) to glyph indices (i.e. the internal storage table
    # of the font face).
    # In FreeType>=2.1, a Unicode charmap (i.e. mapping Unicode codepoints)
    # is selected by default.  Moreover, recent versions of FreeType will
    # automatically synthesize such a charmap if the font does not include one
    # (this behavior depends on the font format; for example it is present
    # since FreeType 2.0 for Type 1 fonts but only since FreeType 2.8 for
    # TrueType (actually, SFNT) fonts).
    # The code below (specifically, the ``chr(char_code)`` call) assumes that
    # we have indeed selected a Unicode charmap.
    codes = font.get_charmap().items()




    i = 0
    c_list = {"name": data[0]["date"].split("T")[0],
              # "stockCode":"指数代码",
              "wai": "场外代码",
              # "index":"index",
              "nei":"场内代码",
              "pe_ttm_y_10_weightedAvg_latestVal": "PE",
              "pe_ttm_y_10_weightedAvg_latestValPos": "PE百分位",
              # "pe_ttm_y_10_weightedAvg_minVal": "PE区间下限",
              # "pe_ttm_y_10_weightedAvg_maxVal": "PE区间上限",
              # "pe_ttm_y_10_weightedAvg_riskVal": "PE危险点",
              # "pe_ttm_y_10_weightedAvg_chanceVal": "PE机会点",

              "pb_y_10_weightedAvg_latestVal": "PB",
              "pb_y_10_weightedAvg_latestValPos": "PB百分位",

              # "ps_ttm_y_10_weightedAvg_latestVal": "PS",
              # "ps_ttm_y_10_weightedAvg_latestValPos": "PS百分位",

              "dyr_weightedAvg": "股息率",

              }
    for check_num in range(1,4):

        main_index=1
        fig, ax = plt.subplots(figsize=(10, 5))  # 大小
        if data:
            labelc = list(c_list.values())
            labelw = []
            chars = []
            cellColours = []
            for solo in data: #排序

                val = solo["pe_ttm_y_10_weightedAvg_latestVal"]
                good = solo["pe_ttm_y_10_weightedAvg_chanceVal"]
                bad = solo["pe_ttm_y_10_weightedAvg_riskVal"]

                value_list = [solo["pe_ttm_y_10_weightedAvg_latestVal"],
                              solo["pe_ttm_y_10_weightedAvg_chanceVal"],
                              solo["pe_ttm_y_10_weightedAvg_riskVal"],
                              solo["pb_y_10_weightedAvg_latestVal"],
                              solo["pb_y_10_weightedAvg_chanceVal"],
                              solo["pb_y_10_weightedAvg_riskVal"],
                              solo["ps_ttm_y_10_weightedAvg_latestVal"],
                              solo["ps_ttm_y_10_weightedAvg_chanceVal"],
                              solo["ps_ttm_y_10_weightedAvg_riskVal"],
                              ]
                result = {"good":0,"bad":0,"other":0}
                for index in range(0, len(value_list), 3):
                    if value_list[index] < value_list[index + 1]:
                        result["good"] += 1
                    elif value_list[index + 1] < value_list[index] < value_list[index + 2]:
                        result["other"] += 1
                    else:
                        result["bad"] += 1
                if result["good"] >= check_num:
                    solo["sort"] = 0
                else:
                    if result["other"] > result["bad"]:
                        solo["sort"] = 1
                    else:
                        solo["sort"] = 2

                if val > bad:
                    solo["sort"] = 2

            data.sort(key=getPoint)
            for solo_data in data:
                if solo_data["stockCode"] not in data_temp.keys():
                    continue
                print(solo_data["stockCode"])
                solo_data["index"] = main_index
                main_index+=1

                solo_data["wai"] = data_temp[solo_data["stockCode"]]["wai"]
                solo_data["nei"] = data_temp[solo_data["stockCode"]]["nei"]
                temp = []
                color = []
                width = []
                for key in c_list:
                    if key in solo_data.keys():
                        if "Pos" in key or "dyr_weightedAvg"==key:
                            temp.append('%.2f%%'%(solo_data[key]*100))
                        elif key == "pe_ttm_y_10_weightedAvg_latestVal":
                            temp.append('%.2f'%solo_data[key])
                        elif key == "pb_y_10_weightedAvg_latestVal":
                            temp.append('%.2f' % solo_data[key])
                        else:
                            temp.append(solo_data[key])
                    else:
                        temp.append("")
                    if solo_data["sort"]==0:
                        color.append('green')
                    elif solo_data["sort"]==1:
                        color.append("yellow")
                    else:
                        color.append("red")
                    width.append(2)
                chars.append(temp)
                cellColours.append(color)
                # labelw.append(0.2)

        ax.set_axis_off()

        table = ax.table(
            cellText=chars,
            # rowLabels=labelr,
            colLabels=labelc,
            # cellColours=[[".95" for c in range(16)] for r in range(16)],
            cellColours=cellColours,
            # colWidths=labelw,
            cellLoc='center',
            edges="BRTL",  # 边框 BRTL
            loc='upper left',
        )
        table.auto_set_font_size(False)
        table.set_fontsize(2)

        # table.scale(2, 2)
        for key, cell in table.get_celld().items():
            row, col = key
            if row > -1 and col > -1:  # 塞数据
                cell.set_text_props(fontproperties=fm.FontProperties(fname=path))

        fig.tight_layout()
        plt.savefig(str(check_num)+".png")
        plt.close()
    ff = open(str(check_num)+"d.csv", "w", encoding='utf-8-sig')
    writer = csv.writer(ff)
    writer.writerows(chars)
    ff.close()
    # plt.show()

def sendQQEmail(emailAddrs: list):
    #========= 改成能用的邮箱 这个邮箱不能发=====
    passwd = 'xxx'
    msg_from = 'liufeng778@163.com'
    # ====================================
    imageFile = '1.png'
    imageApart = MIMEImage(open(imageFile, 'rb').read(), imageFile.split('.')[-1])
    imageApart.add_header('Content-Disposition', 'attachment', filename=imageFile)
    imageFile = '2.png'
    imageApart1 = MIMEImage(open(imageFile, 'rb').read(), imageFile.split('.')[-1])
    imageApart1.add_header('Content-Disposition', 'attachment', filename=imageFile)
    imageFile = '3.png'
    imageApart2 = MIMEImage(open(imageFile, 'rb').read(), imageFile.split('.')[-1])

    imageApart2.add_header('Content-Disposition', 'attachment', filename=imageFile)
    imageFile = '3d.csv'
    imageApart3 = MIMEImage(open(imageFile, 'rb').read(), imageFile.split('.')[-1])
    imageApart3.add_header('Content-Disposition', 'attachment', filename=imageFile)
    msg = MIMEMultipart()
    msg.attach(imageApart)
    msg.attach(imageApart1)
    msg.attach(imageApart2)
    msg.attach(imageApart3)
    msg['Subject'] = 'auto msg'
    try:
        s = smtplib.SMTP_SSL("smtp.163.com", 465)
        s.login(msg_from, passwd)
        for msg_to in emailAddrs:
            s.sendmail(msg_from, msg_to, msg.as_string())
            print("done "+msg_to)
    except s.SMTPException as e:
        print(e)
    finally:
        s.quit()

if __name__ == "__main__":
    token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1ZGVmNDgwMjU5NzRkNTU5MDMwMGI3YTQiLCJpYXQiOjE1NzU5NjMxNTMsImV4cCI6MTU3NzE3Mjc1M30.ZgZ_gpRiTfsSyQfoNbe-z_Ced1De3wmtlOmkbdV5BKk"
    data = getLatest(token)
    if data:
        data = dataWash(data)
        parser = ArgumentParser(description="中文")
        parser.add_argument("path", nargs="?", help="Path 中文to the font file.")
        parser.add_argument("--print-all", action="store_true",
                            help="Additionally, print all chars to stdout.")
        args = parser.parse_args()
        if args.print_all:
            print_glyphs(args.path)
        draw_font_table(args.path, data=data)
        print("send")
        sendQQEmail(['34862933@qq.com', '89285897@qq.com'])
    else:
        print("error")







