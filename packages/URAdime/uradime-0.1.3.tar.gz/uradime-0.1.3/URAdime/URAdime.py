#!/usr/bin/env python3
"""
URAdime (Universal Read Analysis of DIMErs)
A tool for analyzing primer dimers and other artifacts in sequencing data.
This script processes BAM files to identify primer sequences at read ends
and analyzes their relationships and orientations.
"""

import argparse
import pysam
import pandas as pd
from Bio.Seq import Seq
import Levenshtein as lev
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple
import numpy as np
from tqdm import tqdm
import os
import sys

def load_primers(primer_file):
    """
    Load and prepare primers from a tab-separated file.
    
    Args:
        primer_file (str): Path to tab-separated primer file containing Name, Forward, Reverse, and Size columns
        
    Returns:
        tuple: (primers_df, longest_primer_length)
            - primers_df: DataFrame containing primer information
            - longest_primer_length: Length of the longest primer sequence
            
    Raises:
        FileNotFoundError: If primer file doesn't exist
    """
    if not os.path.exists(primer_file):
        raise FileNotFoundError(f"Primer file not found: {primer_file}")
        
    primers_df = pd.read_csv(primer_file, sep="\t")
    primers_df = primers_df.dropna(subset=['Forward', 'Reverse'])
    longest_primer_length = max(
        primers_df['Forward'].apply(len).max(), 
        primers_df['Reverse'].apply(len).max()
    )
    return primers_df, longest_primer_length

def is_match(seq1, seq2, max_distance):
    """
    Check for approximate match between two sequences using Levenshtein distance.
    Handles case-insensitive comparison and treats N's as potential matches.
    
    Args:
        seq1 (str): First sequence
        seq2 (str): Second sequence
        max_distance (int): Maximum allowed Levenshtein distance
        
    Returns:
        bool: True if sequences match within specified distance
    """
    if not seq1 or not seq2:
        return False
    
    try:
        # Convert to uppercase and remove N's for comparing lengths
        seq1 = str(seq1).upper()
        seq2 = str(seq2).upper()
        
        for i in range(len(seq1) - len(seq2) + 1):
            window = seq1[i:i+len(seq2)]
            if len(window) == len(seq2):
                # Calculate distance considering N's as potential matches
                distance = 0
                for w, s in zip(window, seq2):
                    if w != s and w != 'N' and s != 'N':
                        distance += 1
                        if distance > max_distance:
                            break
                
                if distance <= max_distance:
                    return True
    except:
        return False
    return False

def find_primers_in_region(sequence, primers_df, window_size, max_distance):
    """Find primers in a given sequence region"""
    primers_found = []
    
    for _, primer in primers_df.iterrows():
        forward_primer = primer['Forward']
        reverse_primer = primer['Reverse']
        forward_length = len(forward_primer)
        reverse_length = len(reverse_primer)
        
        # Calculate search window based on individual primer lengths
        forward_search_window = sequence[:min(window_size + forward_length, len(sequence))]
        reverse_search_window = sequence[:min(window_size + reverse_length, len(sequence))]
        
        reverse_complement_forward = str(Seq(forward_primer).reverse_complement())
        reverse_complement_reverse = str(Seq(reverse_primer).reverse_complement())
        
        if is_match(forward_search_window, forward_primer, max_distance):
            primers_found.append(f"{primer['Name']}_Forward")
        if is_match(reverse_search_window, reverse_primer, max_distance):
            primers_found.append(f"{primer['Name']}_Reverse")
        if is_match(forward_search_window, reverse_complement_forward, max_distance):
            primers_found.append(f"{primer['Name']}_ForwardComp")
        if is_match(reverse_search_window, reverse_complement_reverse, max_distance):
            primers_found.append(f"{primer['Name']}_ReverseComp")
    
    return list(set(primers_found))

