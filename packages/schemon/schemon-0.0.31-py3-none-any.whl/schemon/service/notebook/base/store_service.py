from typing import List
from schemon.domain.contract.contract import Contract
from schemon.notebook.base.store import Store


def get_store(stores: List[Store], contract: Contract):
    """Retrieve the Store object from the stores list based on the contract."""
    for store in stores:
        if store.contract == contract:
            return store
    raise ValueError(f"No store found for contract {contract.entity.name}")

def append_or_update_store(stores: List[Store], store):
    """
    Append a new store to the self.stores list, or update the df of an existing store
    with the same contract.
    """
    # Check if a store with the same contract already exists
    for existing_store in stores:
        if existing_store.contract == store.contract:
            # Update the df for the existing store
            existing_store.df = store.df
            return  # Exit the method after updating

    # If no matching contract was found, append the new store
    stores.append(store)