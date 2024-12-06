"""
File: querry_bunch_projects.py
Author: Antoine Laurent
Email: alaurent@agencemobilitedurable.ca
Github: https://github.com/alaurent34
Description:
"""

import itertools
import json
import os
import re
import unicodedata

import requests
import pandas as pd
import geopandas as gpd
from unidecode import unidecode

from lapin.constants import (
    SEG_DB_ID,
    SEG_DB_SIDE,
    SEG_DB_STREET
)

CURBSNAPP_HOST = os.environ.get('CURBSNAPP_HOST', '')
CURBSNAPP_KEY = os.environ.get('CURBSNAPP_KEY', '')
API_FETCH = 'api/fetchProjectData'
API_GEOBASE_SIMPLE = 'api/fetchGeobase'
API_GEOBASE_DOUBLE = 'api/fetchGeobaseDouble'
API_CONNECT = 'api/login'

GEOBASE_DBL_COL_DROP = ['REVERSE', 'LENGTH', 'NONPARCOURU', 'MODIFIED']


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = (unicodedata.normalize('NFKD', value)
                            .encode('ascii', 'ignore')
                            .decode('ascii'))
        value = re.sub(r'[^\w\s-]', '', value.lower())

    return re.sub(r'[-\s]+', '-', value).strip('-_')


def connect(url, user: str, password: str) -> requests.Session:
    """_summary_

    Parameters
    ----------
    url : _type_
        _description_
    user : str
        _description_
    password : str
        _description_

    Returns
    -------
    requests.Session
        _description_
    """

    login_data = {'username': user, 'password': password}

    session = requests.Session()
    session.post(url, data=login_data, timeout=600)

    return session


def project_api_call(project_name: str,
                     url: str, active_session: str = None,
                     key: str = None) -> dict:
    """
    doc
    """

    data = {'projectId': project_name}

    if key:
        data['apiKey'] = key

    if active_session:
        restriction = active_session.post(url, json=data, timeout=600)
    else:
        restriction = requests.post(url, json=data, timeout=600)

    try:
        restriction = json.loads(restriction.text)
    except:
        print(restriction.text)
        restriction = {}

    return restriction


def merge_geobases(geobases_list: list[str]) -> gpd.GeoDataFrame:
    """_summary_

    Parameters
    ----------
    geobases_list : list
        _description_

    Returns
    -------
    gpd.GeoDataFrame
        _description_
    """
    if all(not geobase for geobase in geobases_list):
        return gpd.GeoDataFrame(
            columns=[
                SEG_DB_ID,
                SEG_DB_SIDE,
                SEG_DB_STREET,
                'geometry'
            ],
            crs='epsg:4326'
        )
    geobases_list = [gpd.read_file(json.dumps(geobase))
                     for geobase in geobases_list]
    return pd.concat(geobases_list)


def merge_capacities(capacities_list: list) -> dict:
    """TODO: Docstring for merge_capacities.

    :capacities_list: List of capacity objects
    :returns: TODO

    """
    return itertools.chain(*capacities_list)


def save_restrictions(project_name: str, capacity_array: dict):
    """TODO: Docstring for save_capacity.

    Parameters
    ----------
    project_name: str
        Name of the project

    """

    os.makedirs("./output/", exist_ok=True)

    with open("output/" + slugify(unidecode(project_name)) + "_capacity_array.json",
              'w+',
              encoding='utf-8'
             ) as f:
        json.dump(capacity_array, f)


def get_project_geobases(
    projects_list: list,
    geobase_type: str = 'simple'
) -> gpd.GeoDataFrame:
    """_summary_

    Parameters
    ----------
    projects_list : list
        _description_
    geobase_type: str, optional
        Type of geobase to querry. Value can be
        'simple' or 'double', by default 'simple'.

    Returns
    -------
    gpd.GeoDataFrame
        Geobase

    Raises
    -----
    ValueError
    """

    if geobase_type not in ['simple', 'double']:
        raise ValueError('invalid geobase_type provided.')

    host = CURBSNAPP_HOST + API_GEOBASE_SIMPLE
    if geobase_type == 'double':
        host = CURBSNAPP_HOST + API_GEOBASE_DOUBLE

    geobases = map(project_api_call, projects_list,
                   itertools.repeat(host),
                   itertools.repeat(None),
                   itertools.repeat(CURBSNAPP_KEY))

    geobase = merge_geobases(list(geobases))

    geobase.columns = [col.upper() if col != 'geometry' else col
                       for col in geobase.columns]

    # drop unwanted field
    geobase = geobase.drop(columns=GEOBASE_DBL_COL_DROP, errors='ignore')

    geobase = geobase.reset_index(drop=True)
    geobase = geobase.drop_duplicates()

    return geobase


def get_procject_capacities(projects_list: list,
                            user: str = None, pwd: str = None,
                            output: list[str] = None) -> dict:
    """_summary_

    Parameters
    ----------
    projects_list : list
        _description_
    user : str, optional
        _description_, by default None
    pwd : str, optional
        _description_, by default None
    output : list[str], optional
        _description_, by default None

    Returns
    -------
    dict
        _description_
    """
    if user and pwd:
        session = connect(url=CURBSNAPP_HOST+API_CONNECT, user=user, password=pwd) if user else None

        capacities = map(project_api_call, projects_list,
                         itertools.repeat(CURBSNAPP_HOST+API_FETCH),
                         itertools.repeat(session))
    else:
        capacities = map(project_api_call, projects_list,
                         itertools.repeat(CURBSNAPP_HOST+API_FETCH),
                         itertools.repeat(None),
                         itertools.repeat(CURBSNAPP_KEY))

    merge = len(projects_list) > 1

    # save
    if output:
        projects_list=output

    if merge:
        capacities = merge_capacities(list(capacities))
        capacities = [list(capacities)]
    else:
        capacities = list(capacities)

    list(map(save_restrictions, projects_list, capacities))

    capacities = capacities[0]

    return capacities
