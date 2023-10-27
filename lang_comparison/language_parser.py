
from lang_comparison import config
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import urllib
import sqlalchemy
from . import models
import pandas as pd
import re
# from tree_queries.models import TreeNode as tn

#add overarching class like __main__ to run commands for parsing, inserting in db

# find_lang = input('Enter language of choice: ')
class wikipedia_ipa_scrape:
    list_features = {'vowel':['phoneme','vowel_height','vowel_forward','vowel_round','vowel_diacritics','audio_href'],
                            'consonant':['phoneme','consonant_voiced','consonant_manner','consonant_articulation','consonant_diacritics','audio_href']}
    default_rounding = 'unrounded'
    #get_all is to get all phonemes with an audio file or just the ones that match models
    def __init__(self, get_all = True):
        self.get_all = get_all
        self.selenium_driver = self.driver_init()

        self.engine = sqlalchemy.create_engine(config.database_url, echo = False)

        #do I need to encode to find exact matches? I will upload into database, can add 
        #can the vowel and consonant page be matched? if so, will need to get name of phoneme from href
    def driver_init(self):
    # Set up Selenium options
    # executable path being depreciated
        CHROMEDRIVER_PATH = "C:\selenium\chromedriver_win64\chromedriver.exe"
        options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)
        driver.implicitly_wait(10)
        return driver
    

    #CHANGE PARSE CONSONANT
    def parse_consonant_ipa(self, url):
        #just open and load with selenium
        self.selenium_driver.get(url)
        self.selenium_driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        html = self.selenium_driver.page_source
        self.selenium_driver.close()
        #parse with BS, it is faster.

        bs = BeautifulSoup(html).find('tbody')
        #find all vowels with names
        #another site, https://jbdowse.com/ipa/ has other ipa sounds, but I don't like it for some reason.
        features = {}


        for span in bs.findAll('span', {'class': "IPA"}):
            children = span.findChildren("a" , recursive=False)
            if children:
                for child in children:
                    phoneme = child.string
                    #if the browser can't show phoneme correctly, skip it
                    if phoneme.find('\\') != -1:
                        continue
                    segment_name = child.get('href').replace('/wiki/','').lower().replace('sibilant_','sibilant-')
                    seg_list = segment_name.split('_')
                    if not (seg_list[0] == 'voiced' or seg_list[0] == 'voiceless'):
                        seg_list.insert(0,'voiceless')
                    if seg_list[2] == 'lateral':
                        seg_list[1] += '-'+seg_list.pop(2)

                    if len(seg_list) > 4:
                        continue

                    segment_class = 'consonant'
                    # segment_class = seg_list.pop()
                    seg_list.insert(0,phoneme)

                    for n, item in enumerate(seg_list):
                        features.setdefault(segment_name, {})
                        features[segment_name][self.list_features[segment_class][n]] = item                    
                # print([(child.get('href').replace('/wiki/','').split('_'), child.string) for child in children])
            else:
                break
        for span in bs.findAll('span', {'class': "mw-tmh-player audio"}):
            
            children = span.findChildren("a" , recursive=False)
            if children:
                for child in children:  
                    extension = child.get('href')
                    html_audio = urllib.request.urlopen('https://en.wikipedia.org'+extension)
                    file = extension.replace('/wiki/File:','')    
                    #too hardcoded                , hardcoded, replace stop with plosive
                    if file.find('.oga') != -1:
                        continue
                    check_tag = file.replace('.ogg','').replace('PR-','').lower().replace('stop','plosive')
                    print('ct:',check_tag)
                    #doesn't need segment class, does not include 'consonant' in name
                    # check_tag = check_tag[0:check_tag.find(segment_class)+len(segment_class)]
                    # print(file)
                    try:
                        link = BeautifulSoup(html_audio).find('a', string= file)['href']
                        print('checktag:',features[check_tag])
                        features[check_tag]['audio_href'] = 'https:'+link
                    except TypeError as e:
                        pass
                    except KeyError as e:
                        print(e)
                        try:
                            features['voiced_'+check_tag]['audio_href'] = 'https:'+link
                        except:
                            pass
                        
        #post-hoc manipulation into dataframe to insert batchwise into db.
        df = pd.DataFrame(features).transpose()
        df['segment_name'] = df.index
        df['segment_class'] = segment_class
        print(df['segment_name'],df['audio_href'])
        print(df)
        df.to_sql('lang_comparison_ipa_phonemes_audio_href', index = False, con = self.engine, if_exists = 'append', schema = 'public')    #get_all is to get all phonemes with an audio file or just the ones that match models
    
    def parse_vowel_ipa(self, url):
        #just open and load with selenium
        self.selenium_driver.get(url)
        html = self.selenium_driver.page_source
        self.selenium_driver.close()
        #parse with BS, it is faster.

        bs = BeautifulSoup(html).find('tbody')
        #find all vowels with names
        #another site, https://jbdowse.com/ipa/ has other ipa sounds, but I don't like it for some reason.

        features = {}

        for span in bs.findAll('span', {'class': "IPA"}):
            children = span.findChildren("a" , recursive=False)
            if children:
                for child in children:
                    phoneme = child.string
                    segment_name = child.get('href').replace('/wiki/','').lower()
                    #one hardcoded entry to make my life easier
                    if segment_name == 'near-open_central_vowel':
                        segment_name = 'near-open_central_unrounded_vowel'

                    seg_list = segment_name.split('_')
                    segment_class = seg_list.pop()
                    seg_list.insert(0,phoneme)
                    for n, item in enumerate(seg_list):
                        features.setdefault(segment_name, {})
                        features[segment_name][self.list_features[segment_class][n]] = item                    
                # print([(child.get('href').replace('/wiki/','').split('_'), child.string) for child in children])

        for span in bs.findAll('span', {'class': "mw-tmh-player audio"}):
            children = span.findChildren("a" , recursive=False)
            if children:
                for child in children:  
                    extension = child.get('href')
                    html_audio = urllib.request.urlopen('https://en.wikipedia.org'+extension)
                    file = extension.replace('/wiki/File:','')    
                    #too hardcoded                , especially replace('2','')
                    check_tag = file.replace('.ogg','').replace('PR-','').lower()
                    check_tag = check_tag[0:check_tag.find(segment_class)+len(segment_class)]
                    # print(file)
                    try:
                        link = BeautifulSoup(html_audio).find('a', string= file)['href']
                        print(features[check_tag])
                        features[check_tag]['audio_href'] = 'https:'+link
                    except TypeError as e:
                        pass
                    except KeyError as e:
                        features[check_tag.replace('-','_')]['audio_href'] = 'https:'+link
                        
        #post-hoc manipulation into dataframe to insert batchwise into db.
        df = pd.DataFrame(features).transpose()
        df['segment_name'] = df.index
        df['segment_class'] = segment_class
        print(df)
        # df.to_sql('lang_comparison_ipa_phonemes_audio_href', index = False, con = self.engine, if_exists = 'append', schema = 'public')    #get_all is to get all phonemes with an audio file or just the ones that match models
    
