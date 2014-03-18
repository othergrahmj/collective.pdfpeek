# -*- coding: utf-8 -*-
from collective.pdfpeek.interfaces import IPDF
from collective.pdfpeek.interfaces import PDFPEEK_ANNOTATION_KEY
from zope.annotation.interfaces import IAnnotations
from zope.component import adapts
from zope.interface import implements
from zope.publisher.interfaces.http import IHTTPRequest
from zope.traversing.interfaces import ITraversable


class PDFPeekImageScaleTraverser(object):
    """ Used to traverse to images stored on IPDF objects

        Traversing to portal/object/++images++/++page++1 will retrieve the
        first page of the pdf, acquisition-wrapped.
    """
    implements(ITraversable)
    adapts(IPDF, IHTTPRequest)

    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def traverse(self, name, ignore):
        ann = IAnnotations(self.context).get(PDFPEEK_ANNOTATION_KEY)
        return ann['image_thumbnails'][name]
