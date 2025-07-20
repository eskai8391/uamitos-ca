class EntityNotFoundError(Exception):
    """
    Custom exception raised when an entity was not found
    """

    def __init__(self, message="The entity was not found"):
        self.message = message
        super().__init__(self.message)