# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests
import os
import shutil

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
# from Workspace.WorkspaceClient import Workspace
from ReadsUtils.ReadsUtilsClient import ReadsUtils
from kb_PRINSEQ.kb_PRINSEQImpl import kb_PRINSEQ
from kb_PRINSEQ.kb_PRINSEQServer import MethodContext


class kb_PRINSEQTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.token = environ.get('KB_AUTH_TOKEN', None)
        user_id = requests.post(
            'https://kbase.us/services/authorization/Sessions/Login',
            data='token={}&fields=user_id'.format(cls.token)).json()['user_id']
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': cls.token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'kb_PRINSEQ',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_PRINSEQ'):
            cls.cfg[nameval[0]] = nameval[1]
        # cls.shockURL = cls.cfg['shock-url']
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL, token=cls.token)
        cls.serviceImpl = kb_PRINSEQ(cls.cfg)
        #cls.ws = workspaceService(cls.wsURL, token=token)
        #cls.ws = Workspace(cls.cfg['workspace-url'], token=cls.token)
        # cls.hs = HandleService(url=cls.cfg['handle-service-url'],
        #                        token=cls.token)
        cls.scratch = cls.cfg['scratch']
        shutil.rmtree(cls.scratch)
        os.mkdir(cls.scratch)
        suffix = int(time.time() * 1000)
        wsName = "test_kb_PRINSEQ_" + str(suffix)
        cls.ws_info = cls.wsClient.create_workspace({'workspace': wsName})
        # cls.dfu = DataFileUtil(os.environ['SDK_CALLBACK_URL'], token=cls.token)
        cls.upload_test_reads()
        print('\n\n=============== Starting tests ==================')


    @classmethod
    def tearDownClass(cls):
        if cls.getWsName():
            cls.wsClient.delete_workspace({'workspace': cls.getWsName()})
            print('Test workspace {} was deleted'.format(str(cls.getWsName())))

    def getWsClient(self):
        return self.__class__.wsClient

    @classmethod
    def getWsName(cls):
        return cls.ws_info[1]

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    @classmethod
    def upload_test_reads(cls):
        """
        Seeding an initial SE and PE Reads objects to test filtering
        """
        header = dict()
        header["Authorization"] = "Oauth {0}".format(cls.token)
        # readsUtils_Client = ReadsUtils(url=self.callback_url, token=ctx['token'])  # SDK local
        readsUtils_Client = ReadsUtils(os.environ['SDK_CALLBACK_URL'], token=cls.token)

        fwdtf = 'small_forward.fq'
        revtf = 'small_reverse.fq'
        fwdtarget = os.path.join(cls.scratch, fwdtf)
        revtarget = os.path.join(cls.scratch, revtf)
        print "CWD: "+str(os.getcwd())
        shutil.copy('/kb/module/test/data/' + fwdtf, fwdtarget)
        shutil.copy('/kb/module/test/data/' + revtf, revtarget)

        # Upload single end reads
        cls.se_reads_reference = \
            readsUtils_Client.upload_reads({'wsname': cls.getWsName(),
                                            'name': "se_reads",
                                            'sequencing_tech': 'Illumina',
                                            'fwd_file': fwdtarget}
                                            )['obj_ref']
        # Upload paired end reads
        cls.pe_reads_reference = \
            readsUtils_Client.upload_reads({'wsname': cls.getWsName(),
                                            'name': "pe_reads",
                                            'sequencing_tech': 'Illumina',
                                            'fwd_file': fwdtarget,
                                            'rev_file': revtarget}
                                            )['obj_ref']

    @classmethod
    def getPeRef(cls):
        return cls.pe_reads_reference

    @classmethod
    def getSeRef(cls):
        print "READS REFERENCE:"+str(cls.se_reads_reference)
        return cls.se_reads_reference


    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_your_method(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        pass

    def blah_test_basic_pe_execution(self):
        input_reads_ref = "5119/7/1"
        output_ws = "jkbaumohl:1454626055010"
        output_reads_name = "T_READS_Filtered"
        lc_method = "dust"
        lc_threshold = 2

        self.getImpl().execReadLibraryPRINSEQ(self.ctx, {"input_reads_ref": input_reads_ref,
                                                 "output_ws": output_ws,
                                                 "output_reads_name": output_reads_name,
                                                 "lc_method": lc_method,
                                                 "lc_threshold": lc_threshold})

    def blah_test_basic_se_execution(self):
        input_reads_ref = "5119/8/1"
        output_ws = "jkbaumohl:1454626055010"
        output_reads_name = "SE_READS_Filtered"
        lc_method = "dust"
        lc_threshold = 2

        self.getImpl().execReadLibraryPRINSEQ(self.ctx, {"input_reads_ref": input_reads_ref,
                                                 "output_ws": output_ws,
                                                 "output_reads_name": output_reads_name,
                                                 "lc_method": lc_method,
                                                 "lc_threshold": lc_threshold})

    def test_se_dust_partial(self):
        output_reads_name = "SE_dust_partial"
        lc_method = "dust"
        lc_threshold = 2
        self.getImpl().execReadLibraryPRINSEQ(self.ctx, {"input_reads_ref": self.se_reads_reference,
                                                 "output_ws": self.getWsName(),
                                                 "output_reads_name": output_reads_name,
                                                 "lc_method": lc_method,
                                                 "lc_threshold": lc_threshold})

    




