# Generated by Django 4.1.2 on 2023-03-09 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lang_comparison', '0002_rename_representation_percentage_phonetics_representation_percent_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Intersections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneme', models.CharField(max_length=10)),
                ('language_list', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ipa_phonemes_audio_href',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneme', models.CharField(max_length=10)),
                ('segment_class', models.CharField(max_length=30)),
                ('segment_name', models.CharField(max_length=70)),
                ('vowel_height', models.CharField(max_length=20, null=True)),
                ('vowel_forward', models.CharField(max_length=20, null=True)),
                ('vowel_round', models.CharField(max_length=11, null=True)),
                ('vowel_diacritics', models.CharField(max_length=30, null=True)),
                ('consonant_manner', models.CharField(max_length=20, null=True)),
                ('consonant_articulation', models.CharField(max_length=20, null=True)),
                ('consonant_voiced', models.CharField(max_length=11, null=True)),
                ('consonant_diacritics', models.CharField(max_length=30, null=True)),
                ('audio_href', models.URLField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Phoneme_examples',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneme', models.CharField(max_length=10)),
                ('language', models.CharField(max_length=30, null=True)),
                ('example', models.CharField(max_length=50)),
            ],
        ),
    ]