def process_read_chunk(chunk: List[pysam.AlignedSegment], primers_df: pd.DataFrame, 
                      window_size: int, unaligned_only: bool,
                      max_distance: int) -> List[Dict]:  # Added max_distance parameter
    """Process a chunk of reads in parallel"""
    chunk_data = []
    
    # Calculate max primer length once for efficiency
    max_primer_length = max(
        primers_df['Forward'].apply(len).max(),
        primers_df['Reverse'].apply(len).max()
    )
    
    # Adjusted window size including primer length
    effective_window = window_size + max_primer_length
    
    for read in chunk:
        if unaligned_only and not read.is_unmapped:
            continue
        if read.query_sequence is None:
            continue

        read_sequence = read.query_sequence
        read_length = len(read_sequence)
        
        # Get sequences from both ends of the read
        start_region = read_sequence[:min(effective_window, read_length)]
        
        # Ensure we're getting the correct end region
        end_start_pos = max(0, read_length - effective_window)
        end_region = read_sequence[end_start_pos:]
        
        # Process start primers - pass max_distance
        start_primers_found = find_primers_in_region(
            start_region, 
            primers_df, 
            window_size=window_size,
            max_distance=max_distance
        )
        
        # Process end primers with reversed sequence - pass max_distance
        end_primers_found = find_primers_in_region(
            str(Seq(end_region).reverse_complement()),
            primers_df,
            window_size=window_size,
            max_distance=max_distance
        )
        
        chunk_data.append({
            'Read_Name': read.query_name,
            'Start_Primers': ', '.join(start_primers_found) if start_primers_found else 'None',
            'End_Primers': ', '.join(end_primers_found) if end_primers_found else 'None',
            'Read_Length': read_length,
            'Start_Region_Length': len(start_region),
            'End_Region_Length': len(end_region)
        })
    
    return chunk_data

