# Tool Version Policy

Genome assemblies are only reproducible when software versions, databases, parameters, and command context are preserved. This project treats version capture as part of the analysis, not as an administrative afterthought.

## Minimum Requirements

For every assembly release candidate, record:

- Repository commit for this workflow.
- HPC cluster name and operating environment.
- Job scheduler and relevant module collection.
- Tool name and version for every major step.
- Container image name and digest, when containers are used.
- Conda, mamba, or pixi environment file, when environments are used.
- Database names, versions, and download dates.
- Exact command lines for assembly, scaffolding, QC, contamination, repeat annotation, gene annotation, and submission validation.

## Recommended Files

Store version information in:

```text
00_metadata/tool_versions.tsv
00_metadata/commands.sh
00_metadata/environment.yml
00_metadata/pixi.lock
00_metadata/container_images.tsv
00_metadata/database_versions.tsv
```

## `tool_versions.tsv` Format

```text
step	tool	version	source	notes
assembly	hifiasm	0.25.0	module hifiasm/0.25.0	
qc	BUSCO	6.0.0	conda env busco	embryophyta_odb12 downloaded 2026-04-21
```

## Version Capture Snippets

```bash
{
  date
  hostname
  git rev-parse HEAD
  module list 2>&1 || true
  hifiasm --version || true
  seqkit version || true
  busco --version || true
  nucmer --version || true
  minimap2 --version || true
  samtools --version || true
} > 00_metadata/tool_version_snapshot.txt
```

For conda or mamba:

```bash
conda env export --no-builds > 00_metadata/environment.yml
conda list > 00_metadata/conda_list.tsv
```

For pixi:

```bash
pixi info > 00_metadata/pixi_info.txt
pixi list > 00_metadata/pixi_list.txt
```

For containers:

```bash
apptainer inspect container.sif > 00_metadata/container.inspect.txt
```

## Database Versioning

Record the database version or download date for:

- BUSCO lineage datasets.
- NCBI FCS databases.
- sourmash databases.
- Kraken2/Centrifuge databases.
- RepeatMasker/Dfam/Repbase libraries.
- Protein evidence sets.
- Reference genome accessions.
- Organellar references.

## Release Rule

Do not tag a public release until the final assembly can be traced to:

1. Input data accessions or file checksums.
2. Workflow commit.
3. Tool/database versions.
4. Exact commands or sbatch scripts.
5. Assembly decision log.

