from flatten_json import flatten, unflatten_list

from griff.services.abstract_service import AbstractService


class DictService(AbstractService):
    @staticmethod
    def flat(data: dict) -> dict:
        """
        flatten a dict
        Args:
            data(dict): dict to flatten

        Returns:
            dict: flatten dict
        """
        return flatten(data, separator=".")

    @staticmethod
    def unflat(data: dict) -> dict:
        """
        unflatten a dict
        Args:
            data(dict): dict to unflat

        Returns:
            dict: unflatten dict
        """
        return unflatten_list(data, separator=".")

    @staticmethod
    def keep_keys(d: dict, keys: list):
        """
        Remove key not in keys from dictionary

        Args:
            d(dict): dictionary to clean
            keys(list): dictionary keys to keep

        Returns:
            dict: cleaned dictionary
        """
        return {k: v for k, v in d.items() if k in keys}

    @staticmethod
    def remove_keys(d: dict, keys: list):
        """
        Remove key in keys from dictionary

        Args:
            d(dict): dictionary to clean
            keys(list): dictionary keys to remove

        Returns:
            dict: cleaned dictionary
        """
        return {k: v for k, v in d.items() if k not in keys}

    @staticmethod
    def remap_keys(d: dict, remap_keys: dict) -> dict:
        """
        remap a dictionnary keys and keep only key found in remap_keys
        """
        remaped = {}
        for old, new in remap_keys.items():
            remaped[new] = d[old]
        return remaped
