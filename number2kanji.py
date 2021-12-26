import json

def lambda_handler(event, context):
    # TODO implement
    #key1取得と桁分け前準備
    target_num=event['key1']
    #数字か確認
    if not target_num.isdigit():
        raise Exception("Parameter error. 'key1' is not a correct input")
    num_list=get_split2character(target_num)
    get_split_keta=get_split2keta(num_list)
    #漢字変換
    if int(target_num)==0:
        return {
            'statusCode': 200,
            'body': json.dumps('零', ensure_ascii=False)
        }
    number2kanji=large_keta(get_split_keta)
    print(number2kanji)
    return {
        'statusCode': 200,
        'body': json.dumps(number2kanji, ensure_ascii=False)
    }
    #raise Exception("Parameter error. 'key1' is not a correct input")
        
def convert_character(target_character):#入力はスプリット後の数字文字.
    convert_num=int(target_character)
    suji   = ["","壱","弐","参","四","五","六","七","八","九"]
    return suji[convert_num]
    
def get_split2character(target_num):
    split_num=list(target_num)
    return split_num
    
def get_split2keta(num_list):
    #桁数確認
    num_length=len(num_list)
    if num_length>16:
        raise Exception("Parameter error. 'key1' is too long")
    reverse_num=num_list[::-1]
    n=0
    s=0
    inv_split_num=[]
    for i in reverse_num:
        inv_split_num.append(reverse_num[n:n+4:1])
        n += 4
        s += 1
        if n >= num_length:
            break
    split_len=len(inv_split_num)
    ketadevided_num=[]
    #returnable_num.append(inv_split_num[0][::-1])
    #print(returnable_num)
    for i in range(split_len):
        ketadevided_num.append(inv_split_num[i][::-1])
        #returnable_num[i]=inv_split_num[i][::-1]
        #print(returnable_num[i])
        #桁の小さいものが先頭になって返る
        #1234567890->[[7,8,9,0],[3,4,5,6],[1,2]]
    ketadevided_num=ketadevided_num[::-1]
    #1234567890->[[1,2],[3,4,5,6],[7,8,9,0]]
    return ketadevided_num

def keta2kanji(target_numbers):
    target_strings=[]
    target_length=len(target_numbers)
    target_numbers=target_numbers[::-1]
    #keta = ('千', '百', '拾', '')
    keta=('', '拾', '百', '千')
    for i in range(target_length):
        target_strings.append(convert_character(target_numbers[i]))
        #print(target_strings[i])
        if not target_strings[i]=='':
            target_strings[i]=target_strings[i]+keta[i]
    target_strings=target_strings[::-1]
    #print(target_strings)
    returnable_value=''.join(target_strings)
    #print(returnable_value)
    #[7,8,9,0]->'七千八百九拾',[1,2]->'壱拾弐'
    return returnable_value
    
def large_keta(target_numbers):
    target_ketanum=len(target_numbers)
    target_strings=[]
    large_keta=('兆', '億', '万', '')
    for i in range(target_ketanum):
        target_strings.append(keta2kanji(target_numbers[i]))
        if target_ketanum-i==4:
            target_strings[i]=target_strings[i]+large_keta[0]
        elif target_ketanum-i==3:
            target_strings[i]=target_strings[i]+large_keta[1]
        elif target_ketanum-i==2:
            target_strings[i]=target_strings[i]+large_keta[2]
    target_strings=''.join(target_strings)
    #print(target_strings)
    #[[1,2],[3,4,5,6],[7,8,9,0]]->'壱拾弐億参千四百五拾六万七千八百九拾'
    return target_strings
"""
このプログラムはaws lambdaで使用することを想定しています.
環境:aws api gateway+aws lambda
参考:
https://qiita.com/minsu/items/c9e983f109b1cf5a516e
https://tech-cci.io/archives/1399
https://init0.hatenablog.com/entry/2016/11/28/012325
エンドポイント:
https://gxxw3d3tn0.execute-api.ap-northeast-1.amazonaws.com/v1/number2kanji/number?key1=1
key1を任意の数字に変えると動作.
"""