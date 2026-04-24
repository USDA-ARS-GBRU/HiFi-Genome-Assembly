# Software Environments on HPC

No single installation method works everywhere. This protocol supports four common styles:

- HPC modules
- conda or mamba
- pixi
- direct install or containers

See `docs/tool_version_policy.md` for minimum version and command-capture expectations for review-quality releases.

The point of this page is not to declare a single correct environment strategy for every cluster. The point is to choose the simplest option that your lab can reproduce a few months later without guesswork.

## Pick The Simplest Reproducible Option

Recommended decision logic:

- use **modules** when your cluster maintains current, tested versions
- use **mamba** when you need a flexible bioinformatics environment
- use **pixi** when you want a project-local lockable environment
- use **containers** when tool dependencies are difficult or cluster-specific

For annotation work, a separate environment is often the best choice because repeat and gene annotation tools can be dependency-heavy and conflict with assembly tooling.

If you are just starting a project, pair this page with `docs/project_starter_kit.md` so the environment decision and project layout get written down together.

## Option A: HPC Modules

Use modules when your cluster already maintains current versions.

Check availability:

```bash
module avail hifiasm
module avail seqkit
module avail mummer
module avail busco
module avail samtools
module avail minimap2
```

Load versions explicitly and record them in the job log:

```bash
module load hifiasm/0.25.0
module load seqkit/2.4.0
module load mummer/4.0.0rc1
module load gnuplot/5.4.8

hifiasm --version
seqkit version
nucmer --version
```

## Option B: Conda or Mamba

Use `mamba` when possible because it usually resolves complex bioinformatics environments faster than plain `conda`.

Example assembly environment:

```bash
mamba create -n hifi-assembly -c conda-forge -c bioconda \
  hifiasm \
  seqkit \
  samtools \
  minimap2 \
  mummer4 \
  gnuplot \
  fastqc \
  fastp \
  filtlong \
  jellyfish \
  genomescope2 \
  busco \
  quast \
  merqury \
  purge_dups \
  ragtag \
  yahs \
  bwa \
  bedtools \
  blast \
  sourmash \
  python=3.11
```

Example annotation environment:

```bash
mamba create -n plant-annotation -c conda-forge -c bioconda \
  edta \
  repeatmodeler \
  repeatmasker \
  braker3 \
  maker \
  augustus \
  genemark-et \
  liftoff \
  gffread \
  agat \
  busco \
  miniprot \
  diamond \
  trnascan-se \
  barrnap
```

## Option C: Pixi

Pixi is useful when you want a project-local, lockable environment.

```bash
pixi init
pixi add -c conda-forge -c bioconda hifiasm seqkit samtools minimap2 mummer4 gnuplot busco quast
pixi run hifiasm --version
```

## Option D: Direct Install or Containers

Some tools are often easiest as binaries or containers:

- `hifiasm` can be compiled directly from GitHub
- NCBI FCS often runs best through Singularity/Apptainer or Docker
- `EDTA`, `BRAKER3`, and `MAKER` may be more stable in containers on some systems

Always record:

- the exact command used
- the tool version
- the container tag or digest, if available

## Practical Recommendation

For many crop genome projects on HPC:

- keep one environment for assembly and core QC
- keep a separate environment for repeat and gene annotation
- keep containerized fallbacks for the most fragile tools

That split usually reduces dependency conflicts and makes reruns less painful.

## Before You Move On

Before leaving setup, make sure you can point to:

- the exact environment method you chose
- the place where version output will be captured
- the project-local `01_sbatch/` directory you will actually edit
- the decision log where cluster-specific deviations will be recorded

## Related Files

- `docs/setup/index.md`
- `docs/project_starter_kit.md`
- `docs/tool_version_policy.md`
- `docs/assembly/index.md`
- `01_sbatch_templates/`
