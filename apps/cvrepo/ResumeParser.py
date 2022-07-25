# import nltk
# nltk.download('stopwords')
from pyresparser import ResumeParser
import re


phone_pattern = r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'


def resume_parsing(resume_path):
    try:
        data = ResumeParser(resume_path, custom_regex=phone_pattern)
        return data.get_extracted_data()
    except:
        data = {}
        return data


def get_name(name):
    data = {}
    try:
        name = re.findall(pattern='[a-zA-Z ]*', string=name)
        name = [str(item).strip() for item in name if len(item) > 0]
        name = name[0].split()
        if len(name)>1:
            data['first_name'] = name[0]
            data['last_name'] = " ".join(name[1:])
        elif len(name) == 1:
            data['first_name'] = name[0]
            data['last_name'] = ''
        else:
            data['first_name'] = ''
            data['last_name'] = ''
        return data
    except:
        data['first_name'] = ''
        data['last_name'] = ''
