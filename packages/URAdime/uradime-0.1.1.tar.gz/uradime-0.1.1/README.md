# URAdime

URAdime (Universal Read Analysis of DIMErs) is a Python package for analyzing primers in BAM files. It provides tools for identifying and analyzing primer sequences in DNA sequencing data.

## Installation

```bash
pip install uradime
```

## Usage

URAdime can be used both as a command-line tool and as a Python package.

### Command Line Interface

```bash
# Basic usage
uradime -b input.bam -p primers.tsv -o results/my_analysis

# Full options
uradime \
    -b input.bam \                    # Input BAM file
    -p primers.tsv \                  # Primer file (tab-separated)
    -o results/my_analysis \          # Output prefix
    -t 8 \                           # Number of threads
    -m 1000 \                        # Maximum reads to process (0 for all)
    -c 100 \                         # Chunk size for parallel processing
    -u \                             # Process only unaligned reads
    --max-distance 2 \               # Maximum Levenshtein distance for matching
    -v                               # Verbose output
```

### Python Package

```python
from uradime import bam_to_fasta_parallel, create_analysis_summary, load_primers

# Load and analyze BAM file
result_df = bam_to_fasta_parallel(
    bam_path="your_file.bam",
    primer_file="primers.tsv",
    num_threads=4
)

# Load primers for analysis
primers_df, _ = load_primers("primers.tsv")

# Create analysis summary
summary_df, matched_pairs, mismatched_pairs = create_analysis_summary(result_df, primers_df)
```

## Input Files

### Primer File Format (TSV)
The primer file should be tab-separated with the following columns:
- Name: Primer pair name
- Forward: Forward primer sequence
- Reverse: Reverse primer sequence
- Size: Expected amplicon size

Example:
```
Name    Forward             Reverse             Size
Pair1   ATCGATCGATCG       TAGCTAGCTAGC       100
Pair2   GCTAGCTAGCTA       CGATTCGATCGA       150
```

## Output Files

The tool generates several CSV files with the analysis results:
- `*_summary.csv`: Overall analysis summary
- `*_matched_pairs.csv`: Reads with matching primer pairs
- `*_mismatched_pairs.csv`: Reads with mismatched primer pairs
- `*_wrong_size_pairs.csv`: Reads with correct primer pairs but wrong size

## Features

- BAM file analysis
- Primer sequence identification
- Flexible matching with Levenshtein distance
- Comprehensive analysis reporting
- Parallel processing support
- Both CLI and Python API

## Requirements

- Python ≥3.7
- pysam
- pandas
- biopython
- python-Levenshtein
- tqdm
- numpy

## License

This project is licensed under the MIT License - see the LICENSE file for details.