def create_analysis_summary(result_df, primers_df, ignore_amplicon_size=False):
    """Create a comprehensive summary of primer analysis results"""
    if result_df.empty:
        print("No reads to analyze in the results dataframe")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        
    total_reads = len(result_df)
    
    def get_base_primer_name(primer_str):
        if primer_str == 'None':
            return None
        return primer_str.rsplit('_', 1)[0]
    
    def get_primer_orientation(primer_str):
        if primer_str == 'None':
            return None
        return primer_str.rsplit('_', 1)[1]
    
    result_df['Start_Primer_Name'] = result_df['Start_Primers'].apply(get_base_primer_name)
    result_df['End_Primer_Name'] = result_df['End_Primers'].apply(get_base_primer_name)
    result_df['Start_Orientation'] = result_df['Start_Primers'].apply(get_primer_orientation)
    result_df['End_Orientation'] = result_df['End_Primers'].apply(get_primer_orientation)
    
    no_primers = result_df[
        (result_df['Start_Primers'] == 'None') & 
        (result_df['End_Primers'] == 'None')
    ]
    
    single_end_only = result_df[
        ((result_df['Start_Primers'] != 'None') & (result_df['End_Primers'] == 'None')) |
        ((result_df['Start_Primers'] == 'None') & (result_df['End_Primers'] != 'None'))
    ]
    
    both_ends = result_df[
        (result_df['Start_Primers'] != 'None') & 
        (result_df['End_Primers'] != 'None')
    ]
    
    matched_pairs = both_ends[
        both_ends['Start_Primer_Name'] == both_ends['End_Primer_Name']
    ]
    
    mismatched_pairs = both_ends[
        both_ends['Start_Primer_Name'] != both_ends['End_Primer_Name']
    ]
    
    primer_sizes = primers_df.set_index('Name')['Size'].to_dict()
    
    def is_correct_orientation(row):
        if pd.isna(row['Start_Orientation']) or pd.isna(row['End_Orientation']):
            return False
        return (
            (row['Start_Orientation'].startswith('Forward') and 
             row['End_Orientation'].startswith('Reverse')) or
            (row['Start_Orientation'].startswith('Reverse') and 
             row['End_Orientation'].startswith('Forward'))
        )
 
    
    def is_size_compliant(row, ignore_amplicon_size):
        if ignore_amplicon_size:
            return True
        expected = primer_sizes.get(row['Start_Primer_Name'])
        if pd.isna(expected):
            return False
        tolerance = expected * 0.10
        return abs(row['Read_Length'] - expected) <= tolerance

    matched_pairs['Correct_Orientation'] = matched_pairs.apply(is_correct_orientation, axis=1)
    matched_pairs['Size_Compliant'] = matched_pairs.apply(is_size_compliant, axis=1, ignore_amplicon_size=ignore_amplicon_size)
    
    summary_data = [
        {
            'Category': 'No primers detected',
            'Count': len(no_primers),
            'Percentage': (len(no_primers) / total_reads) * 100
        },
        {
            'Category': 'Single-end primers only',
            'Count': len(single_end_only),
            'Percentage': (len(single_end_only) / total_reads) * 100
        },
        {
            'Category': 'Mismatched primer pairs',
            'Count': len(mismatched_pairs),
            'Percentage': (len(mismatched_pairs) / total_reads) * 100
        },
        # {
        #     'Category': 'Matched pairs - incorrect orientation',
        #     'Count': len(matched_pairs[~matched_pairs['Correct_Orientation']]),
        #     'Percentage': (len(matched_pairs[~matched_pairs['Correct_Orientation']]) / total_reads) * 100
        # },
        {
            'Category': 'Matched pairs - correct orientation, wrong size',
            'Count': len(matched_pairs[
                matched_pairs['Correct_Orientation'] & 
                ~matched_pairs['Size_Compliant']
            ]),
            'Percentage': (len(matched_pairs[
                matched_pairs['Correct_Orientation'] & 
                ~matched_pairs['Size_Compliant']
            ]) / total_reads) * 100
        },
        {
            'Category': 'Matched pairs - correct orientation and size',
            'Count': len(matched_pairs[
                matched_pairs['Correct_Orientation'] & 
                matched_pairs['Size_Compliant']
            ]),
            'Percentage': (len(matched_pairs[
                matched_pairs['Correct_Orientation'] & 
                matched_pairs['Size_Compliant']
            ]) / total_reads) * 100
        }
    ]
    
    summary_df = pd.DataFrame(summary_data)
    summary_df['Percentage'] = summary_df['Percentage'].round(2)
    
    return summary_df, matched_pairs, mismatched_pairs


def downsample_reads(bam_path: str, percentage: float, max_reads: int = 0) -> List[pysam.AlignedSegment]:
    """
    Downsample reads from a BAM file based on a percentage.
    
    Args:
        bam_path (str): Path to the BAM file
        percentage (float): Percentage of reads to keep (0.1-100.0)
        max_reads (int): Maximum number of reads to process (0 for all reads)
    
    Returns:
        List[pysam.AlignedSegment]: List of downsampled reads
    """
    if not (0.1 <= percentage <= 100.0):
        raise ValueError("Downsampling percentage must be between 0.1 and 100.0")
        
    print(f"Loading and downsampling BAM file to {percentage}% of reads...")
    
    try:
        bam_file = pysam.AlignmentFile(bam_path, "rb")
        
        # First pass to count total reads if needed
        total_reads = 0
        if max_reads == 0:
            print("Counting total reads...")
            for _ in tqdm(bam_file.fetch(until_eof=True)):
                total_reads += 1
            bam_file.reset()
        else:
            total_reads = max_reads
            
        # Calculate number of reads to keep
        keep_probability = percentage / 100.0
        target_reads = int(total_reads * keep_probability)
        
        if max_reads > 0:
            target_reads = min(target_reads, max_reads)
            
        print(f"Targeting {target_reads} reads after {percentage}% downsampling")
        
        # Second pass to collect downsampled reads
        downsampled_reads = []
        reads_processed = 0
        
        for read in tqdm(bam_file.fetch(until_eof=True), total=total_reads):
            reads_processed += 1
            
            # Use reservoir sampling if we don't know total reads
            if max_reads == 0:
                if len(downsampled_reads) < target_reads:
                    downsampled_reads.append(read)
                else:
                    j = random.randint(0, reads_processed)
                    if j < target_reads:
                        downsampled_reads[j] = read
            # Otherwise use simple random sampling
            else:
                if random.random() < keep_probability:
                    downsampled_reads.append(read)
                    if len(downsampled_reads) >= target_reads:
                        break
            
            if max_reads > 0 and reads_processed >= max_reads:
                break
                
        bam_file.close()
        
        print(f"Selected {len(downsampled_reads)} reads after downsampling")
        return downsampled_reads
        
    except Exception as e:
        print(f"Error during downsampling: {e}")
        return []

