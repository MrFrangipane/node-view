

class Entity(object):
    """Base class for Entities,
    Provides introspective (de)serialisation for persistance"""
    def as_document(self):
        # Prepare doc
        document = dict(self.__dict__)
        # Add Class info
        document['__class__'] = self.__class__.__name__
        # Return Document
        return document

    def from_document(self, document):
        # Exit if wrong class
        if not document['__class__'] == self.__class__.__name__:
            return

        # Each attribute
        for attribute_name in self.__dict__.keys():
            setattr(self, attribute_name, document[attribute_name])
