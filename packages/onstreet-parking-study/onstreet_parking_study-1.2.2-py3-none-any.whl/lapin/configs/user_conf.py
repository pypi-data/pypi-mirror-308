"""User config parser."""
import os
import configparser
import re
import json
import logging
import pathvalidate
import pandas

from lapin.configs.others import (
    DELIM_CONNECTION,
    GEOREF_CP_CONNECTION,
    PROV_CONF,
    VIS_DELIM_CONNECTION
)
from lapin.configs.tennery_creek import (
    LPR_CONNECTION,
    VEH_CONNECTION,
)
from lapin.configs.mtl_opendata import (
    ROADS_CONNECTION,
    ROADS_DB_CONNECTION,
)

logger = logging.getLogger(__name__)


def str2bool(string):
    ''' Interpret a string to a boolean. '''
    if (string in ['True', 'true', '1', 'y', 'Y']):
        return True
    return False

def string2type(x, i_type='int'):
    if(i_type == 'float'):  return float(x)
    elif(i_type == 'bool'): return str2bool(x)
    elif(i_type == 'int'):  return int(x)
    elif(i_type == 'path'): return path_slashes(x)
    elif(i_type == 'numeric'):
        try:    return int(x)
        except: return float(x)
    else:                   return x

def raw(string):
    ''' Returns a raw string representation of text. '''
    escape_dict={'\a':r'\a','\b':r'\b','\c':r'\c','\f':r'\f','\n':r'\n',
                 '\r':r'\r','\t':r'\t','\v':r'\v','\'':r'\'',
                 '\0':r'\0','\1':r'\1','\2':r'\2','\3':r'\3','\4':r'\4',
                 '\5':r'\5','\6':r'\6','\7':r'\7','\8':r'\8','\9':r'\9'}
    new_string=''
    for char in string:
        try: new_string+=escape_dict[char]
        except KeyError: new_string+=char
    return new_string

def path_slashes(string):
    ''' Convert windows' backslashes or unix slashes to OS's type . '''
    inter = raw(string).replace('\\', os.sep)
    return raw(inter).replace('/', os.sep)

def parseDictString(item):
    start=item.find('{')
    end=item.rfind('}')
    content = item[start+1:end]

    keys=[]
    values=[]
    part=''
    openB=0 #accounting for internal dicts/lists/tuples
    skipT=False #accounting for strings
    for c in content:
        if c in '{[(':
            openB+=1
        if c in ')]}':
            openB-=1
        if c in ['"',"'"] and not skipT:
            skipT=True
        if c not in ':,' or openB > 0 or skipT:
            part+=c
        else:
            if len(keys) == len(values):
                keys.append(part.strip())
            else:
                values.append(part.strip())
            part=''
        if c in ['"',"'"] and skipT:
            skipT=False

    if part != '':
        values.append(part.strip())

    return keys, values

##################
### Structures
##################
def list1D(item, i_type='int', type=list):
    ''' Parse string format into 1 dimensional array (values).
    Will automatically generate range for int values (i.e. [1,3-5] -> [1,3,4,5]).

    Alternative:
    ============
    import ast
    x = '[0.90837,0.90837]'
    ast.literal_eval(x)
    '''
    translator = str.maketrans({key: None for key in ['[',']',' ','\n']})
    item = item.translate(translator).split(',')
    item = list(filter(None, item))
    if(len(item) > 0):
        if(i_type == 'int'):
            if(len(list(set(item))) != len(item)): allowDuplicates = True
            else:                                  allowDuplicates = False
            for i in range(len(item)):
                if('-' in item[i]):
                    temp    = item[i].split('-')
                    item   += list(range(int(temp[0]),int(temp[-1])+1))
                    item[i] = None
            item = list(filter(None, item))
            if(not allowDuplicates):
                item = list(set(item))
            return type(sorted([int(x) for x in item]))
        else: return type([string2type(x, i_type=i_type)for x in item])
    else:
        return type([])

