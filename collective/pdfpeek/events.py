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


def pdf_changed(content, event):
    """
    This event handler is fired when ATFile objects are initialized or edited
    and calls the appropriate functions to convert the pdf to png thumbnails
    and store the list of thumbnails annotated on the file object.
    """
    portal = getSite()
    if 'collective.pdfpeek' in portal.portal_quickinstaller.objectIds():
        registry = getUtility(IRegistry)
        config = registry.forInterface(IPDFPeekConfiguration)
        if config.eventhandler_toggle is True:
            if content.getContentType() == 'application/pdf':
                """Mark the object with the IPDF marker interface."""
                alsoProvides(content, IPDF)
                pdf_file_data_string = content.getFile().data
                image_converter = convertPDFToImage()
                images = image_converter.generate_thumbnails(
                    pdf_file_data_string)
                alsoProvides(content, IAttributeAnnotatable)
                annotations = IAnnotations(content)
                annotations['pdfpeek'] = {}
                annotations['pdfpeek']['image_thumbnails'] = images
                content.reindexObject()
            else:
                noLongerProvides(content, IPDF)
                IAnnotations(content)
                annotations = IAnnotations(content)
                if 'pdfpeek' in annotations:
                    del annotations['pdfpeek']
                content.reindexObject()
        return None


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
        converter_job = Job(IImageFromPDFConverter, content)
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
