# Human tyrosine kinase models

This is a supplementary dataset for:

```
Ensembler: Enabling high-throughput molecular simulations at the superfamily scale.
Daniel L. Parton, Patrick B. Grinaway, Sonya M. Hanson, Kyle A. Beauchamp, John D. Chodera
```

This dataset contains models and associated data for all 93 known human tyrosine kinase catalytic domains, generated with [Ensembler](https://github.com/choderalab/ensembler), using all 4433 protein kinase catalytic domain structures of any species as templates.

Templates were first subjected to loop remodeling, then used to generate models via comparative modeling.
Models were then refined using 100 ps implicit solvent molecular dynamics refinement.

## Manifest

* Target data:
  * `targets-IDs.txt` - newline-separated list of target IDs
  * `targets-data.csv` - detailed target info in CSV format
  * `targets-data.txt` - detailed target info in ASCII-format table
* Template data:
  * `templates-data.csv` - detailed template info in CSV format
  * `templates-data.txt` - detailed template info in ASCII-format table
* `models/`
  * `[target ID]/`
    * `topology.pdb` - PDB-format coordinate file, used to provide model topology
    * `models.xtc` - Gromacs XTC-format trajectory; each frame represents the coordinates of a model
      * Note: only models which successfully completed the implicit solvent MD stage are included in the trajectory
    * `models-data.csv` - data for each model (in same order as the trajectory file), including template ID, sequence identity relative to the target sequence, and RMSD relative to the highest sequence identity model
* `commands.sh` - script containing Ensembler commands used to generate the models provided in this dataset

## Links

* Ensembler code: https://github.com/choderalab/ensembler
* Ensembler documentation: http://ensembler.readthedocs.org/en/latest/

## Dataset construction with Ensembler

The sequence of commands used to generate this dataset can be found in the `commands.sh` script.

To install the same version of Ensembler as used to generate this dataset, the script first creates and activates a [conda environment](http://conda.pydata.org/docs/using/envs.html):
```
conda create -c https://conda.binstar.org/omnia -n ensembler1.0 python=2.7 ensembler=1.0 --yes
source activate ensembler1.0
```

### Initialize Ensembler project

First, we initalize an Ensembler project in the current working directory.
This comamnd creates a number of directories and a metadata file (meta0.yaml).

```
ensembler init
```

### Select target sequences

Next, we designate a set of protein sequences as targets (the sequences for which the user is interested in generating structural models).
Here, we extract from UniProt all human tyrosine protein kinases, and designate that we want to model the protein kinase domain.
```
ensembler gather_targets --query 'family:"tyr protein kinase family" AND organism:"homo sapiens" AND reviewed:yes' --uniprot_domain '^Protein kinase(?!; truncated)(?!; inactive)'
```
This is specified by the [regular expression](https://docs.python.org/2/library/re.html#regular-expression-syntax) ("regex") passed to the `--uniprot_domain` flag.
The initial UniProt search returns a number of domain types, including "Protein kinase", "Protein kinase; 1", "Protein kinase; 2", "Protein kinase; truncated", and "Protein kinase; inactive". The above regex selects the first three types of domain, and excludes the latter two. Sequences are written to a fasta file: ```targets/targets.fa```.

Targets are given IDs of the form ```[UniProt mnemonic]_D[domain id]```, which consists of the UniProt name for the target and an identifier for the domain (since a single target protein may contain multiple domains of interest). Example: ```ABL1_HUMAN_D0```.

### Select template structures


Ensembler uses comparative modeling to build models, and as such requires a set of structures to be used as templates.
This second stage thus entails the selection of templates and storage of associated sequences, structures, and identifiers.
```
ensembler gather_templates --gather_from uniprot --query 'domain:"Protein kinase" AND reviewed:yes' --uniprot_domain_regex '^Protein kinase(?!; truncated)(?!; inactive)'
```
The above command queries UniProt for all protein kinases (of any species), selects the relevant domains, and retrieves sequence data and a list of associated PDB structures (X-ray and NMR techniques only), which are then downloaded from the PDB. Template sequences are written in two forms - the first contains only residues resolved in the structure (```templates/templates-resolved-seq.fa```); the second contains the complete UniProt sequence containined within the span of the structure, including unresolved residues (```templates/templates-full-seq.fa```). Template structures (containing only resolved residues) are extracted and written to the directory ```templates/structures-resolved```. Templates containing the full sequences can optionally be generated with a subsequent step - the ```loopmodel``` function.

Templates are given IDs of the form ```[UniProt mnemonic]_D[domain id]_[PDB id]_[chain id]```, where the final two elements represent the PBD ID and chain identifier.
Example: ```EGFR_HUMAN_D0_2GS7_B```.

### Reconstruct missing loops from template structures

(_Optional_)
Reconstruct template loops which were not resolved in the original PDB structure, using _Rosetta loopmodel_.
```
ensembler loopmodel
```
Pre-building template loops in this way, prior to the main modeling stage (with Modeller), tends to result in higher quality models.
The reconstructed template structures are written to the directory ```templates/structures-modeled-loops```.

### Perform template-target sequence alignments

Conduct pairwise alignments of target sequences against template sequences.
```
ensembler align
```
These alignments are used to guide the subsequent modeling step, and are stored in directories of the form ```models/[target id]/[template id]/alignment.pir```.
The ```.pir``` alignment format is an ascii-based format required by ```Modeller```.

If the ```loopmodel``` function was used previously, then templates which have been successfully remodeled will be selected for this alignment and the subsequent modeling steps.
Otherwise, Ensembler defaults to using the template structures which contain only resolved residues.

### Build structural models of targets

Create models by mapping each target sequence onto each template structure, using the Modeller [automodel](https://salilab.org/modeller/manual/node15.html) function.
```
ensembler build_models
```

### Cluster structural models

Filter out non-unique models by clustering on RMSD. A default cutoff of 0.06 nm is used.
```
ensembler cluster
```
Unique models are given an empty file ```unique_by_clustering``` in their model directory.

### Refine structures in implicit solvent

Refine models by performing an energy minimization followed by a short molecular dynamics simulation (default: 100 ps) with implicit solvent (Generalized Born surface area), using ```OpenMM```. The final structure is written to the compressed PDB file ```implicit-refined.pdb.gz```.
```
ensembler refine_implicit
```