def list2D(item, i_type='int', type=list):
    ''' Parse string format into 2 dimensional array (values).
    set type=list to gt a list back or type=tuple to get a tuple back'''
    translator = str.maketrans({key: None for key in [' ','\n']})
    parsing = item.translate(translator)
    parsing = parsing.split('],[')
    parsing = list(filter(None, parsing))
    item =[]
    if(len(parsing) > 0):
        translator = str.maketrans({key: None for key in ['[',']','(',')',',']})
        for i in range(len(parsing)):
            parsingx = parsing[i].split(',')
            for j in range(len(parsingx)):
                parsingx[j] = parsingx[j].translate(translator)
            item.append(type([string2type(x, i_type=i_type) for x in parsingx]))
        return type(item)
    else:
        return type(type())

PAR = re.compile("\(([^)]+)\)", re.VERBOSE)
BRA = re.compile("\[([^)]+)\]", re.VERBOSE)

PAREXTRACT = re.compile("((?<=\()(?:[^()]+\([^)]+\)))", re.VERBOSE)

def mixedList(item, i_type='int'):
    ''' Parse string format into 1 dimensional array that can contain list-like
    elements. Ex: '[1,2,(2,3)]' -> [1,2,(2,3)]
    '''
    translator = str.maketrans({key: None for key in [' ','\n']})
    parsing = item.translate(translator)
    parsing = [x for x in BRA.split(parsing, maxsplit=1) if x != ''][0]

    item=[]
    if(len(parsing) > 0):
        flag=tuple
        brasearch = BRA.search(parsing)
        if brasearch:
            parsing = parsing.replace('[','(')
            parsing = parsing.replace(']',')')
            flag = list

        parsearch = PAR.search(parsing)
        if not parsearch: return list1D(parsing, i_type=i_type)

        beg = parsing.split(r'(')[0]
        end = parsing.split(r')')[-1]
        mid = parsing[len(beg)+1:-(len(end)+1)]

        item += list1D(beg, i_type=i_type)
        item.append(flag(list1D(mid,  i_type=i_type)))
        item += list1D(end, i_type=i_type)

        return item
    else:
        return [[]]

def dictND(item, i_type='int', k_type='str'):
    """Parse string format to extract a dictionnary that can contain subcontainers
    (list1d, tuple1d, list2d, tuple2d, mixedList, dictionnary) as long as the
    internalmost elements all follow i_type. Keys must all match the same k_type.

    i1 = 'trailing {10:[1], 4:2, 6:[1,2,(2,3)], 1000:{3:1, 99: 2}}'
    i2 = 'trailing {this:[1], 3:2, containing:[1,2,(2,3)], and:{a:1, with a: 2}}'
    dictND(i1, i_type='int', k_type='int')
        >>> {10:[1],
             4:2,
             6:[1,2,(2,3)],
             1000:{3:1, 99: 2}
             }

    dictND(i2, i_type='int', k_type='str')
        >>> {'this':[1],
             '3':2,
             'containing':[1,2,(2,3)]
             'and':{'a':1, 'with a': 2}
             }
    """
    keys, values = parseDictString(item)
    base = {string2type(keys[i],i_type=k_type): values[i] for i in range(len(keys))}

    for k,v in base.items():
        if '[[' in v and ']]' in v:
            base[k] = list2D(v, i_type=i_type, type=list)
        elif '((' in v and '))' in v:
            v = v.replace('((','[[')
            v = v.replace('))',']]')
            base[k] = list2D(v, i_type=i_type, type=tuple)
        elif '(' in v and '[' in v and ']' in v and ')' in v:
            base[k] = mixedList(v, i_type=i_type)
        elif '[' in v and ']' in v:
            base[k] = list1D(v, i_type=i_type, type=list)
        elif '(' in v and ')' in v:
            v = v.replace('(','[')
            v = v.replace(')',']')
            base[k] = list1D(v, i_type=i_type, type=tuple)
        elif '{' in v and '}' in v:
            base[k] = dictND(v, i_type=i_type, k_type=k_type)
        else:
            base[k] = string2type(v, i_type=i_type)
    return base

