
import zarr
from pathlib import Path

class BaseStorage:
    def __init__(self):
        pass
    
    def get_storage(self):
        pass
    
    def get_root_group(self):
        pass
    
    def create_dataset(self, shape, group=None, varnames=None):
        pass


class ArrayLakeStorage(BaseStorage):
    def __init__(self, client: str, repo: str, disk_store: str):
        self.client = client
        self.repo = repo
        self.disk_store = disk_store
        
    def get_storage(self):
        return self.repo.store
    
    @property
    def root_group(self):
        return self.repo.root_group
    
    def create_group(self, group: str):
        self.root_group.create_group(group)
        
    def get_group(self, group: str = None):
        return self.root_group[group]
    
    def delete_group(self, group: str):
        del self.root_group[group]
        
    def create_dataset(self, var, group=None, varnames=None):
        pass

class IceChunkLocalDatastore(BaseStorage):
    
    def __init__(self, path: str, mode: str = "w"):
        storage_config = icechunk.StorageConfig.filesystem(path)
        try:
            self.store = icechunk.IcechunkStore.create(storage_config, mode=mode)
        except ValueError:
            self.store = icechunk.IcechunkStore.open_existing(
                storage=storage_config,
                mode="r+"
            )

    def get_storage(self):
        return self.store
    
    @property
    def root_group(self):
        return zarr.group(store=self.store)
    
    def create_group(self, group: str):
        self.root_group.create_group(group)
        
    def get_group(self, group: str = None):
        return self.root_group[group]
    
    def delete_group(self, group: str):
        del self.root_group[group]
        
    def create_dataset(self, var, group=None, varnames=None):
        pass
    
    
class DummyRepo:
    def commit(self, message: str):
        pass

class PlainOlZarrStore(BaseStorage):
    def __init__(self, path: str):
        self.store = zarr.storage.DirectoryStore(Path(path) / 'data.zarr')
        self.repo = DummyRepo()
        
    def get_storage(self):
        return self.store
    
    @property
    def root_group(self):
        return zarr.group(store=self.store)
    
    def create_group(self, group: str):
        self.root_group.create_group(group)
        
    def get_group(self, group: str = None):
        return self.root_group[group]
    
    def delete_group(self, group: str):
        del self.root_group[group]
        
    def create_dataset(self, var, group=None, varnames=None):
        pass