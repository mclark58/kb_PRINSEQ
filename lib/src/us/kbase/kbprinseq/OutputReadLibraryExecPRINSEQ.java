
package us.kbase.kbprinseq;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: outputReadLibraryExecPRINSEQ</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "output_filtered_ref",
    "output_unpaired_fwd_ref",
    "output_unpaired_rev_ref",
    "report"
})
public class OutputReadLibraryExecPRINSEQ {

    @JsonProperty("output_filtered_ref")
    private String outputFilteredRef;
    @JsonProperty("output_unpaired_fwd_ref")
    private String outputUnpairedFwdRef;
    @JsonProperty("output_unpaired_rev_ref")
    private String outputUnpairedRevRef;
    @JsonProperty("report")
    private String report;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("output_filtered_ref")
    public String getOutputFilteredRef() {
        return outputFilteredRef;
    }

    @JsonProperty("output_filtered_ref")
    public void setOutputFilteredRef(String outputFilteredRef) {
        this.outputFilteredRef = outputFilteredRef;
    }

    public OutputReadLibraryExecPRINSEQ withOutputFilteredRef(String outputFilteredRef) {
        this.outputFilteredRef = outputFilteredRef;
        return this;
    }

    @JsonProperty("output_unpaired_fwd_ref")
    public String getOutputUnpairedFwdRef() {
        return outputUnpairedFwdRef;
    }

    @JsonProperty("output_unpaired_fwd_ref")
    public void setOutputUnpairedFwdRef(String outputUnpairedFwdRef) {
        this.outputUnpairedFwdRef = outputUnpairedFwdRef;
    }

    public OutputReadLibraryExecPRINSEQ withOutputUnpairedFwdRef(String outputUnpairedFwdRef) {
        this.outputUnpairedFwdRef = outputUnpairedFwdRef;
        return this;
    }

    @JsonProperty("output_unpaired_rev_ref")
    public String getOutputUnpairedRevRef() {
        return outputUnpairedRevRef;
    }

    @JsonProperty("output_unpaired_rev_ref")
    public void setOutputUnpairedRevRef(String outputUnpairedRevRef) {
        this.outputUnpairedRevRef = outputUnpairedRevRef;
    }

    public OutputReadLibraryExecPRINSEQ withOutputUnpairedRevRef(String outputUnpairedRevRef) {
        this.outputUnpairedRevRef = outputUnpairedRevRef;
        return this;
    }

    @JsonProperty("report")
    public String getReport() {
        return report;
    }

    @JsonProperty("report")
    public void setReport(String report) {
        this.report = report;
    }

    public OutputReadLibraryExecPRINSEQ withReport(String report) {
        this.report = report;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((("OutputReadLibraryExecPRINSEQ"+" [outputFilteredRef=")+ outputFilteredRef)+", outputUnpairedFwdRef=")+ outputUnpairedFwdRef)+", outputUnpairedRevRef=")+ outputUnpairedRevRef)+", report=")+ report)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