def bam_to_fasta_parallel(bam_path: str, primer_file: str, window_size: int = 20, 
                         unaligned_only: bool = False, max_reads: int = 200, 
                         num_threads: int = 4, chunk_size: int = 50, 
                         downsample_percentage: float = 100.0,
                         max_distance: int = 2) -> pd.DataFrame:  # Added max_distance parameter
    """Process BAM file and find primers in reads using multiple threads"""
    # Validate input files
    if not os.path.exists(bam_path):
        raise FileNotFoundError(f"BAM file not found: {bam_path}")
    
    # Load primers
    primers_df, _ = load_primers(primer_file)
    
    print(f"Loading BAM file: {bam_path}")
    
    # Perform downsampling
    all_reads = downsample_reads(bam_path, downsample_percentage, max_reads)
    
    if not all_reads:
        print("No reads selected after downsampling")
        return pd.DataFrame()
    
    print(f"Processing {len(all_reads)} reads with {num_threads} threads...")
    
    chunks = [all_reads[i:i + chunk_size] for i in range(0, len(all_reads), chunk_size)]
    
    all_data = []
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_chunk = {
            executor.submit(
                process_read_chunk, 
                chunk, 
                primers_df, 
                window_size, 
                unaligned_only,
                max_distance  # Pass max_distance to process_read_chunk
            ): chunk for chunk in chunks
        }
        
        for future in tqdm(as_completed(future_to_chunk), total=len(chunks), desc="Processing chunks"):
            try:
                chunk_data = future.result()
                all_data.extend(chunk_data)
            except Exception as e:
                print(f"Error processing chunk: {e}")
    
    if not all_data:
        print("No data was processed successfully")
        return pd.DataFrame()
        
    return pd.DataFrame(all_data)


def parallel_analysis_pipeline(bam_path: str, primer_file: str, window_size: int = 20,
                             num_threads: int = 4, max_reads: int = 200, chunk_size: int = 50,
                             ignore_amplicon_size: bool = False,
                             max_distance: int = 2, 
                             downsample_percentage: float = 100.0,
                             unaligned_only: bool = False):
    """Complete analysis pipeline using parallel processing"""
    print(f"Starting analysis with {num_threads} threads...")
    
    try:
        result_df = bam_to_fasta_parallel(
            bam_path=bam_path,
            primer_file=primer_file,
            window_size=window_size,
            max_reads=max_reads,
            num_threads=num_threads,
            chunk_size=chunk_size,
            max_distance=max_distance,  # Add missing parameters
            downsample_percentage=downsample_percentage,
            unaligned_only=unaligned_only
        )
        
        if result_df.empty:
            print("No results generated. Check input files and parameters.")
            return None
        
        print(f"\nProcessed {len(result_df)} reads successfully")
        
        primers_df, _ = load_primers(primer_file)
        
        summary_df, matched_pairs, mismatched_pairs = create_analysis_summary(
            result_df, 
            primers_df,
            ignore_amplicon_size=ignore_amplicon_size
        )
        print("\nAnalysis Summary:")
        print(summary_df.to_string(index=False))
        
        return {
            'results': result_df,
            'summary': summary_df,
            'matched_pairs': matched_pairs,
            'mismatched_pairs': mismatched_pairs
        }
        
    except Exception as e:
        print(f"Error in analysis pipeline: {str(e)}")
        return None

