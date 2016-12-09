/*
A KBase module: kb_PRINSEQ

This module contains 1 method:

runPRINSEQ() to a backend KBase App, potentially operating on ReadSets as well - Middle man from Narrative UI to wrapper call
execPRINSEQ() to local method that handle s overloading PRINSEQ to run on to run on a set or a single library
execReadLibraryPRINSEQ() to run PRINSEQ low complexity filtering on a single Reads object (Single End or Paired end)
*/

module kb_PRINSEQ {
    /*
        Common Types
    */
    typedef string workspace_name;
    typedef string data_obj_ref;
    typedef string data_obj_name;

    /* 
        exec PRINSEQ section
    */

    /*
        execPRINSEQ and execReadLibraryPRINSEQ input

        input_reads_ref : may be KBaseFile.PairedEndLibrary or KBaseFile.SingleEndLibrary 
        output_ws : workspace to write to 
        output_reads_name : obj_name to create

        lc_method : Low complexity method - value must be "dust" or "entropy"
        lc_threshold : Low complexity threshold - Value must be an integer between 0 and 100. 
                             Note a higher lc_threshold in entropy is more stringent. 
                             Note a lower lc_threshold is less stringent with dust
    */
    typedef structure {
        data_obj_ref input_reads_ref;
        workspace_name output_ws;
        data_obj_name output_reads_name;
        string lc_method;
        int lc_threshold; 
    } inputPRINSEQ;

    typedef structure {
        data_obj_ref output_filtered_ref;
	    data_obj_ref output_unpaired_fwd_ref;
	    data_obj_ref output_unpaired_rev_ref;
	    string report;
    } outputReadLibraryExecPRINSEQ;

    funcdef execReadLibraryPRINSEQ(inputPRINSEQ input_params)
        returns (outputReadLibraryExecPRINSEQ output)
        authentication required;
};
