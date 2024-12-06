"""URAdime - A package for analyzing primers in BAM files."""

from .URAdime import (
    load_primers,
    bam_to_fasta_parallel,
    create_analysis_summary,
    parse_arguments,
    validate_inputs,
    save_results,
    main
)

__version__ = "0.1.1"