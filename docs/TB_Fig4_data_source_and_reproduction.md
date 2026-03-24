# 该图（TB 早期免疫细胞通讯）数据源与复现说明

你给的图对应论文 **Figure 4**（含 a/b/c/d 四个子图）：

> **Type I IFN drives neutrophil swarming, impeding lung T cell–macrophage interactions and TB control**
> (J Exp Med, 2025; PMCID: PMC12456410)

## 1) 数据源（官方）

论文在 “Data availability” 中给出：

- **Bulk RNA-seq（用于图 4c）**：GEO **GSE298786**  
  https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE298786
- **scRNA-seq（用于图 4a/4b/4d）**：GEO **GSE298787**  
  https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE298787
- **作者分析代码（从 raw data 到 final figures）**：  
  https://github.com/ogarralab/workflowr  
  Zenodo release: https://doi.org/10.5281/zenodo.16894788

GSE298786 页面提供了可下载文件（示例）：

- `GSE298786_bulkRNA_rawcounts.csv.gz`
- `GSE298786_bulkRNA_normalized.csv.gz`
- `GSE298786_bulkRNA_metadata.csv.gz`

GSE298787 页面提供了可下载文件（示例）：

- `GSE298787_scRNA_rawcounts.h5ad.gz`
- `GSE298787_scRNA_metadata.csv.gz`
- `GSE298787_scRNA_integrated_harmony.rds.gz`

## 2) 一键下载（命令行）

> 下面用的是 NCBI GEO 的 `download/?acc=...` 接口，文件名与 GEO 页面一致。

```bash
mkdir -p data/tb_fig4 && cd data/tb_fig4

# Bulk RNA-seq (GSE298786)
curl -L -o GSE298786_bulkRNA_rawcounts.csv.gz \
  "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE298786&format=file&file=GSE298786_bulkRNA_rawcounts.csv.gz"

curl -L -o GSE298786_bulkRNA_normalized.csv.gz \
  "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE298786&format=file&file=GSE298786_bulkRNA_normalized.csv.gz"

curl -L -o GSE298786_bulkRNA_metadata.csv.gz \
  "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE298786&format=file&file=GSE298786_bulkRNA_metadata.csv.gz"

# scRNA-seq (GSE298787)
curl -L -o GSE298787_scRNA_rawcounts.h5ad.gz \
  "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE298787&format=file&file=GSE298787_scRNA_rawcounts.h5ad.gz"

curl -L -o GSE298787_scRNA_metadata.csv.gz \
  "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE298787&format=file&file=GSE298787_scRNA_metadata.csv.gz"

curl -L -o GSE298787_scRNA_integrated_harmony.rds.gz \
  "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE298787&format=file&file=GSE298787_scRNA_integrated_harmony.rds.gz"
```

## 3) 最稳妥复现路径（推荐）

由于图 4a/4b 是 **CellChat 推断图**，对参数、对象结构和分组方式敏感，最可靠办法是直接运行作者代码：

1. 下载 Zenodo 的代码快照（与论文版本一致）。
2. 放入上面下载的数据文件（按作者项目约定目录）。
3. 执行作者提供的 Figure 4 对应脚本/工作流。

这样可以复现：

- 4a：细胞通讯圈图（CellChat）
- 4b：配体-受体贡献柱状图
- 4c：Cxcl9/Cxcl10/Cxcl16/Cxcl2 的 bulk RNA 表达
- 4d：myeloid 亚群 dot plot

## 4) 你这张图对应的关键信息（便于核对）

- 分组：`C57BL/6` 与 `C3HeB/FeJ`
- 时间：`Uninfected`, `Day 14`, `Day 20`
- 关键轴：`CXCL9-CXCR3`, `CXCL10-CXCR3`, `CXCL16-CXCR6`, `CXCL2-CXCR2`

## 5) 说明

当前仓库环境常见限制是对外网下载受限；若你在本地或可联网服务器执行上面命令，可以拿到原始/处理后数据并按作者流程完整复现。
