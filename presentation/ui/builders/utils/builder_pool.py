from typing import Dict, Type, TypeVar, Optional, Generic
import weakref

from presentation.ui.builders.builder_interface import Builder

T = TypeVar('T', bound=Builder)


class BuilderPool(Generic[T]):
    """
    A pool for reusing builder instances to improve performance.
    This implementation uses weak references to avoid memory leaks.
    """
    
    def __init__(self, builder_type: Type[T], max_pool_size: int = 10):
        """
        Initialize the builder pool
        
        :param builder_type: The type of builder to pool
        :param max_pool_size: Maximum number of builders to keep in the pool
        """
        self._builder_type = builder_type
        self._max_pool_size = max_pool_size
        self._pool: Dict[str, weakref.ReferenceType[T]] = {}
    
    def acquire(self, key: str = "default") -> T:
        """
        Get a builder instance from the pool or create a new one if none is available
        
        :param key: Optional key to get a specific builder instance
        :return: A builder instance
        """
        # Check if we have a builder with this key
        if key in self._pool:
            builder = self._pool[key]()
            if builder is not None:
                return builder
            
            # Reference is dead, remove it
            del self._pool[key]
        
        # Create a new builder
        builder = self._builder_type()
        return builder
    
    def release(self, builder: T, key: str = "default") -> None:
        """
        Return a builder to the pool for reuse
        
        :param builder: The builder to return to the pool
        :param key: Optional key to store the builder under
        """
        # Check if we've reached the max pool size
        if len(self._pool) >= self._max_pool_size:
            # If the key already exists, we'll replace it
            if key not in self._pool:
                # Otherwise, don't add more builders
                return
        
        # Store the builder in the pool
        self._pool[key] = weakref.ref(builder)
    
    def clear(self) -> None:
        """
        Clear all builders from the pool
        """
        self._pool.clear()


class BuilderPoolRegistry:
    """
    Registry for managing multiple builder pools
    """
    _pools: Dict[Type[Builder], BuilderPool] = {}
    
    @classmethod
    def get_pool(cls, builder_type: Type[T]) -> BuilderPool[T]:
        """
        Get or create a pool for the specified builder type
        
        :param builder_type: Type of builder to get a pool for
        :return: A builder pool for the specified type
        """
        if builder_type not in cls._pools:
            cls._pools[builder_type] = BuilderPool(builder_type)
        
        return cls._pools[builder_type]
    
    @classmethod
    def acquire_builder(cls, builder_type: Type[T], key: str = "default") -> T:
        """
        Acquire a builder from the appropriate pool
        
        :param builder_type: Type of builder to acquire
        :param key: Optional key for the builder
        :return: A builder instance
        """
        pool = cls.get_pool(builder_type)
        return pool.acquire(key)
    
    @classmethod
    def release_builder(cls, builder: T, key: str = "default") -> None:
        """
        Release a builder back to its pool
        
        :param builder: The builder to release
        :param key: Optional key to store the builder under
        """
        builder_type = type(builder)
        pool = cls.get_pool(builder_type)
        pool.release(builder, key)
    
    @classmethod
    def clear_pools(cls) -> None:
        """
        Clear all pools in the registry
        """
        for pool in cls._pools.values():
            pool.clear()
        cls._pools.clear()