import time
from flask import Flask, json, request, jsonify
from astrapy import DataAPIClient
import uuid
import csv
import io
from flask_cors import CORS
import openai
import requests as re 



# # Configuration for Astra DB
# ENDPOINT = "https://7650461d-f99f-473d-bd18-254b753a4f45-westus3.apps.astra.datastax.com"
TOKEN = "AstraCS:ZhfFhNUAeqZxFEmJeSSudxYg:ff1b988a241645646f73645da5f27c916f2b97846026e2bdcf87d12bfb984f90"
openai.api_key = "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"



cities={
    "leeds":"723289d5-9983-4a2f-6538-08dcc857d3e1"
}



def get_events(city):
    
    url = "https://portal.maiden-ai.com/api/v1/cube/Scouter Galactic Pvt Ltd/night life/scoutermap/Mobile/RequestForJson"

    # Headers including authorization and content type
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJJc3N1ZXIiOiJub0ZldmVyIiwidW5pcXVlX25hbWUiOiI3NDQzN2U1Ny1jOGEwLTQxYTAtYTZmMi1iNjQwYzlhNGIyMzciLCJVc2VySWQiOiI3NDQzN2U1Ny1jOGEwLTQxYTAtYTZmMi1iNjQwYzlhNGIyMzciLCJEZXZpY2VJZCI6IjFCREVEODlCLUI1OTAtNEYwQy1BRTc0LUMyODY0OTRFMDNEOCIsIk9yZ2FuaXphdGlvbklkIjoiMmY4MTE1NzctNTZlYy00YmRmLThlM2MtNjE5MGZkYzYzYmE4IiwiVGltZSI6IjExLzIxLzIwMjQgMDk6MzQ6MDgiLCJuYmYiOjE3MzIxODE2NDgsImV4cCI6MTc2MzcxNzY0OCwiaWF0IjoxNzMyMTgxNjQ4fQ.ycA3jokPX3G46fZk4toGNT5oTfDepv1NLfSNMK1ka3Y'
    }
    jsn={
  "Params1": cities[city.lower()],
  "userId": "b41e0425-47b5-4c06-aba5-d4dc80690174",
  "Params2": "-1",
  "StoredProcedureName": "GetEvents"
}
    res=re.post(url=url,headers=headers,json=jsn).json()
    # print(res)
    return res['data']
    # return jsonify({"message": output_json.split("```")[1].replace("json","")})
    