##################
### Write utils
##################
def split_list(items, max_item_per_line=5, pad_newlines_with=' ', sep=', ',
               end_bracket_on_newline=True, c_type='list'):
    if max_item_per_line is None:
        max_item_per_line = len(items)
    string='[' if c_type=='list' else '('
    is_additional_line=False
    while len(items) > 0:
        if is_additional_line:
            string += ',\n'+pad_newlines_with
        string += sep.join([f"{i}" for i in items[0:max_item_per_line]])
        items = items[max_item_per_line:]
        if len(items) > 0:
            is_additional_line=True

    if end_bracket_on_newline and is_additional_line:
        string += '\n'+pad_newlines_with
    string+=']' if c_type=='list' else ')'
    return string

def split_dict(dictio, max_key_per_line=1, pad_newlines_with=' ', sep=', ',
               end_bracket_on_newline=True, max_split_inside_list=5):

    if len(dictio) == 0:
        return "{}"

    items = list(dictio.keys())
    greatest_key = max([len(f"{k}") for k in items])
    pad_internal_with = ''.join([' ' for i in range(greatest_key+3)]) + pad_newlines_with

    string='{'
    is_additional_line=False
    while len(items) > 0:
        if is_additional_line:
            string += ',\n'+pad_newlines_with
        keys = items[0:max_key_per_line]

        stacks=[]
        for key in keys:
            if isinstance(dictio[key], list):
                stringvalue=split_list(dictio[key], end_bracket_on_newline=False,
                                       max_item_per_line=max_split_inside_list,
                                       pad_newlines_with=pad_internal_with,
                                       sep=sep, c_type='list'
                                       )
            elif isinstance(dictio[key], tuple):
                stringvalue=split_list(dictio[key], end_bracket_on_newline=False,
                                       max_item_per_line=max_split_inside_list,
                                       pad_newlines_with=pad_internal_with,
                                       sep=sep, c_type='tuple'
                                       )
            elif isinstance(dictio[key], dict):
                stringvalue=split_dict(dictio[key], end_bracket_on_newline=False,
                                       max_split_inside_list=max_split_inside_list,
                                       pad_newlines_with=pad_internal_with,
                                       sep=sep, max_key_per_line=max_key_per_line
                                       )
            else:
                stringvalue=f"{dictio[key]}"
            stacks.append(f"{key}: {stringvalue}")
        string+=sep.join(stacks)
        items = items[max_key_per_line:]
        if len(items) > 0:
            is_additional_line=True

    if end_bracket_on_newline and is_additional_line:
        string += '\n'+pad_newlines_with
    string+='}'
    return string

##################
###### Helpers
#################

def build_cache(path):
    cache = os.path.join(path, 'cache')
    os.makedirs(cache, exist_ok=True)

def build_results(path):
    cache = os.path.join(path, 'resultat')
    os.makedirs(cache, exist_ok=True)

def build_dates(days_bounds):
    LPR_CONNECTION['dates'] = days_bounds
    VEH_CONNECTION['dates'] = days_bounds

def set_delimns(gis_bounds, gis_vis_bounds):
    DELIM_CONNECTION['filename'] = gis_bounds
    VIS_DELIM_CONNECTION['filename'] = gis_vis_bounds

def set_prov_origin(prov_origin_filename):
    GEOREF_CP_CONNECTION['filename'] = prov_origin_filename

def set_prov_conf(conf):
    PROV_CONF["act_prov"] = conf.act_prov
    PROV_CONF["cp_base_filename"] = conf.plates_origin_file_name
    PROV_CONF["cp_folder_path"] = conf.plates_origin_path
    PROV_CONF["cp_regions_bounds"] = conf.plates_origin_bounds
    PROV_CONF["cp_regions_bounds_names"] = conf.plates_origin_bounds_name
    PROV_CONF["plates_periods"] = conf.plates_origin_periods
    PROV_CONF["cp_conf"] = GEOREF_CP_CONNECTION

