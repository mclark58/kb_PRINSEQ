# -*- coding: utf-8 -*-
#BEGIN_HEADER
import sys
from biokbase.workspace.client import Workspace as workspaceService
#from Workspace.baseclient import ServerError as WorkspaceError
import requests
import subprocess
import os
import tempfile
import shutil
import re
import shlex

## SDK Utils
#from ReadsUtils.ReadsUtilsClient import ReadsUtilsClient  # FIX
from ReadsUtils.ReadsUtilsClient import ReadsUtils
#from SetAPI.SetAPIClient import SetAPI
from KBaseReport.KBaseReportClient import KBaseReport

requests.packages.urllib3.disable_warnings()
#END_HEADER


class kb_PRINSEQ:
    '''
    Module Name:
    kb_PRINSEQ

    Module Description:
    A KBase module: kb_PRINSEQ

This module contains 1 method:

runPRINSEQ() to a backend KBase App, potentially operating on ReadSets as well - Middle man from Narrative UI to wrapper call
execPRINSEQ() to local method that handle s overloading PRINSEQ to run on to run on a set or a single library
execReadLibraryPRINSEQ() to run PRINSEQ low complexity filtering on a single Reads object (Single End or Paired end)
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/jkbaumohl/kb_PRINSEQ.git"
    GIT_COMMIT_HASH = "a58d989342c9446628e850eab532c7967bdb2361"

    #BEGIN_CLASS_HEADER
    def _sanitize_file_name(self, file_name):
        str = file_name.split(".")
        return ('_'.join(str[0:-1]))

    def _log(self, target, message):
        if target is not None:
            target.append(message)
        print(message)
        sys.stdout.flush()

    def _setup_pe_files(self, readsLibrary, export_dir, input_params):
        # Download reads Libs to FASTQ files
        input_files_info = dict()
        input_fwd_file_path = \
            readsLibrary['files'][input_params['input_reads_ref']]['files']['fwd']
        input_files_info["fastq_filename"] = \
            self._sanitize_file_name(os.path.basename(input_fwd_file_path))
        input_files_info["fastq_file_path"] = \
            os.path.join(export_dir, input_files_info["fastq_filename"])
        shutil.move(input_fwd_file_path, input_files_info["fastq_file_path"])
        input_rev_file_path = \
            readsLibrary['files'][input_params['input_reads_ref']]['files']['rev']
        input_files_info["fastq2_filename"] = \
            self._sanitize_file_name(os.path.basename(input_rev_file_path))
        input_files_info["fastq2_file_path"] = \
            os.path.join(export_dir, input_files_info["fastq2_filename"])
        shutil.move(input_rev_file_path, input_files_info["fastq2_file_path"])
        return input_files_info
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.scratch = config['scratch']
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.ws_url = config['workspace-url']
        #END_CONSTRUCTOR
        pass

    def execReadLibraryPRINSEQ(self, ctx, input_params):
        """
        :param input_params: instance of type "inputPRINSEQ" (execPRINSEQ and
           execReadLibraryPRINSEQ input input_reads_ref : may be
           KBaseFile.PairedEndLibrary or KBaseFile.SingleEndLibrary output_ws
           : workspace to write to output_reads_name : obj_name to create
           lc_method : Low complexity method - value must be "dust" or
           "entropy" lc_threshold : Low complexity threshold - Value must be
           an integer between 0 and 100. Note a higher lc_threshold in
           entropy is more stringent. Note a lower lc_threshold is less
           stringent with dust) -> structure: parameter "input_reads_ref" of
           type "data_obj_ref", parameter "output_ws" of type
           "workspace_name" (Common Types), parameter "output_reads_name" of
           type "data_obj_name", parameter "lc_method" of String, parameter
           "lc_threshold" of Long
        :returns: instance of type "outputReadLibraryExecPRINSEQ" ->
           structure: parameter "output_filtered_ref" of type "data_obj_ref",
           parameter "output_unpaired_fwd_ref" of type "data_obj_ref",
           parameter "output_unpaired_rev_ref" of type "data_obj_ref",
           parameter "report" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN execReadLibraryPRINSEQ
        console = []
#        self.log(console, 'Running execTrimmomatic with parameters: ')
#        self.log(console, "\n"+pformat(input_params))
        report = ''
        returnVal = dict()
#        retVal['output_filtered_ref'] = None
#        retVal['output_unpaired_fwd_ref'] = None
#        retVal['output_unpaired_rev_ref'] = None

        token = ctx['token']
        wsClient = workspaceService(self.ws_url, token=token)
        env = os.environ.copy()
        env['KB_AUTH_TOKEN'] = token

        # param checks
        required_params = ['input_reads_ref',
                           'output_ws',
                           'lc_method',
                           'lc_threshold']
        # output reads_name is optional. If not set will use old_objects name
        for required_param in required_params:
            if required_param not in input_params or input_params[required_param] is None:
                raise ValueError("Must define required param: '" + required_param + "'")

        if (input_params['lc_method'] != 'dust') and (input_params['lc_method'] != 'entropy'):
            raise ValueError("lc_method (low complexity method) must be 'dust' or 'entropy', " +
                             "it is currently set to : " +
                             input_params['lc_method'])

        if (input_params['lc_threshold'] < 0.0) or (input_params['lc_threshold'] > 100.0):
            raise ValueError("lc_threshold must be between 0 and 100, " +
                             "it is currently set to : " +
                             input_params['lc_threshold'])

        reportObj = {'objects_created': [],
                     'text_message': ''}

        # load provenance
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        provenance[0]['input_ws_objects'] = [str(input_params['input_reads_ref'])]

        # GET THE READS OBJECT
        # Determine whether read library or read set is input object
        #
        try:
            # object_info tuple
            [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I,
             WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)

            input_reads_obj_info = wsClient.get_object_info_new({'objects':
                                                                 [{'ref':
                                                                   input_params['input_reads_ref']
                                                                   }]})[0]
            input_reads_obj_type = input_reads_obj_info[TYPE_I]
            # input_reads_obj_version = input_reads_obj_info[VERSION_I]
            # this is object version, not type version

        except Exception as e:
            raise ValueError('Unable to get read library object from workspace: (' +
                             str(input_params['input_reads_ref']) + ')' + str(e))

        # self.log (console, "B4 TYPE: '" +
        #           str(input_reads_obj_type) +
        #           "' VERSION: '" + str(input_reads_obj_version)+"'")
        # remove trailing version
        input_reads_obj_type = re.sub('-[0-9]+\.[0-9]+$', "", input_reads_obj_type)
        # self.log (console, "AF TYPE: '"+str(input_reads_obj_type)+"' VERSION: '" +
        # str(input_reads_obj_version)+"'")

        # maybe add below later "KBaseSets.ReadsSet",
        acceptable_types = ["KBaseFile.PairedEndLibrary",
                            "KBaseAssembly.PairedEndLibrary",
                            "KBaseAssembly.SingleEndLibrary",
                            "KBaseFile.SingleEndLibrary"]
        if input_reads_obj_type not in acceptable_types:
            raise ValueError("Input reads of type: '" + input_reads_obj_type +
                             "'.  Must be one of " + ", ".join(acceptable_types))

        if input_reads_obj_type in ["KBaseFile.PairedEndLibrary", "KBaseAssembly.PairedEndLibrary"]:
            read_type = 'PE'
        elif input_reads_obj_type in ["KBaseFile.SingleEndLibrary",
                                      "KBaseAssembly.SingleEndLibrary"]:
            read_type = 'SE'

        # Instatiate ReadsUtils
        try:
            readsUtils_Client = ReadsUtils(url=self.callback_url, token=ctx['token'])  # SDK local
            self._log(None, 'Starting Read File(s) Download')
            readsLibrary = readsUtils_Client.download_reads({'read_libraries':
                                                            [input_params['input_reads_ref']],
                                                             'interleaved': 'false'
                                                             })
            self._log(None, 'Completed Read File(s) Downloading')
        except Exception as e:
            raise ValueError(('Unable to get read library object from workspace: ({})\n')
                             .format(str(input_params['input_reads_ref']), str(e)))

        # get WS metadata to get obj_name
        ws = workspaceService(self.ws_url)
        try:
            info = ws.get_object_info_new({'objects':
                                          [{'ref': input_params['input_reads_ref']}]})[0]
        except workspaceService as wse:
            self._log(console, 'Logging workspace exception')
            self._log(str(wse))
            raise

        #determine new object base name
        new_object_name = info[1]
        if('output_reads_name' in input_params and
           input_params['output_reads_name'] != '' and
           input_params['output_reads_name'] is not None):
            new_object_name = input_params['output_reads_name']

        # MAKE A DIRECTORY TO PUT THE READ FILE(S)
        # create the output directory and move the file there
        # PUT FILES INTO THE DIRECTORY
        # Sanitize the file names
        tempdir = tempfile.mkdtemp(dir=self.scratch)
        export_dir = os.path.join(tempdir, info[1])
        os.makedirs(export_dir)

        sequencing_tech = readsLibrary['files'][input_params['input_reads_ref']]['sequencing_tech']

        if read_type == 'PE':
            # IF PAIRED END, potentially 6 files created
            # one of each for the two directions(good(paired), good_singletons, bad)
            # Take the good paired and (re)upload new reads object.
            # We throwout the bad reads

            input_files_info = self._setup_pe_files(readsLibrary, export_dir, input_params)

            # RUN PRINSEQ with user options (lc_method and lc_threshold)
            cmd = ("perl /opt/lib/prinseq-lite-0.20.4/prinseq-lite.pl -fastq {} "
                   "-fastq2 {} -out_format 3 -lc_method {} "
                   "-lc_threshold {}").format(input_files_info["fastq_file_path"],
                                              input_files_info["fastq2_file_path"],
                                              input_params['lc_method'],
                                              input_params['lc_threshold'])
            print "Command to be run : " + cmd
            args = shlex.split(cmd)
            perl_script = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = perl_script.communicate()
            found_results = False
            file_names_dict = dict()
            for element in output:
                if "Input and filter stats:" in element:
                    found_results = True
                    element_parts = element.split("Input and filter stats:")
                    # PRINSEQ OUTPUT
                    report = "Input and filter stats:{}".format(element_parts[1])
                    reportObj['text_message'] = report
                    read_files_list = os.listdir(export_dir)

                    # proc = subprocess.Popen(['ls', '-l', export_dir], stdout=subprocess.PIPE)
                    # proc_output = proc.stdout.read()
                    # print "PROC OUTPUT : " + proc_output

                    for read_filename in read_files_list:
                        file_direction = None
                        print "Read File : {}".format(read_filename)
                        # determine if forward(fastq) or reverse(fastq2) file
                        if input_files_info["fastq_filename"] in read_filename:
                            file_direction = "fwd"
                        elif input_files_info["fastq2_filename"]in read_filename:
                            file_direction = "rev"
                        if file_direction is not None:
                            # determine good singleton or good part of a pair.
                            print "TEST: {}_prinseq_good_".format(
                                input_files_info["fastq_filename"])
                            if ("{}_prinseq_good_singletons".format(
                                    input_files_info["fastq_filename"])
                                    in read_filename or
                                    "{}_prinseq_good_singletons".format(
                                        input_files_info["fastq2_filename"])
                                    in read_filename):
                                # Unpaired singletons that need to be
                                # saved as a new single end reads object
                                file_names_dict["{}_good_singletons".format(file_direction)] = \
                                    os.path.join(export_dir, read_filename)
                            elif ("{}_prinseq_good_".format(input_files_info["fastq_filename"])
                                  in read_filename or
                                  "{}_prinseq_good_".format(input_files_info["fastq2_filename"])
                                  in read_filename):
                                file_names_dict["{}_good_pair".format(file_direction)] = \
                                    os.path.join(export_dir, read_filename)
                    if (('fwd_good_pair' in file_names_dict) and
                            ('rev_good_pair' in file_names_dict)):
                        self._log(None, 'Saving new Paired End Reads')
                        returnVal['filtered_paired_end_ref'] = \
                            readsUtils_Client.upload_reads({'wsname':
                                                            str(input_params['output_ws']),
                                                            'name': new_object_name,
                                                            'sequencing_tech': sequencing_tech,
                                                            'fwd_file':
                                                                file_names_dict['fwd_good_pair'],
                                                            'rev_file':
                                                                file_names_dict['rev_good_pair']
                                                            }
                                                           )['obj_ref']
                        reportObj['objects_created'].append({'ref':
                                                             returnVal['filtered_paired_end_ref'],
                                                             'description':
                                                             'Filtered Paired End Reads',
                                                             'object_name': new_object_name})
                        print "REFERENCE : " + str(returnVal['filtered_paired_end_ref'])
                    else:
                        reportObj['text_message'] += \
                            "\n\nNo good matching pairs passed low complexity filtering.\n" + \
                            "Consider loosening the threshold value.\n"
                    if 'fwd_good_singletons' in file_names_dict:
                        self._log(None, 'Saving new Forward Unpaired Reads')
                        fwd_object_name = "{}_fwd_singletons".format(new_object_name)
                        returnVal['output_filtered_fwd_unpaired_end_ref'] = \
                            readsUtils_Client.upload_reads({'wsname':
                                                            str(input_params['output_ws']),
                                                            'name': fwd_object_name,
                                                            'sequencing_tech':
                                                            sequencing_tech,
                                                            'fwd_file':
                                                            file_names_dict['fwd_good_singletons']}
                                                           )['obj_ref']
                        reportObj['objects_created'].append(
                            {'ref': returnVal['output_filtered_fwd_unpaired_end_ref'],
                             'description': 'Filtered Forward Unpaired End Reads',
                             'object_name': fwd_object_name})
                        print "REFERENCE : " + \
                            str(returnVal['output_filtered_fwd_unpaired_end_ref'])
                    if 'rev_good_singletons' in file_names_dict:
                        self._log(None, 'Saving new Reverse Unpaired Reads')
                        rev_object_name = "{}_rev_singletons".format(new_object_name)
                        returnVal['output_filtered_rev_unpaired_end_ref'] = \
                            readsUtils_Client.upload_reads({'wsname':
                                                            str(input_params['output_ws']),
                                                            'name': rev_object_name,
                                                            'sequencing_tech':
                                                            sequencing_tech,
                                                            'fwd_file':
                                                            file_names_dict['rev_good_singletons']}
                                                           )['obj_ref']
                        reportObj['objects_created'].append(
                            {'ref': returnVal['output_filtered_rev_unpaired_end_ref'],
                             'description': 'Filtered Reverse Unpaired End Reads',
                             'object_name': rev_object_name})
                        print "REFERENCE : " + \
                            str(returnVal['output_filtered_rev_unpaired_end_ref'])
                    if len(reportObj['objects_created']) > 0:
                        reportObj['text_message'] += "\nOBJECTS CREATED :\n"
                        for obj in reportObj['objects_created']:
                            reportObj['text_message'] += "{} : {}".format(obj['object_name'],
                                                                          obj['description'])
                    else:
                        reportObj['text_message'] += \
                            "\nFiltering filtered out all reads. No objects made.\n"
            if not found_results:
                raise Exception('Unable to execute PRINSEQ, Error: {}'.format(str(output)))
            print "FILES DICT : {}".format(str(file_names_dict))
            print "REPORT OBJECT :"
            print str(reportObj)

        elif read_type == 'SE':
            # Download reads Libs to FASTQ files
            # IF SINGLE END INPUT 2 files created (good and bad)
            # Take good and (re)upload new reads object
            input_fwd_file_path = \
                readsLibrary['files'][input_params['input_reads_ref']]['files']['fwd']
            fastq_filename = self._sanitize_file_name(os.path.basename(input_fwd_file_path))
            fastq_file_path = os.path.join(export_dir, fastq_filename)
            shutil.move(input_fwd_file_path, fastq_file_path)

            # RUN PRINSEQ with user options (lc_method and lc_threshold)
            cmd = ("perl /opt/lib/prinseq-lite-0.20.4/prinseq-lite.pl -fastq {} "
                   "-out_format 3 -lc_method {} "
                   "-lc_threshold {}").format(fastq_file_path,
                                              input_params['lc_method'],
                                              input_params['lc_threshold'])
            print "Command to be run : " + cmd
            args = shlex.split(cmd)
            print "ARGS:  " + str(args)
            perl_script = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = perl_script.communicate()
            print "OUTPUT: " + str(output)
            found_results = False
            found_se_filtered_file = False
            file_names_dict = dict()
            for element in output:
                if "Input and filter stats:" in element:
                    found_results = True
                    element_parts = element.split("Input and filter stats:")
                    # PRINSEQ OUTPUT
                    report = "Input and filter stats:{}".format(element_parts[1])
                    reportObj['text_message'] = report
                    read_files_list = os.listdir(export_dir)

                    for read_filename in read_files_list:
                        print "Early Read File : {}".format(read_filename)

                    for read_filename in read_files_list:
                        print "Read File : {}".format(read_filename)
                        if ("{}_prinseq_good_".format(fastq_filename) in read_filename):
                            #Found Good file. Save the Reads objects
                            self._log(None, 'Saving Filtered Single End Reads')
                            returnVal['output_filtered_single_end_ref'] = \
                                readsUtils_Client.upload_reads({'wsname':
                                                                str(input_params['output_ws']),
                                                                'name': new_object_name,
                                                                'sequencing_tech':
                                                                sequencing_tech,
                                                                'fwd_file':
                                                                    os.path.join(export_dir,
                                                                                 read_filename)}
                                                               )['obj_ref']
                            reportObj['objects_created'].append(
                                {'ref': returnVal['output_filtered_single_end_ref'],
                                 'description': 'Filtered Single End Reads'})
                            print "REFERENCE : " + str(returnVal['output_filtered_single_end_ref'])
                            found_se_filtered_file = True
                            break
            if not found_se_filtered_file:
                reportObj['text_message'] += \
                    "\n\nNone of the reads passed low complexity filtering.\n" + \
                    "Consider loosening the threshold value.\n"
            if not found_results:
                raise Exception('Unable to execute PRINSEQ, Error: {}'.format(str(output)))
            print "FILES DICT : {}".format(str(file_names_dict))
            print "REPORT OBJECT :"
            print str(reportObj)

        # save report object
        #
        report = KBaseReport(self.callback_url, token=ctx['token'])
        #report = KBaseReport(self.callback_url, token=ctx['token'], service_ver=SERVICE_VER)
        report_info = report.create({'report': reportObj,
                                    'workspace_name': input_params['output_ws']})

        output = {'report_name': report_info['name'], 'report_ref': report_info['ref']}

        #END execReadLibraryPRINSEQ

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method execReadLibraryPRINSEQ return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
