# -*- coding: utf-8 -*-
from collective.pdfpeek.events import handle_pdf
from collective.zamqp.interfaces import IMessageArrivedEvent
from collective.zamqp.producer import Consumer
from collective.zamqp.producer import Producer
from five import grok
from plone.app.uuid.utils import uuidToObject
from zope.interface import Interface

QUEUE_NAME = "collective.pdfpeek"


class IPDFProcessingMessage(Interface):
    """Marker interface for pdf processing  message"""


class PDFProcessingProducer(Producer):
    """Produces PDF processing tasks"""
    grok.name(QUEUE_NAME)

    connection_id = "conn_pdfpeek"
    serializer = "msgpack"
    queue = QUEUE_NAME
    routing_key = QUEUE_NAME

    durable = True
    auto_delete = True


class PDFProcessingConsumer(Consumer):
    """Consumes PDF processing tasks"""
    grok.name(QUEUE_NAME)  # is also the queue name

    connection_id = "conn_query"
    marker = IPDFProcessingMessage
    queue = QUEUE_NAME
    routing_key = QUEUE_NAME

    durable = True
    auto_delete = True


@grok.subscribe(IPDFProcessingMessage, IMessageArrivedEvent)
def process_message(message, event):
    """Handle messages received through consumer."""
    uuid = message.header_frame.correlation_id
    context = uuidToObject(uuid)
    handle_pdf(context)
    message.ack()
