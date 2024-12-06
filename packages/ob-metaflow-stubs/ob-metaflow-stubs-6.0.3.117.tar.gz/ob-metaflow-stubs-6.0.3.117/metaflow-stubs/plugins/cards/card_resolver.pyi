##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.27.1+obcheckpoint(0.1.2);ob(v1)                               #
# Generated on 2024-11-13T19:05:29.395638                                        #
##################################################################################

from __future__ import annotations


class CardDatastore(object, metaclass=type):
    @classmethod
    def get_storage_root(cls, storage_type):
        ...
    def __init__(self, flow_datastore, pathspec = None):
        ...
    @classmethod
    def get_card_location(cls, base_path, card_name, uuid, card_id = None, suffix = "html"):
        ...
    @staticmethod
    def info_from_path(path, suffix = "html"):
        """
        Args:
            path (str): The path to the card
        
        Raises:
            Exception: When the card_path is invalid
        
        Returns:
            CardInfo
        """
        ...
    def save_data(self, uuid, card_type, json_data, card_id = None):
        ...
    def save_card(self, uuid, card_type, card_html, card_id = None, overwrite = True):
        ...
    def create_full_path(self, card_path):
        ...
    def get_card_names(self, card_paths):
        ...
    def get_card_html(self, path):
        ...
    def get_card_data(self, path):
        ...
    def cache_locally(self, path, save_path = None):
        """
        Saves the data present in the `path` the `metaflow_card_cache` directory or to the `save_path`.
        """
        ...
    def extract_data_paths(self, card_type = None, card_hash = None, card_id = None):
        ...
    def extract_card_paths(self, card_type = None, card_hash = None, card_id = None):
        ...
    ...

def resumed_info(task):
    ...

def resolve_paths_from_task(flow_datastore, pathspec = None, type = None, hash = None, card_id = None):
    ...

