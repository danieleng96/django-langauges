from django.shortcuts import render
from  django.urls import reverse
from django.shortcuts import render,redirect,get_object_or_404
from django.utils.text import slugify   
from datetime import date
from django.http import HttpResponse
from django.conf import settings
from lang_comparison import language_parser as lp
from .import models
from .filters import language_filter

def vac(request):
    return render(request, 'lang_comparison/vacuum_screen.html')

def try_geo_data(request):
    lp.analysis_structure(['Korean'], feature_site='wals').grouping_features()
    return HttpResponse(f'Finished syncing phonemes')
#function based views

def sync_audio_to_phonemes(request):
    phonemes = models.Phonetics.objects.all()
    i = 0
    for row in phonemes:
        if not row.phoneme_desc:      
            try:
                row.phoneme_desc = models.Ipa_phonemes_audio_href.objects.get(phoneme = row.segment)
                row.save()
                i =+ 1
            except:
                pass
    return HttpResponse(f'Finished syncing phonemes {i}')


def input_phoneme_features(request):
    # url = 'https://en.wikipedia.org/wiki/IPA_vowel_chart_with_audio'
    url = 'https://en.wikipedia.org/wiki/IPA_pulmonic_consonant_chart_with_audio'
    lp.wikipedia_ipa_scrape().parse_consonant_ipa(url)
    return HttpResponse(f'Finished inserting phonemes from {url}')

def input_parse_language(request, langstring):
    # languages = request.session['language']
    languages = langstring.split('-')
    # phoneme_qs = models.Phonetics.objects.all().values()
    # print('Phonemes:' ,phoneme_qs)
    #
    
    titles, features  = lp.analysis_structure(languages, 'phoible').grouping_features()
    print('feats',titles)
    # print(type(check_grid))
    
    return render(request, 'lang_comparison/show_table.html', {'titles':titles, 'features':features})

    # return HttpResponse(check_grid.to_html())
    # return HttpResponse(request)


    # return HttpResponse(check_grid.to_html())
    # return render(request, 'mainapp/analysis_sidebar.html', {'script':script, 'div':div, 'number_values':{'cats': num_cat, 'val':num_values, 'tot':values}, 'scale':scale})

def custom_search_phonemes(request):

    language = request.GET.get('f', None)
    phonemes = models.Phonetics.objects.all()


    phonemes_filter = language_filter(request.GET, queryset = phonemes)
    # add_languages to sessions to have a running list.
    if 'language' in request.session:

        if language not in request.session['language']:
            request.session['language'].append(language)
        else:
            request.session['language'] = []
        request.session.modified = True
    previous_pages = []
    langstring = ''
    for l in request.session['language']:
        if l:
            previous_pages.append(phonemes.filter(language = l).order_by('-representation_percent'))
            if langstring == '':
                langstring = l
            else:
                langstring+='-'+l
    if langstring == '':
        langstring = None
        langlist = []
    else:
        langlist = langstring.split('-')
    
    return render(request, 'lang_comparison/search_all.html',{'filter': phonemes_filter,'previous_pages':previous_pages, 'langlist':langlist,'langstring':langstring})

