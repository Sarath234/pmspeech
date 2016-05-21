# coding: utf-8
import pandas as pd
import re
import json
import nltk
import unicodedata


def ProcessText(s):
    s = unicodedata.normalize('NFKD', unicode(s))
    s = u"".join([c for c in s if not unicodedata.combining(c)])
    s = s.translate({0x2018: 0x27, 0x2019: 0x27, 0x201C: 0x22,
                     0x201D: 0x22}).encode('ascii', 'ignore')
    s = re.sub(r'\s+', ' ', s)
    return s.lower()


def MostCommon(s):
    s = nltk.word_tokenize(s)
    s = [w for w in s if w not in stopwords]
    l = float(len(s))
    s = nltk.FreqDist(s).most_common()
    return s

if __name__ == '__main__':
    f = open("abvmmsspeech.json")
    data = json.load(f)
    data = pd.DataFrame.from_dict(data)
    data.loc[:, 'speech'] = data[['speech1', 'speech2', 'speech3']].apply(
        lambda s: ' '.join(s['speech1'] + s['speech2'] + s['speech3']), axis=1)
    data = data.drop(['speech1', 'speech2', 'speech3'], axis=1)
    data.loc[:, 'date'] = data.datenplace.apply(lambda s: s[0])
    data.loc[:, 'place'] = data.datenplace.apply(
        lambda s: s[1] if len(s) > 1 else '')
    data.loc[:, 'pm'] = data.link.apply(lambda s: s.split('/')[3])
    data = data[['date', 'place', 'pm', 'title', 'speech']]
    data.loc[:, 'title'] = data.title.apply(ProcessText)
    data.loc[:, 'speech'] = data.speech.apply(ProcessText)
    data_speech = data.groupby('pm', as_index=False).agg(
        {'speech': lambda s: '. '.join(s)})
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords = stopwords + ["prime", '.', ',', 'also',
                             "minister", "'s", "pm", "address", "speech"]
    print data_speech.speech.apply(MostCommon)
