# CAP - `coloc` Automation Pipeline
## Authors: Emil Cacayan, Cian Dotson, Richa Patel

### Introduction
This pipeline provides an intuitive approach to colocalization, capable of processing ARIC-formatted pQTLs, GTEx-formatted eQTLs, and GWAS summary statistics. It tests for shared genetic signals between GWAS and QTL data by identifying overlapping causal variants, helping to pinpoint or features that are not only associated with a trait but also have their expression influenced by the same variants. Building on previous work, this pipeline allows users to input a list of genes and run colocalization analysis without modifying the script for each iteration.

### Data
This pipeline is a modification of a pipeline created to generate colocalization for pQTL data in a paper published detailing a proteome association study of breast, prostate, ovarian, and endometrial cancers (Gregga et al. 2023). The GWAS data provided for testing is a truncated version of the data used in the aforementioned study. The QTL data comes from [ARIC](https://predictdb.org/categories/downloads/) for and [GTEX](https://www.gtexportal.org/home/).

### CAP Workflow

#### Dependencies
This pipeline is designed for a Unix environment, and requires the following software to function:
* [Linux/Unix](https://www.linux.org/pages/download/)
  * [libmariadbclient-dev](https://github.com/r-dbi/RMySQL)
* [Python3](https://www.python.org/downloads/)
* [R](https://www.r-project.org/)  

### R Packages Used in the Pipeline

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


#### Input Specifications
As mentioned, this pipeline accepts ARIC-formatted pQTLs or GTEx-formatted eQTLs and GWAS summary statistics to perform colocalization. Due to the lack of a consensus in the format of GWAS, eQTL, and pQTL data, we ask that the following information be included. For ease of use, please enter it in the [`config.ini`](#the-configini-file) file:
##### The `config.ini` File
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

The current functionality of the pipeline runs colocalization procedures with the `coloc` package in `R`,  first being the assumption of 0 or 1 causal variant in each trait (single variant assumption). 

The linkage disequilibrium data is generated from data obtained from phase 3 of the 1000 genomes project, a project aimed to map the majority of human genetic variation. The data that is required for this pipeline is extremely large, and we highly recommend that upon downloading the user keeps the data in a safe place for reuse. This pipeline has the added capability of downloading the required data built-in. The pipeline can also accommodate already downloaded and processed data skipping corresponding steps, streamlining the process for future iterations of the pipeline's usage. 

The output of this pipeline is a directory with a text file containing the associated $p$-values for the colocalization, and visualization of different plots via `RMarkdown` utilizing `locuscompareR` and other visualization tools. This tool is primarily intended to generate raw data, and does not have robust capability to interpret results. 

In order to select regions of interest, the pipeline requires a list of genes to generate an SNP list from for either eQTL or pQTL data. The pipeline requires the user specify a directory containing a list of such identifiers/gene symbols.
* **Using GTEx-formatted eQTLs**
	* A `.txt` file with newline-separated data. The first line is a header indicating the column content. Each subsequent line contains the gene using its Ensembl Gene ID (e.g. ENSG00000227232, ENSG00000162591, etc.).
* **Using ARIC-formatted pQTLs**
	* A `.txt` file with newline-separated data. The first line is a header indicating the column content. Each subsequent line contains the gene using its gene symbol (e.g. LAYN, PTEN, TP53I3, etc.).


##### Command Arguments
To run the script, please clone the repository:
```
git clone https://github.com/richapatel138/CAP_SVA.git
```
Move into the directory:
```
cd CAP_SVA
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

1. Gregga I, Pharoah PDP, Gayther SA, Manichaikul A, Im HK, Kar SP, Schildkraut JM, Wheeler HE. Predicted Proteome Association Studies of Breast, Prostate, Ovarian, and Endometrial Cancers Implicate Plasma Protein Regulation in Cancer Susceptibility. Cancer Epidemiol Biomarkers Prev. 2023 Sep 1;32(9):1198-1207. doi: 10.1158/1055-9965.EPI-23-0309. PMID: 37409955; PMCID: PMC10528410.
