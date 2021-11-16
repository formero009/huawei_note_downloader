#coding=utf8

import requests,json,html
from lxml import etree

list_url = "https://cloud.huawei.com/notepad/simplenote/query"
content_url = "https://cloud.huawei.com/notepad/note/query"
payload = json.dumps({
  "traceId": "123"
})
header= {
  'Cookie': 'cplang=en-us; HW_refts_hicloudportal_2_cloud_huawei_com=1637036129154; HW_id_hicloudportal_2_cloud_huawei_com=3f08455fcf764926b7bcc3ce94c3b099; HW_idts_hicloudportal_2_cloud_huawei_com=1637036129155; HuaweiID_CAS_ISCASLOGIN=true; CASLOGINSITE=1; LOGINACCSITE=1; HW_idn_hicloudportal_2_cloud_huawei_com=73cb901d36a64cccbf2a213d971cc6c5; HW_viewts_hicloudportal_2_cloud_huawei_com=1637043298958; siteID=1; JSESSIONID=EEF071275EC5E33DA20BA3DD5C3EA8896F6CF737F1C28C9D; loginID=EEF071275EC5E33DA20BA3DD5C3EA8896F6CF737F1C28C9D; token=467eb61ef76e5c93302b68ea0f228dc913e30225297315da; needActive=10; userId=350086000007208204; functionSupport=1_1; isLogin=1; loginSecLevel=2; webOfficeEditToken=3500860000072082041637043300603; CSRFToken=592f1fb42d7d73ed5ae712547950d1c83334a1ad1bda4b9b; HW_idvc_hicloudportal_2_cloud_huawei_com=2',
  'Content-Type': 'application/json'
}

#解析所有note目录json数据
def getAllNote():
    response = requests.request("POST", list_url, headers=header, data=payload)
    result = json.loads(response.text)
    result_json = result.get('rspInfo').get('noteList')
    return result_json


if __name__ == '__main__':
    dataFile = "C:\\Users\\Forme\\Desktop\\dataFile.txt"
    f = open(dataFile,"w+",encoding="utf8")
    result_json = getAllNote()
    for j in result_json:
        # print(json.loads(json.dumps(j.get('data'))))
        f.writelines('标题: \n')
        f.writelines(json.loads(j.get('data')).get('title')+'\n内容:\n')
        guid = json.loads(j.get('data')).get('guid')
        print(guid)
        ##  request content
        contentPayload = json.dumps({
            "ctagNoteInfo": "123",
            "ctagNoteTag": "123",
            "guid": guid,
            "traceId": "123"
        })
        
        contentRes = requests.request("POST", content_url, headers=header, data=contentPayload)
        # print(contentRes.text[0:100])
        contentData = json.loads(contentRes.text)
        t = contentData.get('rspInfo').get('data')
        content_string = json.loads(t).get('content').get('html_content')
        
        #
        imgList = json.loads(t).get('fileList')
        if imgList != None and len(imgList) > 0:
            imgpos = 0
            while content_string.find('图片')!=-1:
                content_string.replace('图片',imgList[imgpos].get('name'),1)
                imgpos+=1
                
        t = html.unescape(content_string)
        html1=etree.HTML(t)
        result = html1.xpath('string(.)')
        # result=etree.tostring(html1,encoding='utf-8')
        # result = result.decode('utf-8')
        # content_string = content_string.replace('<note><element type="Text">','')
        # content_string = content_string.replace('</element></note>','')
        # content_string = content_string.replace('<hw_font size ="1.0">','')
        # content_string = content_string.replace('</hw_font>','')
        # content_string = content_string.replace('<br>','')
        f.writelines(result + '\n\n\n')
    f.close()