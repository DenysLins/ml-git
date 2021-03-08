"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import os

from ml_git import log
from ml_git import utils
from ml_git.constants import ML_GIT_PROJECT_NAME, SPEC_EXTENSION, EntityType, STORAGE_KEY
from ml_git.utils import get_root_path, yaml_load
from ml_git.ml_git_message import output_messages

DATASETS = EntityType.DATASETS.value


class SearchSpecException(Exception):

    def __init__(self, msg):
        super().__init__(msg)


def search_spec_file(repotype, spec, root_path=None):
    if root_path is None:
        root_path = os.path.join(get_root_path(), repotype)
    spec_file = spec + SPEC_EXTENSION
    for root, dir, files in os.walk(root_path):
        if spec_file in files:
            return root, spec_file
    raise SearchSpecException(output_messages['ERROR_WRONG_NAME'])


def get_entity_dir(repotype, spec, root_path=None):
    if root_path is None:
        root_path = os.path.join(get_root_path(), repotype)
    spec_path, _ = search_spec_file(repotype, spec, root_path)
    entity_dir = os.path.relpath(spec_path, root_path)
    return entity_dir


def spec_parse(spec):
    sep = '__'
    specs = spec.split(sep)
    if len(specs) <= 1:
        raise SearchSpecException(output_messages['ERROR_TAG_INVALID_FORMAT'] % specs)
    else:
        categories_path = os.sep.join(specs[:-1])
        specname = specs[-2]
        version = specs[-1]
        return categories_path, specname, version


"""Increment the version number inside the given dataset specification file."""


def incr_version(file, repotype=DATASETS):
    spec_hash = utils.yaml_load(file)
    if is_valid_version(spec_hash, repotype):
        spec_hash[repotype]['version'] += 1
        utils.yaml_save(spec_hash, file)
        log.debug(output_messages['DEBUG_VERSION_INCREMENTED_TO'] % spec_hash[repotype]['version'], class_name=ML_GIT_PROJECT_NAME)
        return spec_hash[repotype]['version']
    else:
        log.error(output_messages['ERROR_INVALID_VERSION_INCREMENT'] % file, class_name=ML_GIT_PROJECT_NAME)
        return -1


def get_version(file, repotype=DATASETS):
    spec_hash = utils.yaml_load(file)
    if is_valid_version(spec_hash, repotype):
        return spec_hash[DATASETS]['version']
    else:
        log.error(output_messages['ERROR_INVALID_VERSION_GET'] % file, class_name=ML_GIT_PROJECT_NAME)
        return -1


"""Validate the version inside the dataset specification file hash can be located and is an int."""


def is_valid_version(the_hash, repotype=DATASETS):
    if the_hash is None or the_hash == {}:
        return False
    if repotype not in the_hash or 'version' not in the_hash[repotype]:
        return False
    if not isinstance(the_hash[repotype]['version'], int):
        return False
    if int(the_hash[repotype]['version']) < 0:
        return False
    return True


def get_spec_file_dir(entity_name, repotype=DATASETS):
    dir1 = os.path.join(repotype, entity_name)
    return dir1


def set_version_in_spec(version_number, spec_path, repotype=DATASETS):
    spec_hash = utils.yaml_load(spec_path)
    spec_hash[repotype]['version'] = version_number
    utils.yaml_save(spec_hash, spec_path)
    log.debug(output_messages['DEBUG_VERSION_CHANGED_TO'] % spec_hash[repotype]['version'], class_name=ML_GIT_PROJECT_NAME)


"""When --bumpversion is specified during 'dataset add', this increments the version number in the right place"""


def increment_version_in_spec(entity_name, repotype=DATASETS):
    # Primary location: dataset/<the_dataset>/<the_dataset>.spec
    # Location: .ml-git/dataset/index/metadata/<the_dataset>/<the_dataset>.spec is linked to the primary location
    if entity_name is None:
        log.error(output_messages['ERROR_NO_NAME_PROVIDED'] % repotype, class_name=ML_GIT_PROJECT_NAME)
        return False

    if os.path.exists(entity_name):
        increment_version = incr_version(entity_name, repotype)
        if increment_version != -1:
            return True
        else:
            log.error(output_messages['ERROR_INCREMENTING_VERSION'] % entity_name, class_name=ML_GIT_PROJECT_NAME)
            return False
    else:
        log.error(output_messages['ERROR_SPEC_FILE_NOT_FOUND'] % entity_name, class_name=ML_GIT_PROJECT_NAME)
        return False


def get_entity_tag(specpath, repotype, entity):
    entity_tag = None
    try:
        spec = yaml_load(specpath)
        entity_tag = spec[repotype][entity]['tag']
    except Exception:
        log.warn(output_messages['WARN_NOT_EXIST_FOR_RELATED_DOWNLOAD'] % entity)
    return entity_tag


def update_storage_spec(repotype, artifact_name, storage_type, bucket, entity_dir=''):
    path = None
    try:
        path = get_root_path()
    except Exception as e:
        log.error(e, CLASS_NAME=ML_GIT_PROJECT_NAME)
    spec_path = os.path.join(path, repotype, entity_dir, artifact_name, artifact_name + SPEC_EXTENSION)
    spec_hash = utils.yaml_load(spec_path)
    spec_hash[repotype]['manifest'][STORAGE_KEY] = storage_type + '://' + bucket
    utils.yaml_save(spec_hash, spec_path)
    return


def validate_bucket_name(spec, config):
    values = spec['manifest'][STORAGE_KEY].split('://')
    len_info = 2

    if len(values) != len_info:
        log.error(output_messages['ERROR_INVALID_BUCKET_NAME'], CLASS_NAME=ML_GIT_PROJECT_NAME)
        return False

    bucket_name = values[1]
    storage_type = values[0]
    storage = config[STORAGE_KEY]

    if storage_type in storage and bucket_name in storage[storage_type]:
        return True

    log.error(
        'Bucket name [%s] not found in config.\n'
        % bucket_name, CLASS_NAME=ML_GIT_PROJECT_NAME)
    return False