def get_placers_list(query):
    # Simulate delay
    time.sleep(3)
    
    # Get user input from the JSON request
    user_input = query
    # Messages for OpenAI ChatCompletion
    messages = [
    {
        "role": "system",
        "content": (
            "You are an assistant that generates filter query objects based on user input for a Place database. "
            "The data model includes attributes like PlaceType, CityId, Country, Rating, PriceRange, "
            "CurrentPopularity, Reviews, Gender Preferences, Interest Groups, Neighborhood, and Timezone. "
            "You analyze user input to construct a structured JSON object for filtering."
        )
    },
    {
    "role": "user",
    "content": (
        f"User Input: '{user_input}'\n\n"
        "The data model includes the following attributes and their possible filters:\n\n"
        "1. **PlaceType**: Represents the type of place (e.g., 'Bar', 'Restaurant', 'Seafood market'). Use 'MULTI' as the filter type. Do not make it a list it will be a single list with multiple element seperated bt  ',' \n"
        "2. **CityId**: Represents the city. Use 'EQUALS' as the filter type. Example input: 'cityId: 723289d5-9983-4a2f-6538-08dcc857d3e1'.\n"
        "3. **Country**: Represents the country. Use 'EQUALS' as the filter type.\n"
        "4. **Rating**: Represents the place's rating (1-5). Use 'GREATER' or 'LESSER' as appropriate.\n"
        "5. **PriceRange**:\n"
        "   - '$' = Budget (cheap)\n"
        "   - '$$' = Average\n"
        "   - '$$$' = Expensive\n"
        "   - '$$$$' = VIP (luxury)\n"
        "   Use 'MULTI' as the filter type.\n"
        "6. **CurrentPopularity**:\n"
        "   - 'Packed' = EQUALS 80+\n"
        "   - 'Busy' = GREATER 40 AND LESSER 80 (two filters)\n"
        "   - 'Calm' = GREATER 1 AND LESSER 40 (two filters)\n"
        "   - 'Closed' = EQUALS 0\n"
        "7. **Reviews**: Filter places with specific terms in reviews (e.g., 'fresh seafood', 'great service'). Use 'CONTAINS' as the filter type.\n"
        "8. **Gender Preferences** (e.g., GenderMale, GenderFemale): Filter based on gender percentages. Example input: 'Places with at least 50% male visitors'. Use 'GREATER_THAN'.\n"
        "9. **Interest Groups** (e.g., InterestGay, InterestStraight, InterestBisexual): Filter based on interest group preferences.\n"
        "10. **Neighborhood**: Represents the neighborhood. Use 'EQUALS' as the filter type.\n"
        "11. **Timezone**: Represents the timezone. Use 'EQUALS' as the filter type.\n\n"
        "### City Extraction:\n"
        "Before generating the JSON, extract the city name from the user input and map it to its corresponding city ID using the following dictionary:\n\n"
        "{\n"
        "    'leeds': '723289d5-9983-4a2f-6538-08dcc857d3e1',\n"
        #"    'Los Angeles': '82f34bd9-1290-4abc-9a53-08dcc857d4b2',\n"
        #"    'London': 'b91a6d11-7654-4c8a-a67f-08dcc857d5c3',\n"
        #"    'Tokyo': 'f50e3a77-9983-4f21-b7e8-08dcc857d6d4'\n"
        "}\n\n"
        "If a city name is found in the user input, add the following filter:\n"
        "{\n"
        "    'filterTerm': '<city_id>',\n"
        "    'filterType': 'EQUALS',\n"
        "    'filterBy': 'CityId'\n"
        "}\n\n"
        "### Current Popularity Handling:\n"
        "If 'Busy' or 'Calm' is mentioned in the user input, apply two separate filters:\n"
        "- **Busy (40-80%)**\n"
        "  1. { 'filterTerm': '40', 'filterType': 'GREATER', 'filterBy': 'CurrentPopularity' }\n"
        "  2. { 'filterTerm': '80', 'filterType': 'LESSER', 'filterBy': 'CurrentPopularity' }\n"
        "- **Calm (1-40%)**\n"
        "  1. { 'filterTerm': '1', 'filterType': 'GREATER', 'filterBy': 'CurrentPopularity' }\n"
        "  2. { 'filterTerm': '40', 'filterType': 'LESSER', 'filterBy': 'CurrentPopularity' }\n\n"
        "### Final JSON Output:\n"
        f"Generate the final JSON object for the input '{user_input}' as follows:\n"
        "{\n"
        "    'filterInfo': [\n"
        "        {\n"
        "            'filterTerm': '<filter_value>',\n"
        "            'filterType': '<filter_type>',\n"
        "            'filterBy': '<attribute>'\n"
        "        },\n"
        "        ... additional filters as required\n"
        "    ],\n"
        "    'pageSize': 100000\n"
        "}"
    )
}
    
]


    # Make a request to OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=1000,
            temperature=0.2
        )
        output_json = response['choices'][0]['message']['content'].strip()
        # print(type(output_json))
        # print(output_json)
        
        url = "https://portal.maiden-ai.com/api/v1/cube/Scouter Galactic Pvt Ltd/night life/scoutermap/Place/list"

        # Headers including authorization and content type
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJJc3N1ZXIiOiJub0ZldmVyIiwidW5pcXVlX25hbWUiOiI3NDQzN2U1Ny1jOGEwLTQxYTAtYTZmMi1iNjQwYzlhNGIyMzciLCJVc2VySWQiOiI3NDQzN2U1Ny1jOGEwLTQxYTAtYTZmMi1iNjQwYzlhNGIyMzciLCJEZXZpY2VJZCI6IjFCREVEODlCLUI1OTAtNEYwQy1BRTc0LUMyODY0OTRFMDNEOCIsIk9yZ2FuaXphdGlvbklkIjoiMmY4MTE1NzctNTZlYy00YmRmLThlM2MtNjE5MGZkYzYzYmE4IiwiVGltZSI6IjExLzIxLzIwMjQgMDk6MzQ6MDgiLCJuYmYiOjE3MzIxODE2NDgsImV4cCI6MTc2MzcxNzY0OCwiaWF0IjoxNzMyMTgxNjQ4fQ.ycA3jokPX3G46fZk4toGNT5oTfDepv1NLfSNMK1ka3Y'
        }
        print(type(output_json.split("```")[1].replace("json","")))
        res=re.post(url=url,headers=headers,json=json.loads(output_json.split("```")[1].replace("json",""))).json()
        print(output_json.split("```")[1].replace("json",""))
        # print(res)
        return {"places_data":res["data"],"filter_jsn":json.loads(output_json.split("```")[1].replace("json",""))}
        # return jsonify({"message": output_json.split("```")[1].replace("json","")})
    except openai.error.OpenAIError as e:
        print(e)
        return jsonify({"error": str(e)})
    



