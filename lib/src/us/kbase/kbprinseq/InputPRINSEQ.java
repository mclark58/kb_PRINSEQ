
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
 * <p>Original spec-file type: inputPRINSEQ</p>
 * <pre>
 * execPRINSEQ and execReadLibraryPRINSEQ input
 * input_reads_ref : may be KBaseFile.PairedEndLibrary or KBaseFile.SingleEndLibrary 
 * output_ws : workspace to write to 
 * output_reads_name : obj_name to create
 * lc_method : Low complexity method - value must be "dust" or "entropy"
 * lc_entropy_threshold : Low complexity threshold - Value must be an integer between 0 and 100. 
 *                        Note a higher lc_entropy_threshold in entropy is more stringent. 
 * lc_dust_threshold : Low complexity threshold - Value must be an integer between 0 and 100.                        
 *                      Note a lower lc_entropy_threshold is less stringent with dust
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "input_reads_ref",
    "output_ws",
    "output_reads_name",
    "lc_method",
    "lc_entropy_threshold",
    "lc_dust_threshold"
})
public class InputPRINSEQ {

    @JsonProperty("input_reads_ref")
    private String inputReadsRef;
    @JsonProperty("output_ws")
    private String outputWs;
    @JsonProperty("output_reads_name")
    private String outputReadsName;
    @JsonProperty("lc_method")
    private String lcMethod;
    @JsonProperty("lc_entropy_threshold")
    private Long lcEntropyThreshold;
    @JsonProperty("lc_dust_threshold")
    private Long lcDustThreshold;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("input_reads_ref")
    public String getInputReadsRef() {
        return inputReadsRef;
    }

    @JsonProperty("input_reads_ref")
    public void setInputReadsRef(String inputReadsRef) {
        this.inputReadsRef = inputReadsRef;
    }

    public InputPRINSEQ withInputReadsRef(String inputReadsRef) {
        this.inputReadsRef = inputReadsRef;
        return this;
    }

    @JsonProperty("output_ws")
    public String getOutputWs() {
        return outputWs;
    }

    @JsonProperty("output_ws")
    public void setOutputWs(String outputWs) {
        this.outputWs = outputWs;
    }

    public InputPRINSEQ withOutputWs(String outputWs) {
        this.outputWs = outputWs;
        return this;
    }

    @JsonProperty("output_reads_name")
    public String getOutputReadsName() {
        return outputReadsName;
    }

    @JsonProperty("output_reads_name")
    public void setOutputReadsName(String outputReadsName) {
        this.outputReadsName = outputReadsName;
    }

    public InputPRINSEQ withOutputReadsName(String outputReadsName) {
        this.outputReadsName = outputReadsName;
        return this;
    }

    @JsonProperty("lc_method")
    public String getLcMethod() {
        return lcMethod;
    }

    @JsonProperty("lc_method")
    public void setLcMethod(String lcMethod) {
        this.lcMethod = lcMethod;
    }

    public InputPRINSEQ withLcMethod(String lcMethod) {
        this.lcMethod = lcMethod;
        return this;
    }

    @JsonProperty("lc_entropy_threshold")
    public Long getLcEntropyThreshold() {
        return lcEntropyThreshold;
    }

    @JsonProperty("lc_entropy_threshold")
    public void setLcEntropyThreshold(Long lcEntropyThreshold) {
        this.lcEntropyThreshold = lcEntropyThreshold;
    }

    public InputPRINSEQ withLcEntropyThreshold(Long lcEntropyThreshold) {
        this.lcEntropyThreshold = lcEntropyThreshold;
        return this;
    }

    @JsonProperty("lc_dust_threshold")
    public Long getLcDustThreshold() {
        return lcDustThreshold;
    }

    @JsonProperty("lc_dust_threshold")
    public void setLcDustThreshold(Long lcDustThreshold) {
        this.lcDustThreshold = lcDustThreshold;
    }

    public InputPRINSEQ withLcDustThreshold(Long lcDustThreshold) {
        this.lcDustThreshold = lcDustThreshold;
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
        return ((((((((((((((("InputPRINSEQ"+" [inputReadsRef=")+ inputReadsRef)+", outputWs=")+ outputWs)+", outputReadsName=")+ outputReadsName)+", lcMethod=")+ lcMethod)+", lcEntropyThreshold=")+ lcEntropyThreshold)+", lcDustThreshold=")+ lcDustThreshold)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
