import json
import urllib
import io
import os
import random
import time
import csv
import oauth2


def search(args = None):

	if(args == None):
		args = sys.argv[1:]

	query = args
	access_token = "__________"

	url = "___________".format(access_token, query)
	print(url)

	r = urllib2.urlopen(url)
	resultJSON = r.readline().decode('utf-8')
	result = json.loads(resultJSON)

	result['data'] = [ item for item in result['data']
                   if query.lower() in item['name'].lower() 

        while(search_type != -1)
        for i in range (len(search_type))
          url = website+"/graphql/query/?query_hash=298b92c8d7cad703f7565aa892ede943&variables=%7B%22tag_name%22%3A%22"+q+"%22%2C%22first%22%3A6%2C%22after%22%3A%22"+hashn+"%22%7D"
            print (url1)
           temp_dict = {}  

          continue
            first_string = search_type[i]['node']['edge_media_to_caption']['edges'][0]['node']['text']
            shortcode = search_type[i]['node']['shortcode']
            url2 = website+"/p/"+shortcode+"/?__a=1"
            getnt = s.get(url2, verify=False)
            getnt = json.loads(getnt.text)
            username = getnt['imageql']['shortcode_media']['owner']['username']
            ptext = getnt['shortcode_media']['tag']['tag_text']
            ptime = getnt['imageql']['shortcode_media']['taken_at_timestamp']
            ptime = time.strftime('%Y-%m-%d',time.localtime(ptime))
            print (username)
            print (ptime)
            print (first_string)
            data = [username,ptime,re.sub(r'\s+',' ', d)]
            result.writerow(data)
    
        try:
             if len(search_type[i]['node']['edge_media_to_caption']['edges']) == 0:
        except:
              error_message = open("bug.txt","w")
              error_message.writelines(html.text)
              error_message.close()
              print ("ERROR")
        return result

if __name__ == '__main__':

	args = sys.argv[1:]

	search(args[0])


        print(urllib.parse.quote(search))
          url1 = website+"/explore/tags/"+q+"/?__a=1"
          csvfile = codecs.open("./Save/"+str(search)+".csv", 'wb',encoding='gb18030')
          submit = "./Save/"+str(search)+".json"
          result = [] 

          tag_owner = csv.writer(csvfile)
          data = ['poster','data_time','tag_text']
          tag_owner.writerow(data)

    
        data = [username,ptime,nd]
        temp_dict['author'] = username  
        temp_dict['date'] = ptime  
        temp_dict['comment'] = nd 
        result.append(temp_dict) 
        writer.writerow(data)
    
        f.writelines('tag_owner'+username+'\n'+'time'+ptime+'\n'+'content'+ptext+'\n')
        b = ans['data']['hashtag']["edge_hashtag_to_media"]
        hnp = b['page_info']['has_next_page']
        hashn = b['page_info']['end_cursor'] 
        print (hnp,hashn,pgn,len(edges))
      

