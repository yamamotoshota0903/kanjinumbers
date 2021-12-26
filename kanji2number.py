import json
suji   = ["","壱","弐","参","四","五","六","七","八","九"]
num_table = dict(zip(suji,(n for n in range(10))))
tais1 = '千百十'
tais1_table=dict(zip(tais1, (10**(3-n) for n in range(3))))
tais2 = '兆億万'
tais2_table=dict(zip(tais2, (10000**(3-n)for n in range(3))))

def lambda_handler(event, context):
    # TODO implement
    #漢数字か確認
    if not (event['key1'].isnumeric() and event['key1'].isalpha()):
        raise Exception("Parameter error. 'key1' is not a correct input")
    #萬を万に変換
    event['key1']=event['key1'].replace('萬', '万')
    #兆億万の回数
    if (event['key1'].count('兆')>1 or event['key1'].count('億')>1 or event['key1'].count('万')>1):
        raise Exception("Parameter error. 'key1' is not a correct keta")
    #0の処理
    if event['key1']=='零':
        return {
            'statusCode': 200,
            'body': json.dumps(0)
        }
    ans_num=kanji2num_main(event['key1'])
    return {
        'statusCode': 200,
        'body': json.dumps(ans_num)
    }

def kan2num(text):
    text=text.replace('一', '壱').replace('二', '弐').replace('三', '参')
    try:
        ans_num=num_table[text]
    except:
        raise Exception("Parameter error. 'key1' is bad order")
    #'壱'->1
    return ans_num
    
def split_small_keta(text):
    #十->拾
    text=text.replace('十', '拾')
    #千百拾の回数チェック
    if (text.count('千')>1 or text.count('百')>1 or text.count('拾')>1):
        raise Exception("Parameter error. 'key1' has many small keta")
    #ans_numに追加していく
    ans_num=0
    #千を壱千に変換する
    if (text.find('千')==0):
        text=text.replace('千', '壱千')
    #千でわける
    splitted_text=text.split('千')
    if (len(splitted_text)>1 or (not text.find('千')==-1)):
        ans_num=kan2num(splitted_text[0])*1000
    #以下百の処理
    if (splitted_text[-1].find('百')==0):
        splitted_text[-1]=splitted_text[-1].replace('百', '壱百')
    #print(splitted_text)
    splitted_text=splitted_text[-1].split('百')
    if (len(splitted_text)>1 or (not text.find('百')==-1)):
        ans_num+=kan2num(splitted_text[0])*100
    #以下拾の処理
    if (splitted_text[-1].find('拾')==0):
        splitted_text[-1]=splitted_text[-1].replace('拾', '壱拾')
    splitted_text=splitted_text[-1].split('拾')
    if (len(splitted_text)>1 or (not text.find('拾')==-1)):
        ans_num+=kan2num(splitted_text[0])*10
        #print(splitted_text)
    ans_num+=kan2num(splitted_text[-1])
    #print(ans_num)
    return ans_num

def kanji2num_main(text):
    #変換のメインになる関数(0以外全部ここでやる)
    #ans_numに加算していく
    ans_num=0
    extracted_text=[]
    #兆
    splitted_text=text.split('兆')
    if (len(splitted_text)>1 or (not text.find('兆')==-1)):
        extracted_text.append(splitted_text[0])
        ans_num+=int(split_small_keta(splitted_text[0]))*10**12
        #兆の桁変換:壱兆->10**12
    #億
    splitted_text=splitted_text[-1].split('億')
    if (len(splitted_text)>1 or (not text.find('億')==-1)):
        extracted_text.append(str(split_small_keta(splitted_text[0])))
        #print('億なう')
        print(splitted_text)
        ans_num+=split_small_keta(splitted_text[0])*10**8
    #万
    splitted_text=splitted_text[-1].split('万')
    if (len(splitted_text)>1 or (not text.find('万')==-1)):
        extracted_text.append(str(split_small_keta(splitted_text[0])))
        #print('万なう')
        ans_num+=split_small_keta(splitted_text[0])*10**4
        ans_num+=split_small_keta(splitted_text[1])
    else:
        print('koko'+splitted_text[0])
        ans_num+=split_small_keta(splitted_text[0])

    return ans_num
"""
endpoint:
https://040qnq4pnc.execute-api.ap-northeast-1.amazonaws.com/v1/kanji2number/kanji?key1=五億七千万
"""