def set_roads(roads_path, roads_dbl_path, projects_id):
    # OPTIONAL
    if roads_path != 'Default.def':
       ROADS_CONNECTION['filename'] = roads_path
    if roads_dbl_path != 'Default.def':
       ROADS_DB_CONNECTION['filename'] = roads_dbl_path

    ROADS_CONNECTION['config']['projects_list'].extend(projects_id)
    ROADS_DB_CONNECTION['config']['projects_list'].extend(projects_id)

##################
### Configuration
##################
class LapinConfig():
    """_summary_
    """
    def __init__(self):

        self.num_proj = 0
        self.title_proj = ''
        self.client_proj = ''
        self.work_folder = './'
        self.curbsnapp_projects_id = []

        # options
        self.act_occup = False
        self.act_rempla = False
        self.act_prov = False
        self.comp_sect_agg = False
        self.handle_restriction = False
        self.one_way_agg = False
        self.act_report = False

        # parameters
        self.gis_bounds = ''
        self.gis_bounds_names = ''
        self.gis_ana_vis_same_bounds = ''
        self.days_bounds = []
        self.hour_bounds = {}
        self.analyse_freq = ''
        self.allow_veh_on_restrictions = ''
        self.restrictions_to_exclude = ''
        self.plates_origin_path = ''
        self.plates_origin_file_name = ''
        self.plates_origin_bounds = ''
        self.plates_origin_bounds_name = ''
        self.plates_origin_periods = {}
        self.plates_origin_gis = ''
        self.report_street_name = ['']
        self.vehicule_conf = {}

        # optional
        self.roads_path = 'Default.def'
        self.roads_dbl_path = 'Default.def'
        self.ignore_agg_seg = []
        self.gis_vis_bounds = "Path\to\file.json"
        self.gis_vis_bounds_names = "-"
        self.vis_rotation = []
        self.vis_buffer = []
        self.veh_size = 5.5
        self.compass_rose = True
        self.anotation = True
        self.capa_along_occ = False
        self.build_leg = False
        self.anotation_prov = True
        self.regs_zoom_prov = []
        self.plot_all_capa = False