def get_place_info(query):
    import json
    import  re
    import urllib.request
    from urllib.parse import quote
    import random
    search_url = "https://list.didsoft.com/get?email=rajeshkumardevapp@gmail.com&pass=zxamw8&pid=http1000&showcountry=no&level=1&country=US"
    search_url2 = "https://list.didsoft.com/get?email=rajeshkumardevapp@gmail.com&pass=zxamw8&pid=http1000&showcountry=no&level=2&country=US"
    search_url3 = "https://list.didsoft.com/get?email=rajeshkumardevapp@gmail.com&pass=zxamw8&pid=http1000&showcountry=no&level=3&country=US"
    urls=[]
     
 
 
    user_agent_list = [
        #Chrome
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            #Firefox
            'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
        ]       
    resp = urllib.request.urlopen(urllib.request.Request(url=search_url, data=None))
    data = resp.read().decode('utf-8').split('/*""*/')[0]
    for i in data.split("\n"):
        urls.append(i)
    resp = urllib.request.urlopen(urllib.request.Request(url=search_url2, data=None))
    data = resp.read().decode('utf-8').split('/*""*/')[0]
    for i in data.split("\n"):
        urls.append(i)
    resp = urllib.request.urlopen(urllib.request.Request(url=search_url3, data=None))
    data = resp.read().decode('utf-8').split('/*""*/')[0]
    for i in data.split("\n"):
        urls.append(i)
    print(len(urls))
    def get_place_info_from_google(placename,city):
            # try:
                address = quote(placename+" "+city).split()
                user_agent = random.choice(user_agent_list)
                headers = {'User-Agent': user_agent}

                
                def index_get(array, *argv):
                    try:
                        for index in argv:
                            array = array[index]
                        return array
                    except (IndexError, TypeError):
                        return None
                
  
                params_url = {
                        "tbm": "map",
                        "tch": 1,
                        "hl": "en",
                        "q":"+".join(address).replace(" ",""),
                        "pb": "!4m12!1m3!1d4005.9771522653964!2d-122.42072974863942!3d37.8077459796541!2m3!1f0!2f0!3f0!3m2!1i1125!2i976"
                            "!4f13.1!7i20!10b1!12m6!2m3!5m1!6e2!20e3!10b1!16b1!19m3!2m2!1i392!2i106!20m61!2m2!1i203!2i100!3m2!2i4!5b1"
                            "!6m6!1m2!1i86!2i86!1m2!1i408!2i200!7m46!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e3!2b0!3e3!"
                            "1m3!1e4!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e3!2b1!3e2!1m3!1e9!2b1!3e2!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e"
                            "10!2b0!3e4!2b1!4b1!9b0!22m6!1sa9fVWea_MsX8adX8j8AE%3A1!2zMWk6Mix0OjExODg3LGU6MSxwOmE5ZlZXZWFfTXNYOGFkWDh"
                            "qOEFFOjE!7e81!12e3!17sa9fVWea_MsX8adX8j8AE%3A564!18e15!24m15!2b1!5m4!2b1!3b1!5b1!6b1!10m1!8e3!17b1!24b1!"
                            "25b1!26b1!30m1!2b1!36b1!26m3!2m2!1i80!2i92!30m28!1m6!1m2!1i0!2i0!2m2!1i458!2i976!1m6!1m2!1i1075!2i0!2m2!"
                            "1i1125!2i976!1m6!1m2!1i0!2i0!2m2!1i1125!2i20!1m6!1m2!1i0!2i956!2m2!1i1125!2i976!37m1!1e81!42b1!47m0!49m1"
                            "!3b1"
                    }

                search_url = "https://www.google.de/search?" + "&".join(k + "=" + str(v) for k, v in params_url.items())
                # search_url="https://www.google.de/search?" + "&"+"tbm"+"="+"map"+"&"+"tch"+"="+"1"+"&"+"hl"+"="+"en"+"&"+"q"+"="+urllib.quote_plus(" ".join(address))+"&"+"pb"+"="+"!4m12!1m3!1d4005.9771522653964!2d-122.42072974863942!3d37.8077459796541!2m3!1f0!2f0!3f0!3m2!1i1125!2i976""!4f13.1!7i20!10b1!12m6!2m3!5m1!6e2!20e3!10b1!16b1!19m3!2m2!1i392!2i106!20m61!2m2!1i203!2i100!3m2!2i4!5b1!6m6!1m2!1i86!2i86!1m2!1i408!2i200!7m46!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e3!2b0!3e3!1m3!1e4!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e3!2b1!3e2!1m3!1e9!2b1!3e2!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e4!2b1!4b1!9b0!22m6!1sa9fVWea_MsX8adX8j8AE%3A1!2zMWk6Mix0OjExODg3LGU6MSxwOmE5ZlZXZWFfTXNYOGFkWDhqOEFFOjE!7e81!12e3!17sa9fVWea_MsX8adX8j8AE%3A564!18e15!24m15!2b1!5m4!2b1!3b1!5b1!6b1!10m1!8e3!17b1!24b1!25b1!26b1!30m1!2b1!36b1!26m3!2m2!1i80!2i92!30m28!1m6!1m2!1i0!2i0!2m2!1i458!2i976!1m6!1m2!1i1075!2i0!2m2!1i1125!2i976!1m6!1m2!1i0!2i0!2m2!1i1125!2i20!1m6!1m2!1i0!2i956!2m2!1i1125!2i976!37m1!1e81!42b1!47m0!49m1!3b1"
                proxy_handler = urllib.request.ProxyHandler({'http': random.choice(urls)})
                req = urllib.request.Request(url=search_url, data=None, headers=headers)
                opener = urllib.request.build_opener(proxy_handler)
                resp = opener.open(req)
                data = resp.read().decode('utf-8').split('/*""*/')[0]
                # f=io.open("data.txt","w",encoding='utf8')  
                # f.write(data)
                jend = data.rfind("}")
                if jend >= 0:
                    data = data[:jend + 1]

                jdata = json.loads(data)["d"]
                jdata = json.loads(jdata[4:])

                info = index_get(jdata, 0, 1, 0, 14)
                rating = index_get(info, 4, 7)
                rating_n = index_get(info, 4, 8)
                popular_times = index_get(info, 84, 0)
                current_popularity = index_get(info, 84, 7, 1)
                current_popularity_status = index_get(info, 84, 6) or ""
                # print(current_popularity_status)
                time_spent = index_get(info, 117, 0)
                if time_spent:

                    nums = [float(f) for f in re.findall(r'\d*\.\d+|\d+', time_spent.replace(",", "."))]
                    contains_min, contains_hour = "min" in time_spent, "hour" in time_spent or "hr" in time_spent

                    time_spent = None

                    if contains_min and contains_hour:
                        time_spent = [nums[0], nums[1] * 60]
                    elif contains_hour:
                        time_spent = [nums[0] * 60, (nums[0] if len(nums) == 1 else nums[1]) * 60]
                    elif contains_min:
                        time_spent = [nums[0], nums[0] if len(nums) == 1 else nums[1]]

                    time_spent = [int(t) for t in time_spent]
                    
                def extract_opening_hours(data):
                    result = {}
                    for entry in data:
                        day = entry[0]
                        time_intervals = entry[-2]  # Directly using time data from entry[-2]

                        if not time_intervals:  # Closed all day
                            result[day] = []
                        else:
                            intervals = []
                            for interval in time_intervals:
                                print(interval)
                                start_time = f"{interval[0]}:{interval[1]}"  # (hour, minute) for start time
                                end_time = f"{interval[2]}:{interval[3]}"  # (hour, minute) for end time
                                intervals.append(start_time)
                                intervals.append(end_time)

                            result[day] = intervals  if intervals!=[] else ["0","0"]
                    result_string = "-".join(
                        ",".join(result[day]) if result[day] else "0,0"
                        for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
                    )
                    return result_string

                rating = json.dumps(rating or None)
                rating_n = json.dumps(rating_n or None)
                current_popularity = json.dumps(current_popularity or 0)
                time_spent  = str(time_spent or []).strip('[]')
                priceRange = len(str(index_get(info, 4, 2) or '$'))
                types = index_get(info, 13, 0) or ''
                address = index_get(info, 18) or ""
                description = index_get(info, 32,1,1) or ""
                print(description)
                
                tel = index_get(info, 3, 0) or index_get(info, 178, 0, 0) or ""
                lat = index_get(info, 9, 2) or 0
                lng = index_get(info, 9, 3) or 0
                img=(index_get(info, 72,0,1,6,0)) 
                googleMapLocation = index_get(info, 42) or ""
                try:
                    googleImages =",".join( [index_get(img_data, 6,0) for img_data in index_get(info, 52,0,0,14) ])
                    print(googleImages)
                except:
                    googleImages=img

                try:
                    print(index_get(info, 34,1))
                    OpeningHour= extract_opening_hours(index_get(info, 34,1)) or ""
                    print(OpeningHour)
                except:
                    OpeningHour=""
                review_text_= [i[1] for i in index_get(info, 31,1) ]
                review_text = ",".join(review_text_)
                print(review_text)
                facebookLink = index_get(info, 7, 0) or ""
                placeName = index_get(info, 11) or ""
            
                if priceRange == 4:
                    priceRange = '$$$$'
                elif priceRange == 3:
                    priceRange = '$$$'
                elif priceRange == 2:
                    priceRange = '$$'
                else:
                    priceRange = '$'

                    
                df={
                "PlaceName": placeName,
                "Address":  address.replace(f"{placeName}, ",''),
                "Latitude": lat,
                "Longitude": lng,
                "PlaceType":types,
                "Reviews":review_text,
                "Description":description,
                "OpeningHours":OpeningHour,
                "PriceRange":priceRange,
                "PhoneNumber": tel,
                "GooglePlaceName": address.replace(f"{placeName},",placeName),
                "GooglePlaceImage":googleImages,
                "Rating": rating,
                "Rating_n": rating_n,
                "CurrentPopularity": current_popularity,
                "GoogleMapLocation":  googleMapLocation.replace("1e1","1d1"),
                "FacebookLink": facebookLink.replace("/url?q=",""),
                }
                
                
                return df
        
   
    return get_place_info_from_google(query["place_name"],query["city"])
    







