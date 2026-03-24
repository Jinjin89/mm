# Figure source + reproduction guide (TB chemokine panel)

This guide maps the uploaded figure to its data sources and provides a reproducible workflow.

## Figure match
The image matches **Figure 4** ("Myeloid–T cell chemokine interactions dominate lungs of C57BL/6 mice...") from:

- Branchett *et al.* (2025), *Journal of Experimental Medicine*.
- Article page: https://rupress.org/jem/article/222/12/e20250466/278334/Type-I-IFN-drives-neutrophil-swarming-impeding

## Primary data sources
### 1) Bulk RNA-seq (panel c)
- GEO series: **GSE298786**
- Lung normalized expression table used for panel-c-like plot:
  - `GSE298786_202501_lung_norm_expr.csv.gz`
- GEO record: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE298786

### 2) scRNA-seq (panels a, b, d)
- GEO series: **GSE298787**
- Files:
  - `GSE298787_cellranger_outs.tar.gz`
  - `GSE298787_sc_integrated.rdata.gz`
- GEO record: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE298787

### 3) Analysis code
- GitHub repository from paper Data Availability section:
  - https://github.com/willjbranchett/branchett_et_al_tb

## Minimal reproduction commands (run in an internet-enabled environment)

```bash
# 0) clone analysis repo
git clone https://github.com/willjbranchett/branchett_et_al_tb.git
cd branchett_et_al_tb

# 1) download bulk lung table (panel c source)
curl -L -o GSE298786_202501_lung_norm_expr.csv.gz \
  'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE298nnn/GSE298786/suppl/GSE298786_202501_lung_norm_expr.csv.gz'

# 2) optional: scRNA objects (for CellChat/dot/chord plots in panels a,b,d)
curl -L -o GSE298787_sc_integrated.rdata.gz \
  'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE298nnn/GSE298787/suppl/GSE298787_sc_integrated.rdata.gz'

# 3) follow repository scripts to rerun CellChat and plotting workflows
#    (see repo README / scripts for figure-specific targets)
```

## Environment note
This workspace blocks outbound package/data downloads from shell (proxy 403), so raw data retrieval and full rerun are documented but cannot be executed end-to-end here.
