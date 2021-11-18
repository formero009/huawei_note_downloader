#coding=utf8

import requests,json,html
from lxml import etree

list_url = "https://cloud.huawei.com/notepad/simplenote/query"
content_url = "https://cloud.huawei.com/notepad/note/query"
payload = json.dumps({
  "traceId": ""
})
header= {
  'Cookie': 'HW_id_hicloudportal_2_cloud_huawei_com=69d0edc067af46ce83c559ed341a178d; HW_idts_hicloudportal_2_cloud_huawei_com=1637224634426; HW_idn_hicloudportal_2_cloud_huawei_com=70a4b4b3a74f4818a170e0f2b274291e; HuaweiID_CAS_ISCASLOGIN=true; CASLOGINSITE=1; LOGINACCSITE=1; siteID=1; loginID=997E2DF1A67E41523F794D6A8F494F6A9265752E5E027AFD; token=d4feed508fafc3439f8c6d5ae0f48b30ca89b278b5b87bd9; cplang=en-us; needActive=10; userId=350086000007208204; functionSupport=1_1; isLogin=1; loginSecLevel=2; webOfficeEditToken=3500860000072082041637224649081; HW_refts_hicloudportal_2_cloud_huawei_com=1637224656338; HW_viewts_hicloudportal_2_cloud_huawei_com=1637224661546; JSESSIONID=9DFD65ED66959E1F9549E43812ED62F1CC8DA8F01C370525; HW_idvc_hicloudportal_2_cloud_huawei_com=3; CSRFToken=1d14334f7a3dc6f0167f75284ee272ef895d3ddfbb38510e',
  'Content-Type': 'application/json'
}

#解析所有note目录json数据
def getAllNote():
    response = requests.request("POST", list_url, headers=header, data=payload)
    result = json.loads(response.text)
    result_json = result.get('rspInfo').get('noteList')
    return result_json


if __name__ == '__main__':
    dataFile = "D:\\dataFile.txt"
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
            "startCursor":"123",
            "traceId": "123"
        })
        
        contentRes = requests.request("POST", content_url, headers=header, data=contentPayload)
        # print(contentRes.text[0:100])
        contentData = json.loads(contentRes.text)
        # print(contentData)
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