class search_and_parse:
    def __init__(self, language, feature_site = 'wals', iso_code = None):
        self.language = language
        self.dic = config.parser_dics[feature_site]
        self.driver = self.driver_init()
        self.iso = iso_code
        self.search_key = self.language

    def driver_init(self):
    # Set up Selenium options
    # executable path being depreciated
        CHROMEDRIVER_PATH = "C:\selenium\chromedriver_win64\chromedriver.exe"
        options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)
        driver.implicitly_wait(10)
        return driver
        # seconds
    #if I was doing this everytime it would be a good time to use celery

    #Wals and phoible should have similar format
    #need to add menu for dialects
    def parse_linguistics_page(self):
        # url = self.dic['url']
        tags = self.dic['tags']
        id = self.dic['id']
        name = self.dic['name']
        self.driver.get(self.url)
        self.driver.maximize_window()

            # hardcoded for specific pages to parse.
        l = self.driver.find_elements("xpath", f'//*[@id="{id}"]/tbody/tr/td')

        data = []
        height=self.driver.execute_script("return document.body.scrollHeight")
        #scroll to get all data
        while True:
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(1)
            for n,item in enumerate(l):
                if item in data:
                    continue
                else:
                    data.append(item)
            lastheight=self.driver.execute_script("return document.body.scrollHeight")
            if height==lastheight:
                break

            height=lastheight
        # print('data: ',data)

        #exclude the empty column that I don't want, could add an excluded column list too
        if name == 'wals':
            for n,i in enumerate(data):
                if n > 0:
                    if n % (len(tags)) == 0:
                        data.remove(i)
        #creates a dictionary with the titles to be put into a pandas dataframe. some trickery on the grammar page, I wanted to parse the percent occurence, which was inside parentheses (n%)
        dic = {title:[] for title in tags}
        dic['language'] = []

        for n in range(len(data)//(len(tags))):
            for m,title in enumerate(tags):
                val = data[m+len(tags)*n].text
                if name == 'phoible':
                    if val == '' or val is None:
                        if title == 'marginal':
                            val = False
                        else:
                            val = ''
                    else:
                        val = re.sub(r'^.*?\(', '' , val.replace('%)',''))
                    
                # elif id == 'Datapoints':
                dic[title].append(val)
            dic['language'].append(self.language)
        # self.driver.close()
        df = pd.DataFrame(dic)
        return df
    #step 1 to find the language in the bar and navigate. need to find better way to locate language, needs to be perfect match or ask for clarification.
    
    # 0. one function for each set, agg and info models.
    # 1. 
    # 2. "lang_geography" for phoible. get "iso_639_3" from lang page.
    #

    def find_language_in_search(self):
        
        self.driver.get(self.dic['url'])
        if self.dic['name'] == 'wals':
            # if self.iso:
            lang_enter = self.driver.find_elements("xpath", '//thead[2]/tr/th/input[@name = "iso_codes"]')
            self.search_key = self.iso
            
                # lang_enter = self.driver.find_elements("xpath", '//thead[2]/tr/th/input[@name = "name"]')
        elif self.dic['name'] == 'phoible':

            # else:
            lang_enter = self.driver.find_elements("xpath", '//thead[2]/tr/th/input[@name = "language"]')
            # lang_enter = self.driver.find_elements("xpath", '//thead[2]/tr/th/input[@name = "iso_codes"]')

            # lang_enter = self.driver.find_elements("xpath", '//thead[2]/tr/th/input[@name = "inventory"]')
        for i in lang_enter:
            try:
                i.send_keys(self.search_key)
                i.submit(Keys.ENTER)
                time.sleep(1)
            except:
                time.sleep(1)
            break
            #applicable to wals, need one more step for phoible
        cols = self.driver.find_elements("xpath", '//thead[1]/tr/th')
        elements = self.driver.find_elements("xpath", '//tbody[1]/tr/td')
        #get the iso639-3 field in the phoible language to connect to geo_data
        element_with_url = self.driver.find_element("xpath", '//tbody[1]/tr/td/a')

        if self.dic['name'] == 'phoible':
            #this needs to return simply an iso code.
            iso = self.driver.find_element("xpath", '//tbody[1]/tr/td[2]/a')
            phoible_language = iso.text
            iso_url = iso.get_attribute('href')
            self.iso = self.phoible_iso(iso_url=iso_url)
            inst = models.Lang_iso(iso_639_3 = self.iso)
            inst.search_name_phoible = self.language
            inst.phoible_lang = phoible_language
            #experimenting with search key instead of language or iso in parse linguistics page
            self.search_key = iso
                    #     lang_geography['iso_639_3'] = self.phoible_iso(iso_url=iso_url)
        #if wals we want geo data and save in geodata table, if 
        elif self.dic['name'] == 'wals':
            inst = models.Lang_geography()
            for n,col in enumerate(cols):
                # may have some problematic elements
                key = str(col.text).lower().replace(' ', '_').replace('-','_').replace('#','num').replace("name","language")
                val = elements[n].text.replace(' ','_').lower().strip()
                #this is the foreign key, so it needs to be an instance of the Lang_iso model
                if key == 'language':
                    lang = val
                if key == 'iso_639_3':
                    val = models.Lang_iso.objects.get(iso_639_3 = val)
                    try:
                        val.wals_lang = lang
                        val.save()
                    except:
                        pass
                    
                setattr(inst, key, val)
        inst.save()
        #currently lang geography has all fields.        
        #lang_geography to save to another table. update url to follow link
        self.url = element_with_url.get_attribute('href')
        # if iso_url:
        #     lang_geography['iso_639_3'] = self.phoible_iso(iso_url=iso_url)
        # print(lang_geography)
        # if self.dic['name']
        # return lang_geography
    
    #this finds the second item after a language search (in the language field) 
    #this will follow the phoible language link and find the iso639-3 code to correlate to geodata
    def phoible_iso(self, iso_url):
        #PHOIBLE ONLY, FIND ISOCODE

        inventory_page = urllib.request.urlopen(iso_url)
        # print('inv:',inventory_page)
        iso_soup = BeautifulSoup(inventory_page, "html.parser")
        result = str(iso_soup.find("span", class_ = "iso639-3").text.strip())
        return result
    
    def examples(self, phoneme_name):
        url = fr'https://en.wikipedia.org/wiki/{phoneme_name}'

    def main(self):
        #reads from self to get language and dictionary
        #parse phoible and iso, then use that iso to parse lang_geo and wals data
        self.find_language_in_search()
        df = self.parse_linguistics_page()
        if self.iso:
            return [df, self.iso]
        else:
            return [df, None]
#input languages to process. needs input menus if there are multiple repositories.

#structure: input language, query db, either fetch or ask for clarification. 
class analysis_structure:
    def __init__(self, languages, feature_site = 'phoible'):
        self.languages = languages
        self.feature_site = feature_site
        self.table = config.parser_dics[self.feature_site]['model']
        self.engine = sqlalchemy.create_engine(config.database_url, echo = False)

    def grouping_features(self):
        #use sql alchemy because it is faster for batch insertion
        groupings = []
        feature_sets = {}
        reps = {}
        # href_dic = {}
        audio_hrefs = models.Ipa_phonemes_audio_href.objects.only('phoneme','audio_href')
        hrefs = pd.DataFrame.from_records(audio_hrefs.values())
        
        for n,lang in enumerate(self.languages):
            phoneme_qs = models.Phonetics.objects.filter(language = lang)
            if not phoneme_qs:

                df, self.iso = search_and_parse(language = lang, feature_site = "phoible").main()
                df.to_sql(f'lang_comparison_phonetics', index = False, con = self.engine, if_exists = 'append', schema = 'public')
                search_and_parse(language = lang, feature_site = "wals", iso_code = self.iso).main()[0].to_sql(f'lang_comparison_grammar', index = False, con = self.engine, if_exists = 'append', schema = 'public')

                phoneme_qs = models.Phonetics.objects.filter(language = lang)

            lang_df = pd.DataFrame.from_records(phoneme_qs.values())
            hrefs = hrefs.rename(columns ={'phoneme':'segment'})
            merged = lang_df.merge(hrefs, how = 'inner', on = 'segment')
            print(merged)
            # lang_df.merge(hrefs)
                #set default column as language
            for m,l in enumerate(lang_df['segment']):
                #connect to sql table, need to find db to connect to, lambda/aws or postgres?
                #celery/ redis broker
                reps.setdefault(l, [0,None])
                reps[l][0] = int(lang_df['representation_percent'][m])
                if (merged['segment'] == l).any():
                    reps[l][1] = str(merged.loc[merged['segment'] == l, 'audio_href'].iloc[0])
                # row_dic = {'phoneme':l,'rep':rep, 'truths':}
                # rep = lang_df[lang_df['segment']==l]['representation_percent'].to_list()[0]
                feature_sets.setdefault(l, list(bytearray(len(self.languages))))
                feature_sets[l][n] = 1

            #needs a total rewrite
            groupings.append(lang_df)
        reps_s = sorted(reps.items(), key=lambda item: item[1][0], reverse = True)
        keys = feature_sets.keys()
        print(reps_s)
        feat_list = [[{'phoneme':l,'hr':p[1]},str(p[0])+'%'] + feature_sets[l] for (l,p) in reps_s]
        # print(feat_list)
        return self.languages, feat_list
# wikipedia_ipa_scrape().parse_ipa(url = 'https://en.wikipedia.org/wiki/IPA_vowel_chart_with_audio')
#https://en.wikipedia.org/wiki/Voiced_velar_fricative to find examples of the ipa symbol, use ipa symbol name to go to page and parse.

# print(analysis_structure(['English','Russian']).grouping_features())
        
    # groups_for_sets.append(total_col)
# df_grid = pd.DataFrame(columns = [i for i in set(total_col)], index = [lang for lang in languages]).fillna(False)
# for n,lang in enumerate(languages):
#     for k in df_grid.keys():
#         print(k)
#         if k in groups_for_sets[n]:
#             df_grid.at[lang,k] = True
#             #     print(languages[:n+1])
# print(df_grid)
#all matched items, matched by groups. comparison to global representat