import logging
import requests
import kodilogging
import xbmcaddon
import utils


API_BASE_URL = 'https://api.nhk.or.jp/nhkworld/'
NHK_BASE_URL = 'https://www3.nhk.or.jp'

API_LANGUAGE = 'en'
API={}


def create_command(prefix, resource):
    return('{0}_{1}'.format(prefix,resource))

def get_API_from_NHK():
    raw_API_json = utils.get_json('https://www3.nhk.or.jp/nhkworld/assets/api_sdk/api.json')
    nhk_api = {}
    for row in raw_API_json['api']:
        prefix = row['prefix']
        version = row['version']
        for resource in row['resources']:
            command = create_command(prefix,resource)
            params = row['resources'][resource]
            nhk_api.update({ command: {'version': version, 'params': params}})
           
    return(nhk_api)


def get_full_API_url(path):
    return(API_BASE_URL + path)

def get_full_NHK_url(path):
    return(NHK_BASE_URL + path)

def replace_path_parameters_version_language(path, version, language):
    path = path.replace('{version}', version)
    path = path.replace('{lang}', language)
    return(path)


def get_homepage_ondemand_url():
    command = create_command('vod','RecommendListFetch')
    version = API[command]['version']
    params = API[command]['params']
    path = str(params['path'])
    path = replace_path_parameters_version_language(path, version, API_LANGUAGE)
    path = get_full_API_url(path)
    return(path)

def get_homepage_news_url():
    command = create_command('news','ListFetch')
    params = API[command]['params']
    path = str(params['path'])
    path = get_full_NHK_url(path)
    return(path)


def get_livestream_url():
    command = create_command('tv','EPGFetch')
    params = API[command]['params']
    version = API[command]['version']
    path = str(params['path'])
    path = path.replace('{version}', version)
    path = path.replace('{region}', 'world')
    path = path.replace('{Time}', 'now')
    path = get_full_API_url(path)
    return(path)


API = get_API_from_NHK()