def parse_arguments():
    """Parse command line arguments for URAdime."""
    parser = argparse.ArgumentParser(
        description="URAdime - Universal Read Analysis of DIMErs",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "-b", "--bam",
        required=True,
        help="Input BAM file path"
    )
    
    parser.add_argument(
        "-p", "--primers",
        required=True,
        help="Tab-separated primer file containing columns: Name, Forward, Reverse, Size"
    )
    
    parser.add_argument(
        "-o", "--output",
        default="uradime_results",
        help="Output prefix for result files"
    )
    
    parser.add_argument(
        "-t", "--threads",
        type=int,
        default=4,
        help="Number of threads to use for parallel processing"
    )
    
    parser.add_argument(
        "-m", "--max-reads",
        type=int,
        default=0,
        help="Maximum number of reads to process (0 for all reads)"
    )
    
    parser.add_argument(
        "-c", "--chunk-size",
        type=int,
        default=50,
        help="Number of reads to process in each thread chunk"
    )
    
    parser.add_argument(
        "-u", "--unaligned-only",
        action="store_true",
        help="Process only unaligned reads"
    )
    
    parser.add_argument(
        "--max-distance",
        type=int,
        default=2,
        help="Maximum Levenshtein distance for primer matching"
    )
    
    parser.add_argument(
        "-w", "--window-size",
        type=int,
        default=20,
        help="Size of the window to search for primers at read ends"
    )

    parser.add_argument("--ignore-amplicon-size", 
        action="store_true", 
        help="Ignore amplicon size compliance checks"
        )

    parser.add_argument(
        "-d", "--downsample",
        type=float,
        default=100.0,
        help="Percentage of reads to randomly sample from the BAM file (0.1-100.0)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print detailed progress information"
    )
    
    return parser.parse_args()

