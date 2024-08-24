
from algoliasearch_django import algolia_engine


def get_client():
    return algolia_engine.client


def get_index(index_name = 'jetkerpy_ProductInventory'):
    """
    INDEX_NAME = JETKERPY_PRODUCTINVENTORY WE HAVE THIS NAME
    IN OUR APP INTO ALGOLIA API SO WE GONNA GET DATA FROM THIS OK :)
    """
    client = get_client()
    index = client.init_index(index_name)
    return index



def perform_search(query, **kwargs):
    index = get_index()
    results = index.search(query)
    return results
