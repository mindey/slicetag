import os
import shutil

import sharing_options
from slicer import Slicer

def get_identities(names=['FriendX','ME'], provider='Name'):
    """
    Passing the provider='Name', returns the actual sharing_options.INDIVIDUALS dictionary keys.
    ** Maybe later we should rename all the 'Name' references to 'Key', as conceptually it is INDIVIDUALS['Key']

    This function assumes a file, like the one below, with all-uppercase
    (e.g., 'ME') indicates an organization, and if with at least one
    lowercase indicating individual names.

    ```
    PROVIDERS = {
        'Gmail' : 'Gmail email address, with associated OAuth services identification',
        'Wechat': 'Tencent Wechat, with associated OAuth services identification',
        'GPG': 'GPG public key id',
        'Disk': 'Location to share to on the disk',
    }
    INDIVIDUALS = {
        'Public': {'Disk': ['/my/public/folder/'],
        },
        'FriendX': {'Gmail': ['friendx@gmail.com', 'friendxmail2@gmail.com'],
                    'Disk': ['/my/Dropbox/folder/for/friendx'],
        },
        'FriendY': {'Wechat': ['friendy'],
                    'Disk': ['/my/Dropbox/folder/for/friendy'],
        },
    }
    ORGANIZATIONS = {
        'ALL': ['Public'],
        'ME': ['FriendX'],
        'WE': ['FriendX', 'Mindey'],
        'FRIENDS': ['Mindey',
                    'FriendX',
                    'FriendY'],
    }
    ```
    """

    def get_individuals_identities(individual_names=[]):
        identities = []
        for name in individual_names:
            if name in sharing_options.INDIVIDUALS.keys():
                if provider in sharing_options.INDIVIDUALS[name].keys() or provider == 'Name':
                    if provider == 'Name':
                        identities += [name]
                    else:
                        identities += sharing_options.INDIVIDUALS[name][provider]
        return identities

    identities = []
    for name in names:
        if name.isupper():
            if name in sharing_options.ORGANIZATIONS.keys():
                identities += get_individuals_identities(sharing_options.ORGANIZATIONS[name])
        else:
            identities += get_individuals_identities([name])

    return(set(identities))

def get_individual_by_provider(search='FriendX', provider='Name'):
    """
       Returns a sub-dictionary result from sharing_options.INDIVIDUALS as a tuple:
           (DICT_access_key, { DICT }),
       where DICT is a value of sharing_options.INDIVIDUALS.

       For example, this can be used to query:

       >>> import sharing_options
       >>> get_individual_by_provider('friendx@gmail.com', provider='Gmail')

       >>> utils.get_individual_by_provider('friendy','Wechat')
       ('FriendY', {'Wechat': ['friendy'], 'Disk': ['/run/media/mindey/ndisk/Data/vimwiki/w/friendy']})

    """
    if provider=='Name':
        if search in sharing_options.INDIVIDUALS.keys():
            return (search, sharing_options.INDIVIDUALS[search])
    for key, value in enumerate(sharing_options.INDIVIDUALS):
        if provider in sharing_options.INDIVIDUALS[value].keys():
            if search in sharing_options.INDIVIDUALS[value][provider]:
                return (value, sharing_options.INDIVIDUALS[value])

def split_file(filepath):
    """
    Takes one file,
        splits it into cuts,
            and joins to create multiple files for different sharing_options.INDIVIDUALS.

    Returns:
        A dictionary, of {'name1': ['content bit11', 'content bit12',...],
                          'name2': ['content bit21', 'content bit22',...]}

    In this case, the ('conditions', 'content') -- the 'conditions' = 'sharewith',
    containing comma-separated 'Individual1,ORGANIZATION1,...'.
    """
    slicer = Slicer()
    slicer.content = open(filepath).read()
    slicer.get_cuts()
    slicer.parse_cuts()

    # Each key here to store the cuts shared with specific individual.
    results = {}

    for ix, item in enumerate(slicer.tree):

        # Assume that conditions in tuples represent names:
        # (organizations, individuals) for whom to share it.

        sharewith, content = item

        # Only consider content of the cuts with (conditions|.
        if sharewith:
            names = sharewith.split(',')
            for name in get_identities(names, provider='Name'):
                # Assume that 'Public' identity is also shared with everyone else.
                if name == 'Public':
                    for individual in sharing_options.INDIVIDUALS:
                        if individual not in results.keys():
                            results[individual] = [content]
                        else:
                            results[individual] += [content]
                else:
                    if name not in results.keys():
                        results[name] = [content]
                    else:
                        results[name] += [content]
    return results


def write_file(content, destination):

    if not os.path.exists(os.path.dirname(destination)):
        try:
            os.makedirs(os.path.dirname(destination))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(destination, "w") as f:
        f.write(content)

def clean_destination():

    if os.path.exists(sharing_options.SHARES_ROOT):
        shutil.rmtree(sharing_options.SHARES_ROOT)


def origin_to_shares():

    """
    Take the original files from sharing_options.ORIGIN_ROOT, and for each file use
    split_file() to generate files sharing_options.SHARE_ROOT/name
    for every sharing_options.INDIVIDUALS 'name' as sub-directory.
    """

    clean_destination()

    def process_file(filepath):

        results = split_file(filepath)

        for key, name in enumerate(results):
            destination = filepath.replace(sharing_options.ORIGIN_ROOT,
                os.path.join(sharing_options.SHARES_ROOT, name.lower()+'/')
            )
            print(destination)
            joined_cuts = ''.join(results[name])

            write_file(joined_cuts, destination)

    for path, dirs, files in os.walk(sharing_options.ORIGIN_ROOT):
        for file in files:
            if file[-4:] == 'wiki':
            #   print(os.path.join(path,file))
                process_file(os.path.join(path,file))