def get_general_info(query):
    pass
  

  


def get_user_desire(query):
    
    message=message = [
    {
        "role": "system",
        "content": (
            "You are an assistant that extracts location-related details from user queries. "
            "Your task is to identify and extract the 'place name', 'city', and 'address' from the input. "
            "Additionally, classify the intent into one of the following categories: "
            "'ListPlaces' (searching for places), 'PlaceDetails' (inquiring about a specific place), "
            "'EventsList' (looking for events), or 'Other' (unrelated queries)."
        )
    },
    {
        "role": "user",
        "content": (
            f"User Input: '{query}'\n\n"
            "Extract the following details from the user input:\n"
            "- Place Name (if mentioned)\n"
            "- City (if mentioned)\n"
            "- Address (if mentioned)\n\n"
            "Then, classify the intent as follows:\n"
            "- If the user is searching for places, return: ListPlaces\n"
            "- If the user wants details about a place, return: PlaceDetails\n"
            "- If the user is looking for events, return: EventsList\n"
            "- If the query is unrelated, return: Other\n\n"
            "Return the extracted details in this format:\n"
            "{\n"
            "  'place_name': '<Extracted Place Name>',\n"
            "  'city': '<Extracted City>',\n"
            "  'address': '<Extracted Address>',\n"
            "  'intent': '<Determined Intent>'\n"
            "}"
        )
    }
]


    # try:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=message,
        max_tokens=1000,
        temperature=0.2
    )
    output_json = response['choices'][0]['message']['content'].strip()
    # print(type(output_json))
    print(output_json)
    
    try:
        return json.loads(output_json.split("```")[1].replace("json",""))
    except:
        return json.loads(output_json.replace("'",'"'))
        # return jsonify({"message": output_json.split("```")[1].replace("json","")})
    # except openai.error.OpenAIError as e:
    #     print(e)
    #     return jsonify({"error": str(e)})




# Initialize Flask App
app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    
    user_input=request.json.get("message")
    
    user_desire =  get_user_desire(user_input)
    
    if "PlaceDetails" in user_desire["intent"]:
        place=get_place_info(user_desire)
        print(place)
        return jsonify({"type":"info","message":f"{'Here is the place Info :' if place['PlaceName']!="" else f"No place found!\n {user_desire}" }","places":[place]}) 
    elif "ListPlaces" in user_desire["intent"]:
        places=get_placers_list(user_input)
        return jsonify({"type":"place","message":f"{'Here is the list of places' if places['places_data']!=[] else f"No place found!\n {places['filter_jsn']}" }","places":places['places_data']}) 
    elif "EventsList" in user_desire["intent"]:
        events=get_events(user_desire["city"])
        print(type(events))
        return jsonify({"type":"event","message":f"{'Here is the list of Events Tonight!' if events[0]['tonight']!=[] else f"No place found for tonight for the city! Here are some events this week! " }","events": events[0]['tonight'] if events[0]['tonight']!=[] else  events[0]['thisWeek']}) 
        # print("asked for a some Event lists ",user_input,str(user_desire))
    else:
        print("asked for a some other info ",user_input,str(user_desire))
         
    


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=12000)
