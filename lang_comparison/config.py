parser_dics = {'wals':{'name':'wals',
            'url':"https://wals.info/languoid",
            'tags':['fid','value','feature','area','reference'], 'model':'grammar',
            'id':'Datapoints',
            'exclude':[4]},'phoible':{'name':'phoible',
               'url':"https://phoible.org/inventories",
               'tags':['segment_class','segment','marginal','allophones','representation_percent'],
               'id':'Phonemes',
               'model':'phonetics',
               'exclude':None}}

from django.conf import settings

user = settings.DATABASES['default']['USER']
password = settings.DATABASES['default']['PASSWORD']
database_name = settings.DATABASES['default']['NAME']
# host = settings.DATABASES['default']['HOST']
# port = settings.DATABASES['default']['PORT']

database_url = 'postgresql+psycopg2://{user}:{password}@localhost:5432/{database_name}'.format(
    user=user,
    password=password,
    database_name=database_name,
)
