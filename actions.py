import datetime
import persistent

class DataTask(persistent.Persistent):
    """
    Represents some manipulation with respect to some data.
    """

    def __init__(self, method, **kwargs):
        self.created = datetime.datetime.now()
        self.last_attempted = None
        self.completed = None

        self.method = method
        self.kwargs = kwargs
    
    def execute(self):
        if self.completed is not None:
            raise RuntimeError('Task already executed.')

        self.last_attempted = datetime.datetime.now()
        self.method(**self.kwargs)

        self.completed = datetime.datetime.now()
        return None

class TransformDataTask(DataTask):
    """
    Generates a new datum from an existing datum using ``method``.
    """
    def __init__(self, method, **kwargs):
        self.datum_from = kwargs.get('datum')
        super(TransformDataTask, self).__init__(self, method, **kwargs)

    def execute(self):
        result = super(TransformDataTask, self).execute()
        self.datum_to = result
        return result

class CreateDataTask(DataTask):
    """
    Creates a new datum using ``method``.
    """
    def execute(self):
        result = super(CreateDataTask, self).execute()
        self.datum = result
        return result