def validate_inputs(args):
    """Validate input files and parameters."""
    if not os.path.exists(args.bam):
        raise FileNotFoundError(f"BAM file not found: {args.bam}")
    
    if not os.path.exists(args.primers):
        raise FileNotFoundError(f"Primer file not found: {args.primers}")

    if args.downsample <= 0 or args.downsample > 100:
        raise ValueError("Downsampling percentage must be between 0.1 and 100")
    
    try:
        primers_df = pd.read_csv(args.primers, sep="\t")
        required_columns = ['Name', 'Forward', 'Reverse', 'Size']
        missing_columns = [col for col in required_columns if col not in primers_df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns in primer file: {', '.join(missing_columns)}")
    except Exception as e:
        raise ValueError(f"Error reading primer file: {str(e)}")
    
    if args.max_distance < 0:
        raise ValueError("Maximum distance must be non-negative")
    
    if args.threads < 1:
        raise ValueError("Number of threads must be positive")
    
    if args.chunk_size < 1:
        raise ValueError("Chunk size must be positive")
        
    if args.window_size < 1:
        raise ValueError("Window size must be positive")

def create_primer_statistics(matched_pairs, primers_df, total_reads):
    """Create statistics for each primer pair"""
    primer_stats = []
    
    for primer_name in primers_df['Name'].unique():
        # Get all reads where this primer appears
        primer_matches = matched_pairs[matched_pairs['Start_Primer_Name'] == primer_name].copy()
        
        if len(primer_matches) == 0:
            continue
            
        total_appearances = len(primer_matches)
        stats = {
            'Primer_Name': primer_name,
            'Total_Appearances': total_appearances,
            'Percentage_of_Total_Reads': round((total_appearances / total_reads * 100), 2),
            'Correct_Orientation_Percentage': round(
                (len(primer_matches[primer_matches['Correct_Orientation']]) / 
                total_appearances * 100), 2
            ),
            'Size_Compliant_Percentage': round(
                (len(primer_matches[primer_matches['Size_Compliant']]) / 
                total_appearances * 100), 2
            ),
            'Correct_Orientation_and_Size_Percentage': round(
                (len(primer_matches[
                    primer_matches['Correct_Orientation'] & 
                    primer_matches['Size_Compliant']
                ]) / total_appearances * 100), 2
            )
        }
        
        primer_stats.append(stats)
    
    return pd.DataFrame(primer_stats)

def save_results(results, output_prefix, primers_df):
    """Save analysis results to files."""
    os.makedirs(os.path.dirname(output_prefix) if os.path.dirname(output_prefix) else '.', exist_ok=True)
    
    # Save summary
    results['summary'].to_csv(f"{output_prefix}_summary.csv", index=False)
    
    # Save matched pairs
    if not results['matched_pairs'].empty:
        results['matched_pairs'].to_csv(f"{output_prefix}_matched_pairs.csv", index=False)
        
        # Generate and save primer statistics using existing primers_df
        primer_stats = create_primer_statistics(
            results['matched_pairs'].copy(),  # Create a copy to avoid the warning
            primers_df,
            len(results['results'])
        )
        primer_stats.to_csv(f"{output_prefix}_primer_statistics.csv", index=False)
    
    # Save mismatched pairs
    if not results['mismatched_pairs'].empty:
        results['mismatched_pairs'].to_csv(f"{output_prefix}_mismatched_pairs.csv", index=False)
    
    # Save wrong size pairs
    wrong_size_pairs = results['matched_pairs'][
        results['matched_pairs']['Correct_Orientation'] & 
        ~results['matched_pairs']['Size_Compliant']
    ].copy()  # Create a copy to avoid the warning
    
    if not wrong_size_pairs.empty:
        wrong_size_pairs.to_csv(f"{output_prefix}_wrong_size_pairs.csv", index=False)

def main():
    """Main execution function for URAdime."""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Validate inputs
        validate_inputs(args)
        
        if args.verbose:
            print("Starting URAdime analysis...")
            print(f"Input BAM: {args.bam}")
            print(f"Input primers: {args.primers}")
            print(f"Using {args.threads} threads")
            print(f"Window size: {args.window_size}")
            print(f"Max distance: {args.max_distance}")  # Added log message
            print(f"Downsampling to {args.downsample}% of reads")
        
        # Process BAM file - pass max_distance from args
        result_df = bam_to_fasta_parallel(
            bam_path=args.bam,
            primer_file=args.primers,
            window_size=args.window_size,
            unaligned_only=args.unaligned_only,
            max_reads=args.max_reads,
            num_threads=args.threads,
            chunk_size=args.chunk_size,
            downsample_percentage=args.downsample,
            max_distance=args.max_distance  # Pass max_distance from args
        )
        
        if result_df.empty:
            print("No results generated. Check input files and parameters.")
            return 1
        
        if args.verbose:
            print(f"\nProcessed {len(result_df)} reads successfully")
        
        # Load primers for analysis
        primers_df, _ = load_primers(args.primers)
        
        # Create analysis summary
        summary_df, matched_pairs, mismatched_pairs = create_analysis_summary(
            result_df, 
            primers_df,
            ignore_amplicon_size=args.ignore_amplicon_size
        )

        # Prepare results dictionary
        results = {
            'results': result_df,
            'summary': summary_df,
            'matched_pairs': matched_pairs,
            'mismatched_pairs': mismatched_pairs
        }
        
        # Save results
        save_results(results, args.output, primers_df)
        
        # Print summary to console
        print("\nAnalysis Summary:")
        print("=" * 80)
        print(summary_df.to_string(index=False))
        
        if args.verbose:
            print(f"\nResults saved with prefix: {args.output}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())