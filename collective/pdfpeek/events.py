# -*- coding: utf-8 -*-
from collective.pdfpeek.async import get_queue, Job
from collective.pdfpeek.conversion import remove_image_previews
from collective.pdfpeek.interfaces import IImageFromPDFConverter
from collective.pdfpeek.interfaces import ALLOWED_CONVERSION_TYPES
from collective.pdfpeek.interfaces import IPDF
from collective.pdfpeek.interfaces import IPDFPeekConfiguration
from collective.pdfpeek.transforms import convertPDFToImage
from plone.registry.interfaces import IRegistry
from plone.rfc822.interfaces import IPrimaryFieldInfo
from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from zope.component import getUtility
from zope.component.hooks import getSite

import logging

logger = logging.getLogger('collective.pdfpeek.browser.utils')


def convert_pdf(content):
    return IImageFromPDFConverter(content)()


def queue_document_conversion(content, event):
    """
    This method queues the document for conversion.
    One job is queued for the jodconverter if required, and for pdfpeek.
    """
    portal = getSite()
    if 'collective.pdfpeek' in portal.portal_quickinstaller.objectIds():

        # Use IPrimaryFieldInfo adapter to retrieve field value
        try:
            info = IPrimaryFieldInfo(content)
            content_type = info.value.contentType

            assert content_type in ALLOWED_CONVERSION_TYPES

        except (TypeError, AssertionError):
            queue_image_removal(content)
            return

        # get the queue
        conversion_queue = get_queue(
            'collective.pdfpeek.conversion_' + portal.id)

        # create a converter job
        converter_job = Job(convert_pdf, content)
        # add it to the queue
        conversion_queue.pending.append(converter_job)
        logger.info("Document Conversion Job Queued")


def queue_image_removal(content):
    """
    Queues the image removal if there is no longer a pdf
    file stored on the object
    """
    portal = getSite()
    conversion_queue = get_queue('collective.pdfpeek.conversion_' + portal.id)
    removal_job = Job(remove_image_previews, content)
    conversion_queue.pending.append(removal_job)
    logger.info("Document Preview Image Removal Job Queued")
