# -*- coding: utf-8 -*-
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.testing import Layer
from plone.testing import z2

import doctest
import fnmatch
import os

SAMPLE_DATA_DIRECTORY = \
    os.path.join(os.path.dirname(__file__), 'tests', 'data')


class SampleDataLayer(Layer):

    def setUp(self):
        self['pdf_files'] = []
        for f in os.listdir(SAMPLE_DATA_DIRECTORY):
            if fnmatch.fnmatch(f, '*.pdf'):
                self['pdf_files'].append(
                    os.path.join(SAMPLE_DATA_DIRECTORY, f))

PDFPEEK_SAMPLEDATA_FIXTURE = SampleDataLayer()


class PDFPeekATLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import collective.pdfpeek
        self.loadZCML(package=collective.pdfpeek)
        
        z2.installProduct(app, 'Products.Archetypes')
        z2.installProduct(app, 'Products.ATContentTypes')
        z2.installProduct(app, 'plone.app.blob')

        import Products.ATContentTypes
        self.loadZCML(package=Products.ATContentTypes)

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'Products.Archetypes')
        z2.uninstallProduct(app, 'Products.ATContentTypes')
        z2.uninstallProduct(app, 'plone.app.blob')

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.pdfpeek:default')

        # install Products.ATContentTypes manually if profile is available
        # (this is only needed for Plone >= 5)
        profiles = [x['id'] for x in portal.portal_setup.listProfileInfo()]
        if 'Products.ATContentTypes:default' in profiles:
            applyProfile(portal, 'Products.ATContentTypes:default')

PDFPEEK_AT_FIXTURE = PDFPeekATLayer()


class PDFPeekDXLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import plone.app.contenttypes
        self.loadZCML(package=plone.app.contenttypes)

        import collective.pdfpeek
        self.loadZCML(package=collective.pdfpeek)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.contenttypes:default')
        self.applyProfile(portal, 'collective.pdfpeek:default')
        self.applyProfile(portal, 'collective.pdfpeek.dx:dx')

PDFPEEK_DX_FIXTURE = PDFPeekDXLayer()

# ATContentTypes
PDFPEEK_AT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(
        PDFPEEK_SAMPLEDATA_FIXTURE,
        PDFPEEK_AT_FIXTURE,
    ),
    name='PDFPeek:AT:Integration'
)
PDFPEEK_AT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(
        PDFPEEK_SAMPLEDATA_FIXTURE,
        PDFPEEK_AT_FIXTURE,
    ),
    name='PDFPeek:AT:Functional'
)

# Dexterity
# PDFPEEK_DX_INTEGRATION_TESTING = IntegrationTesting(
#    bases=(
#        PDFPEEK_SAMPLEDATA_FIXTURE,
#        PDFPEEK_DX_FIXTURE,
#    ),
#    name='PDFPeek:DX:Integration'
# )
# PDFPEEK_DX_FUNCTIONAL_TESTING = FunctionalTesting(
#     bases=(
#         PDFPEEK_SAMPLEDATA_FIXTURE,
#         PDFPEEK_DX_FIXTURE,
#     ),
#     name='PDFPeek:DX:Functional'
# )

optionflags = (
    doctest.REPORT_ONLY_FIRST_FAILURE |
    doctest.NORMALIZE_WHITESPACE |
    doctest.ELLIPSIS
)