class UserConfig(LapinConfig):
    """_summary_

    Parameters
    ----------
    LapinConfig : _type_
        _description_
    """

    def __init__(self, config_name, encoding='latin-1'):

        # default
        super().__init__()

        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.read(config_name, encoding=encoding)

        self.handles=[]

        self.section = 'DESCRIPTION'
        self.store("num_proj",             "Numéro de projet [required]",       "1",               c_type='int')
        self.store("title_proj",           "Titre de projet  [required]",       "<Titre>",         c_type='string')
        self.store("client_proj",          "Client",                            "<Client>",        c_type='string')
        self.store("work_folder",          "Dossier de travail [required]",     "Path\to\folder",  c_type='path', p_type='folder')
        self.store("curbsnapp_projects_id", "No de projet Curbsnapp [required]", "[]",              c_type='string', c_struct='list1D')

        self.section = 'OPTIONS'
        self.store("act_occup",            "Analyser les occupations",                                                  "True",  c_type='bool')
        self.store("act_rempla",           "Analyser le remplacement",                                                  "False", c_type='bool')
        self.store("act_prov",             "Analyser les provenances",                                                  "False", c_type='bool')
        self.store("comp_sect_agg",        "Aggréger par secteurs",                                                     "True",  c_type='bool')
        self.store('handle_restriction',   "Calculer uniquement les points sur zone non restrainte",                    'True',  c_type='bool')
        self.store("one_way_agg",          "Agréger les rues à sens unique",                                            "False", c_type='bool')
        self.store("act_report",           "Modéliser le report des stationnements d'une rue sur les rues avoisinante", "False", c_type='bool')

        self.section = 'PARAMÈTRES'
        self.store("gis_bounds",                 "Analyse - Fichier des limites",                         "Path\to\file.json",                            c_type='path',   p_type='file')
        self.store("gis_bounds_names",           "Analyse - Header des noms de limites",                  "Nom",                                          c_type='string')
        self.store("gis_ana_vis_same_bounds",    "Carto et Analyse - Même fichier GIS",                   "True",                                         c_type='bool')
        self.store("days_bounds",                "Dates de collecte",                                     '[{"from":"2000-01-01", "to":"2099-12-31"}]',   c_struct='json')
        self.store("hour_bounds",                "Jours et heures d'analyse",                             '{"lun-dim":[{"from": "0h00", "to":"23h59"}]}', c_struct='json')
        self.store("analyse_freq",               "Fréquence d'analyse",                                   "1h",                                           c_type='string')
        self.store("allow_veh_on_restrictions",  "Liste des infractions où l'on autorise le stat.",       '["Borne fontaine"]',                           c_struct='json')
        self.store("restrictions_to_exclude",    "Liste des réglementations à exclure",                    '["Défaut"]',                                  c_struct='json')
        self.store("plates_origin_path",         "Provenance - Emplacement des fichiers de plaque",       "Path\to\folder",                               c_type='path',   p_type='folder')
        self.store("plates_origin_file_name",    "Provenance - Squelette nom des fichiers de plaque",     "Plaques_zone_{}_periode_{}.XLS",               c_type='string')
        self.store("plates_origin_bounds",       "Provenance - Fichier géographique des zones de plaque", "Path\to\file.json",                            c_type='path',   p_type='file')
        self.store("plates_origin_bounds_name",  "Provenance - Header des noms de limites",               "Nom",                                          c_type='string')
        self.store("plates_origin_periods",      "Provenance - Périodes temporelle",                      "{}",                                           c_type='string', c_struct='dictND')
        self.store("plates_origin_gis",          "Provenance - Fichier des limites des code postaux",     "Path\to\file",                                 c_type='path',   p_type='folder')
        self.store("report_street_name",         "Report - Nom de la rue à reporter",                     "[]",                                          c_type='string', c_struct='list1D')
        self.store("vehicule_conf",              "Configuration des caméras",                            "{}",                                           c_struct='json')

        self.section = 'OPTIONEL'
        self.store("roads_path",            "Fichier de géobase personalisé",                         'Default.def',       c_type='path',  p_type='file')
        self.store("roads_dbl_path",        "Fichier de route double personalisé",                    'Default.def',       c_type='path',  p_type='file')
        self.store('ignore_agg_seg',        "Ignorer les segments dans l'aggrégation du coté de rue", "[]",                c_type='int',    c_struct='list1D')
        self.store("gis_vis_bounds",        "Carto - Fichier des limites",                            "Path\to\file.json", c_type='path',  p_type='file')
        self.store("gis_vis_bounds_names",  "Carto - Header des noms de limites",                     "-",                 c_type='string')
        self.store('vis_rotation',          "Carto - Rotation du Nord (degrés)*",                     "[]",                c_type='float', c_struct='list1D')
        self.store('vis_buffer',            "Carto - Distance au pourtour (m)*",                      "[]",                c_type='float', c_struct='list1D')
        self.store('veh_size',              "Longueur moyenne d'un véhicule",                         '5.5',               c_type='float')
        self.store('compass_rose',          "Affichage de la rose des vents",                         'True',              c_type='bool')
        self.store('anotation',             "Affichage des annotations",                              'True',              c_type='bool')
        self.store('capa_along_occ',        "Afficher la capacité avec l'occupation",                 'False',             c_type='bool')
        self.store('build_leg',             "Affichage de la légende dans la carte",                  'False',             c_type='bool')
        self.store('anotation_prov',        "Provenance - Affichage des annotations",                 'True',              c_type='bool')
        self.store('regs_zoom_prov',        "Provenance - Zoom sur des arrondissements",              "[]",                c_type='string', c_struct='list1D')
        self.store('plot_all_capa',         "Affichage de toutes les capacitées désagrégées",         'False',             c_type='bool')

        #finishing touches
        self.__dict__.pop('section')
        self.sections = self.config.sections()
        self.handles = pandas.DataFrame(self.handles)
        self._handle_potential_copies()
        self.init_config()

        if (not os.path.isfile(config_name)):
            logger.info('Notice: No default configuration found. Creating new %s', str(config_name))
            self.write(config_name)

    def _handle_potential_copies(self):
        candidates = {'gis_ana_vis_same_bounds':{'gis_vis_bounds':'gis_bounds',
                                                 'gis_vis_bounds_names':'gis_bounds_names'
                                                }
                      }

        for cand, _ in candidates.items():
            if getattr(self, cand):
                for dependent, keyed_to in candidates[cand].items():
                    value = getattr(self, keyed_to)
                    setattr(self, dependent, value)
                    self._update_handle_df(dependent, value)

    def _update_handle_df(self, key, value):
        handlesdf = self.handles.copy().set_index('attr')
        handlesdf.at[key, 'value'] = value
        self.handles = handlesdf.reset_index()

    def store(self, attr, key, default, c_type='int', c_struct='simple', k_type='str', p_type=None):
        """_summary_

        Parameters
        ----------
        attr : _type_
            _description_
        key : _type_
            _description_
        default : _type_
            _description_
        c_type : str, optional
            _description_, by default 'int'
        c_struct : str, optional
            _description_, by default 'simple'
        k_type : str, optional
            _description_, by default 'str'
        p_type : _type_, optional
            _description_, by default None

        Returns
        -------
        _type_
            _description_
        """
        value =  self.parse(key, default, c_type=c_type, c_struct=c_struct, k_type=k_type, p_type=p_type)
        self.handles.append({'section':self.section, 'attr':attr, 'text':key, 'value':value, 'c_type':c_type, 'c_struct':c_struct})
        setattr(self, attr, value)

        return value

    def parse(self, key, default, c_type='int', c_struct='simple', k_type='str', p_type=None):
        ''' Handle configuration file values. '''
        if(not self.config.has_section(self.section)):    self.config.add_section(self.section)
        if(not self.config.has_option(self.section,key)): self.config.set(self.section,key,default)

        if(c_struct == 'list1D'):      return list1D(self.config.get(self.section, key), i_type=c_type)
        elif(c_struct == 'list2D'):    return list2D(self.config.get(self.section, key), i_type=c_type)
        elif(c_struct == 'mixedList'): return mixedList(self.config.get(self.section, key), i_type=c_type)
        elif(c_struct == 'dictND'):    return dictND(self.config.get(self.section, key), i_type=c_type, k_type=k_type)
        elif(c_struct == 'json'):      return json.loads(self.config.get(self.section, key).replace("\'", "\""))

        if(c_type == 'int'):           return self.config.getint(self.section, key)
        elif(c_type == 'float'):       return self.config.getfloat(self.section, key)
        elif(c_type == 'bool'):        return self.config.getboolean(self.section, key)
        elif(c_type == 'path'):        return self.verify_path(self.config.get(self.section, key), p_type)
        else:                          return self.config.get(self.section, key)

    def to_string(self, attr, **kwargs):
        value = getattr(self, attr)


        if self.handles.set_index('attr').at[attr, 'c_struct'] == 'json':
            return f"{value}"
        elif isinstance(value, (list, tuple)):
            return split_list(value, **kwargs)
        elif isinstance(value, dict):
            return split_dict(value, **kwargs)
        else:
            if self.handles.set_index('attr').at[attr, 'c_type'] == 'path':
                return f"{path_slashes(value)}"
            return f"{value}"

    def _get_min_indent(self):
        current_min = 0
        for section in self.sections:
            for key, default in self._get_defaults(section, indent=0):
                if len(key) > current_min: current_min = len(key)
        return current_min

    def _get_defaults(self, section, indent=5):
        raw = self.handles[self.handles['section'] == section][['text', 'attr']].to_dict(orient='records')
        return [(i['text'], self.to_string(i['attr'], pad_newlines_with=' ' * indent) ) for i in raw]

    def write(self,config_name,indent='auto'):
        with open(config_name, 'w') as new_file:
            new_file.write("# Fichier de configuration pour la production de rapports d'analyse utilisant les \n"
                           "# données d'une collecte LAPI.\n"
                           "# \n"
                           "# Instructions:\n"
                           "#    - Les entêtes de sections doivent être respectées (ie: il n'est pas possible \n"
                           "#      de déplacer un élément d'une section à l'autre) \n"
                           "#    - Les éléments d'une section peuvent être omis, à l'exception de ceux avec la \n"
                           "#      mention '[required]'. Les valeurs par défaut seront \n"
                           "#      alors utilisées. \n"
                           "#    - Une section entière peut également être omise si aucun de ses éléments n'est \n"
                           "#      marqué de la mention '[required]'. \n"
                           "# \n"
                           "#    TYPES SPÉCIAUX \n"
                           "#    - Les listes s'écrivent encadrées de braquettes: '[' et ']' \n"
                           "#    - Les éléments ci-dessous constituent des listes: \n"
                           "#           + Carto - Rotation du Nord (degré) \n"
                           "#           + Carto - Distance au pourtour (m)* \n"
                           "# \n"
                           "#    - Les dictionnaires s'écrivent encadrés d'accolades: '{' et '}' \n"
                           "#    - Les éléments ci-dessous constituent des dictionnaires: \n"
                           "#           + AUCUN DICTIONNAIRE À CE JOUR \n"
                           "# \n"
                           "#    - Les éléments mixtes combinent les caractéristiques des listes et des \n"
                           "#     dictionnaires.\n"
                           "#    - Certains sont des dictionnaires contenant des listes: \n"
                           "#           + Jours et heures d'analyse \n"
                           "#    - D'autres sont des listes contenant des dictionnaires: \n"
                           "#           + Dates de collecte \n"
                           "# \n"
                           "#    - Les dictionnaires et les listes peuvent être écrits sur plusieurs lignes pour \n"
                           "#      augmenter la lisibilité du fichier, en autant que les lignes additionnelles \n"
                           "#      comportent une indentation d'au moins quelques espaces et que les éléments \n"
                           "#      de la liste soient séparés par une virgule (,), même lorsque le suivant se \n"
                           "#      situe sur une autre ligne.\n"
                           "# \n"
                           "#    NOTA BENE \n"
                           "#    - Les éléments notés par un astérisque (*) s'appliquent par secteurs. \n"
                           )
            if indent == 'auto':
                indent = self._get_min_indent()
            if not isinstance(indent, int):
                raise TypeError(f"If not 'auto', the keyword 'indent' must be of type 'int', received {indent.__class__}")

            for section in self.sections:
                new_file.write(f"[{section.upper()}]\n")
                for text, default in self._get_defaults(section, indent=indent):
                    new_file.write(f"{text.capitalize():<{indent}} = {default} \n")
                new_file.write("\n")

    def verify_path(self, raw, p_type):
        xform = path_slashes(raw)

        #verify that we have a valid scheme - works for both folder and file scheme
        #will raise an error is invalid
        pathvalidate.validate_filepath(xform , platform='auto')

        #pathvalidate does not differentiate between file and folder, let's
        #see if we got an extension
        if p_type == 'folder' and not os.path.splitext(xform)[-1] == '':
            raise ValueError('Folder path should not contain an extension')
        if p_type == 'file'and os.path.splitext(xform)[-1] == '':
            raise ValueError('File path should contain an extension')

        return xform

    def init_config(self):
        build_cache(self.work_folder)
        build_results(self.work_folder)
        build_dates(self.days_bounds)
        set_delimns(self.gis_bounds, self.gis_vis_bounds)
        set_prov_origin(self.plates_origin_gis)
        set_roads(self.roads_path, self.roads_dbl_path, self.curbsnapp_projects_id)
        set_prov_conf(self)
