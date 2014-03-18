# -*- coding: utf-8 -*-
from zope.i18nmessageid import MessageFactory

import pkg_resources

PDFPeekMessageFactory = MessageFactory('collective.pdfpeek')

try:
    pkg_resources.get_distribution('plone.namedfile')
except pkg_resources.DistributionNotFound:
    HAS_BLOBIMAGE = False
else:
    HAS_BLOBIMAGE = True


def initialize(context):
    """Intializer called when used as a Zope 2 product."""
