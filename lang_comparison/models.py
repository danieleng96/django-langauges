from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields): #**kwargs same
        if not email:
            raise ValueError('Please include email')
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('', True)

        
class Lang_iso(models.Model):

    iso_639_3 = models.CharField(max_length = 10, primary_key=True)
    search_name_phoible = models.CharField(null = False, max_length = 30)
    phoible_lang = models.CharField(null = False, max_length = 30)
    wals_lang = models.CharField(null = False, max_length = 30)

class Ipa_phonemes_audio_href(models.Model):
    phoneme = models.CharField(null = False, max_length = 10)
    segment_class = models.CharField(null = False, max_length = 30)
    #full name, i.e. Voiced_palatal_affricate
    segment_name = models.CharField(null = False,  max_length=70)
    vowel_height = models.CharField(null = True, max_length = 30)
    vowel_forward = models.CharField(null = True, max_length = 30)
    vowel_round = models.CharField(null = True, max_length = 11)
    vowel_diacritics = models.CharField(null = True, max_length = 30)
    consonant_manner = models.CharField(null = True, max_length = 30)
    consonant_articulation = models.CharField(null = True, max_length = 30)
    consonant_voiced = models.CharField(null = True, max_length = 11)
    consonant_diacritics = models.CharField(null = True, max_length = 30)
    audio_href = models.URLField(null = True, max_length = 100)

    def __str__(self):
        return self.phoneme, self.audio_href
    

#language specific phonemes, phoible
class Phonetics(models.Model):

    phoneme_desc = models.ForeignKey(Ipa_phonemes_audio_href, on_delete=models.SET_NULL, null = True)
    iso_639_3 = models.ForeignKey(Lang_iso, on_delete=models.SET_NULL, null = True)

    language = models.CharField(null = False, max_length = 30)
    segment_class = models.CharField(null = False, max_length = 30)
    segment = models.CharField(null = False, max_length = 10)
    marginal = models.BooleanField(default = False)
    allophones = models.CharField(default = False, max_length = 30)
    representation_percent = models.IntegerField(null = False)
    create_time = models.DateTimeField(auto_now_add = True)
    update_time = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return f'{self.language}, {self.segment}'
    
    #might not be relevant, can make table with just phoible language name, iso, alternate names. 
# class Lang_inv(models.Model):
#     inventory = models.CharField(null = False, max_length = 30)
#     #must be custom added
#     iso_639_3 = models.CharField(null = False, max_length = 10)
#     #added at same time as phonetics table, save phonetics table first and connect
#     language =  models.ForeignKey(Phonetics, on_delete=models.CASCADE, null = False)
#     num_segments = models.IntegerField(null = False)
#     num_vowels = models.IntegerField(null = False)
#     num_consonants = models.IntegerField(null = False)
#     num_tones = models.IntegerField(null = False)
#     contributor = models.CharField(null = False, max_length = 30)
#     cite = models.CharField(null = False, max_length = 30)

    #basic language with alternate names


#need to take from wals.info/languoid. more info than at phoible
class Lang_geography(models.Model):
    
    language = models.CharField(null = False, max_length = 30)
    wals_code = models.CharField(null = True, max_length = 5)
    iso_639_3 = models.ForeignKey(Lang_iso, on_delete=models.SET_NULL, null = True)
    genus = models.CharField(null = True, max_length = 30)
    family = models.CharField(null = True, max_length = 30)
    latitude = models.FloatField(null = True)
    longitude = models.FloatField(null = True)
    macroarea = models.CharField(null = True, max_length = 50)
    countries =  models.CharField(null = True, max_length = 70)
#from phoible, could be useful
#1 model, get phoible data first

#wals page wals.info/languoid/lect/wals_code_{code}
class Grammar(models.Model):
    iso_639_3 = models.ForeignKey(Lang_iso, on_delete=models.SET_NULL, null = True)

    language = models.CharField(null = True, max_length= 200)
    fid = models.CharField(null = False, max_length= 7)
    value = models.CharField(null = False, max_length= 200)
    reference = models.CharField(null = True, max_length= 200)
    feature = models.CharField(null = True, max_length= 200)
    area = models.CharField(null = True, max_length= 200)

#a growing intersection table
class Intersections(models.Model):
    phoneme = models.CharField(null = False, max_length = 10)
    language_list = models.CharField(null = True, max_length= 200)
#collect examples of phonemes in target language

class Phoneme_examples(models.Model):
    phoneme = models.CharField(null = False, max_length = 10)
    iso_639_3 = models.ForeignKey(Lang_iso, on_delete=models.SET_NULL, null = True)
    example = models.CharField(null = False, max_length=50)
#this table should be independent of any languages and should be populated at the same time, either with trigger or foreign keys.
#needs to be added to trigger. could be better as an unstructured json NoSql.
