class BaseHandler:
    def __init__(self, file_path, metadata):
        self.file_path = file_path
        self.metadata = metadata

    def process(self):
        raise NotImplementedError("Subclasses must implement process()")