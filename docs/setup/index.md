# Setup

Use this section when you are preparing a new project workspace, choosing how software will be installed on HPC, or trying to make sure another lab member can reproduce your environment later.

Recent crop genome workflows combine tools with very different dependency profiles: hifiasm, Merqury, YaHS/Juicebox, FCS, EDTA, BRAKER, MAKER, and sometimes Verkko or ONT-heavy assemblers. Plan environments as part of the method, not as an afterthought.

## Read This Section First If

- you are starting a new species or cultivar project
- you need to choose between modules, conda or mamba, pixi, containers, or direct installs
- you want a cleaner project directory before running large jobs
- you are trying to make sbatch templates portable across clusters

## Best Starting Pages

- [Software environments on HPC](environment.md)
- [Tool version policy](../tool_version_policy.md)
- [sbatch template index](../sbatch_template_index.md)
- [MkDocs and GitHub Pages publishing](../mkdocs_publishing.md)

## Practical Outcome

After finishing this section, you should have:

- a project directory layout
- a documented software installation strategy
- a plan for cluster-specific sbatch edits
- a record of tool versions worth keeping in methods and release notes

## Read Next

Once your environment is stable, continue to [Assembly](../assembly/index.md).
