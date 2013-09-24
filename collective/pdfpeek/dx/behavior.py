from plone.directives import form
from zope.interface import Interface


class IPrimaryFieldPDFThumbnailsAndMetadata(form.Schema):
    """Marker interface for extractable primary field"""


class IPDFDataExtractionEnabled(Interface):
    """ """
