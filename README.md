# CAP_SingleVariant: `coloc` Automation Pipeline for Single Variant Analysis
#### Authors: Emil Cacayan, Cian Dotson, Richa Patel

### Introduction
This pipeline provides an intuitive approach to colocalization, capable of processing ARIC-formatted pQTLs, GTEx-formatted eQTLs, and GWAS summary statistics. It tests for shared genetic signals between GWAS and QTL data by identifying overlapping causal variants, helping to pinpoint or features that are not only associated with a trait but also have their expression influenced by the same variants. Building on previous work, this pipeline allows users to input a list of genes and run colocalization analysis without modifying the script for each iteration.

### Data
This pipeline is a modification of a pipeline created to generate colocalization for pQTL data in a paper published detailing a proteome association study of breast, prostate, ovarian, and endometrial cancers (Gregga et al. 2023). The GWAS data provided for testing is a truncated version of the data used in the aforementioned study. The QTL data comes from [ARIC](https://predictdb.org/categories/downloads/) for and [GTEX](https://www.gtexportal.org/home/).

**Reference:**
Gregga I, Pharoah PDP, Gayther SA, Manichaikul A, Im HK, Kar SP, Schildkraut JM, Wheeler HE. Predicted Proteome Association Studies of Breast, Prostate, Ovarian, and Endometrial Cancers Implicate Plasma Protein Regulation in Cancer Susceptibility. Cancer Epidemiol Biomarkers Prev. 2023 Sep 1;32(9):1198-1207. doi: 10.1158/1055-9965.EPI-23-0309. PMID: 37409955; PMCID: PMC10528410.

### Scripts 
* `SVA.R`: R script that performs automated colocalization analysis between GWAS data and either eQTL or pQTL datasets. It processes input files, aligns SNPs, runs the coloc method, and generates visualizations using locuscomparer.
* `wrapper.py`: Python script that acts as a wrapper to run the SVA.R script using parameters specified in a .ini config file, streamlining execution by dynamically building and executing the appropriate Rscript command based on user-defined settings.
* `config.ini`: File that is a configuration file (in .ini format) used by the Python wrapper script to provide input parameters for running the SVA.R R script. `config_eqtl.ini` and `config_pqtl.ini` are already initialized for running test data.

### Packages & Dependencies
This pipeline is designed for a Unix environment, and requires the following software to function:
* [`Linux/Unix`](https://www.linux.org/pages/download/)
  * [`libmariadbclient-dev`](https://github.com/r-dbi/RMySQL)
* [`Python3`](https://www.python.org/downloads/)
* [`R`](https://www.r-project.org/)  

The following R packages are automatically installed (if not already present) and loaded silently by the pipeline. However, if any issues arise, please use the following links to troubleshoot. 
- [`data.table`](https://cran.r-project.org/web/packages/data.table/index.html)
- [`dplyr`](https://cran.r-project.org/web/packages/dplyr/index.html)
- [`coloc`](https://chr1swallace.github.io/coloc/)
- [`hash`](https://cran.r-project.org/web/packages/hash/index.html)
- [`optparse`](https://cran.r-project.org/web/packages/optparse/index.html)
- [`R.utils`](https://cran.r-project.org/web/packages/R.utils/index.html)
- [`ggplot2`](https://cran.r-project.org/web/packages/ggplot2/index.html)
- [`httr`](https://cran.r-project.org/web/packages/httr/index.html)
- [`jsonlite`](https://cran.r-project.org/web/packages/jsonlite/index.html)
- [`RMySQL`](https://cran.r-project.org/web/packages/RMySQL/index.html)
- [`locuscomparer`](https://github.com/boxiangliu/locuscomparer)

### Input Specifications
As mentioned, this pipeline accepts ARIC-formatted pQTLs or GTEx-formatted eQTLs and GWAS summary statistics to perform colocalization. Due to the lack of a consensus in the format of GWAS, eQTL, and pQTL data, we ask that the following information be included. For ease of use, please enter it in the [`config.ini`](#the-configini-file) file:
#### The `config.ini` File
- `process`: Indicates the type of QTL data being used. Acceptable values are typically:
  - `eqtl`: expression Quantitative Trait Loci, denote in config file with "eqtl"
  - `pqtl`: protein Quantitative Trait Loci, deafult, leave blank in config file
- `genes`: A file containing gene names or identifiers to be analyzed. For specific formatting instructions, refer to the section below.
- `seqIDdir`: Directory path for the ARIC pQTLs `seqid.txt` file. Only needed if using pQTL data.
- `GWASdir`: Directory containing Genome-Wide Association Study (GWAS) summary statistics.
- `pQTLdir`: Directory containing pQTL (protein QTL) summary statistics files. Only needed if using pQTL data.
- `eQTLdir`: Directory containing eQTL (expression QTL) summary statistics files. Only needed if using eQTL data.
- `CHR_input`: The column name in the input data that specifies the chromosome (e.g., `"CHR"`).
- `BP_input`: The column name indicating the base pair position (e.g., `"POS"` or `"BP"`).
- `A1_input`: The column name for the effect allele (also called the alternative allele or minor allele).
- `A2_input`: The column name for the reference or non-effect allele.
- `BETA_input`: The column name for the effect size estimate (e.g., regression coefficient).
- `SE_input`: The column name for the standard error of the effect size estimate.
- `ID_input`: The column name containing SNP IDs or variant identifiers (e.g., `"rsid"`). Only needed if using eQTL data.
- `outputdir`: Name of directory where all output files (plots, results tables, logs) will be written. This will be generated for you.

#### Formatting genes of interest file: 
In order to select regions of interest, the pipeline requires a list of genes to generate an SNP list from for either eQTL or pQTL data. The pipeline requires the user specify a directory containing a list of such identifiers/gene symbols.
* **Using GTEx-formatted eQTLs**
	* A `.txt` file with newline-separated data. The first line is a header indicating the column content. Each subsequent line contains the gene using its Ensembl Gene ID (e.g. ENSG00000227232, ENSG00000162591, etc.).
* **Using ARIC-formatted pQTLs**
	* A `.txt` file with newline-separated data. The first line is a header indicating the column content. Each subsequent line contains the gene using its gene symbol (e.g. LAYN, PTEN, TP53I3, etc.).

### Singe Variant Colocalization Analysis Workflow 

#### Step 1: Load Required Packages
- Install and load necessary R packages for data manipulation, plotting, and colocalization analysis.
#### Step 2: Parse Input Arguments
- Accept command-line arguments or parameters for:
  - Gene list
  - GWAS and QTL summary statistic refrence files and column names
  - Output directory
#### Step 3: Prepare Output Directory
- For each target gene, create a corresponding output directory to store results.
#### Step 4: Process and Harmonize Summary Statistics
- Load GWAS and QTL data for each gene.
- Filter and harmonize variants:
  - Remove ambiguous SNPs
  - Handle strand flips
  - Match variants by chromosome and position
#### Step 5: Format Data for Colocalization
- Format both GWAS and QTL datasets according to `coloc.abf()` function requirements:
  - Use SNP-level data (e.g., effect sizes, standard errors, MAFs, etc.)
  - Ensure consistent variant identifiers
#### Step 6: Run Colocalization Analysis
- Perform single variant colocalization analysis using the `coloc` package.
- Save the results, including summary statistics and matching SNPs, as `.rds` and `.txt` files.
#### Step 7: Generate Locus Comparison Plots
- Create and save comparison plots using `locuscomparer`:
  - Visualize p-value concordance between GWAS and QTL signals at each locus
#### Step 8: Final Output
- Store all result files and plots in the gene-specific output directories.

### Output Files
* For each gene in the gene list, there will be a folder created for it in the specified output directory. Each folder will contain:
	* `gene_gwascoloc`: coloc formatted GWAS dataset  
	* `gene_qtlcoloc`: coloc formatted QTL dataset
	* `gene_matchsnps`: Lists SNPs matched between datasets (e.g., GWAS and QTL) after filtering and cleaning
	* `gene_sva_results.tsv`: Full results for coloc.abf() single variant analysis
	* `gene_sva_summary.tsv`: Summary results for coloc.abf() single variant analysis
	* `gene_gwas_locuscompare.txt`: GWAS file generated for locuscomapre using matchsnps dataset.
	* `gene_qtl_locuscompare.txt`: QTL file generated for locuscomapre using matchsnps dataset.
	* `gene_locuscompare.png`: Visualization of locus comparison results between datasets.
 * A `SVA.log` file is also generated in the working direcotry to capture all terminal output and error messages from the run.

### Command Arguments
To run the script, please clone the repository:
```
git clone https://github.com/richapatel138/CAP_SingleVariant.git
```
Move into the directory:
```
cd CAP_SingleVariant
```
To run the pipeline with other data, first ensure that all paths in the config file is accurate. The syntax to run the single variant analysis is: 
```
python3 wrapper.py --config "path_to_file.ini"
```
To run the pipeline using eQTL test data, use the following command:

```
python3 wrapper.py --config "config_eqtl.ini"
```
To run the pipeline using pQTL test data, use the following command:

```
python3 wrapper.py --config "config_pqtl.ini"
```
