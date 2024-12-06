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
    """Load and prepare primers dataframe"""
    if not os.path.exists(primer_file):
        raise FileNotFoundError(f"Primer file not found: {primer_file}")
        
    primers_df = pd.read_csv(primer_file, sep="\t")
    primers_df = primers_df.dropna(subset=['Forward', 'Reverse'])
    longest_primer_length = max(
        primers_df['Forward'].apply(len).max(), 
        primers_df['Reverse'].apply(len).max()
    )
    return primers_df, longest_primer_length

def is_match(seq1, seq2, max_distance=2):
    """Check for approx match using Levenshtein distance."""
    if not seq1 or not seq2:
        return False
    
    try:
        for i in range(len(seq1) - len(seq2) + 1):
            window = seq1[i:i+len(seq2)]
            if len(window) == len(seq2):
                distance = lev.distance(str(window), str(seq2))
                if distance <= max_distance:
                    return True
    except:
        return False
    return False

def find_primers_in_region(sequence, primers_df, window_size=100, max_distance=2):
    """Find primers in a given sequence region"""
    primers_found = []
    
    for _, primer in primers_df.iterrows():
        forward_primer = primer['Forward']
        reverse_primer = primer['Reverse']
        reverse_complement_forward = str(Seq(forward_primer).reverse_complement())
        reverse_complement_reverse = str(Seq(reverse_primer).reverse_complement())
        
        if is_match(sequence, forward_primer, max_distance):
            primers_found.append(f"{primer['Name']}_Forward")
        if is_match(sequence, reverse_primer, max_distance):
            primers_found.append(f"{primer['Name']}_Reverse")
        if is_match(sequence, reverse_complement_forward, max_distance):
            primers_found.append(f"{primer['Name']}_ForwardComp")
        if is_match(sequence, reverse_complement_reverse, max_distance):
            primers_found.append(f"{primer['Name']}_ReverseComp")
    
    return list(set(primers_found))

def process_read_chunk(chunk: List[pysam.AlignedSegment], primers_df: pd.DataFrame, 
                      search_window: int, unaligned_only: bool) -> List[Dict]:
    """Process a chunk of reads in parallel"""
    chunk_data = []
    
    for read in chunk:
        if unaligned_only and not read.is_unmapped:
            continue
        if read.query_sequence is None:
            continue

        read_sequence = read.query_sequence
        read_length = len(read_sequence)
        
        start_region = read_sequence[:min(search_window, read_length)]
        end_region = read_sequence[max(0, read_length - search_window):]
        
        start_primers_found = find_primers_in_region(start_region, primers_df, window_size=search_window)
        end_primers_found = find_primers_in_region(end_region, primers_df, window_size=search_window)
        
        chunk_data.append({
            'Read_Name': read.query_name,
            'Start_Primers': ', '.join(start_primers_found) if start_primers_found else 'None',
            'End_Primers': ', '.join(end_primers_found) if end_primers_found else 'None',
            'Read_Length': read_length
        })
    
    return chunk_data

def create_analysis_summary(result_df, primers_df):
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
    
    def is_size_compliant(row):
        expected = primer_sizes.get(row['Start_Primer_Name'])
        if pd.isna(expected):
            return False
        tolerance = expected * 0.10
        return abs(row['Read_Length'] - expected) <= tolerance
    
    matched_pairs['Correct_Orientation'] = matched_pairs.apply(is_correct_orientation, axis=1)
    matched_pairs['Size_Compliant'] = matched_pairs.apply(is_size_compliant, axis=1)
    
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
        {
            'Category': 'Matched pairs - incorrect orientation',
            'Count': len(matched_pairs[~matched_pairs['Correct_Orientation']]),
            'Percentage': (len(matched_pairs[~matched_pairs['Correct_Orientation']]) / total_reads) * 100
        },
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

def bam_to_fasta_parallel(bam_path: str, primer_file: str, unaligned_only: bool = False, 
                         max_reads: int = 200, num_threads: int = 4, chunk_size: int = 50) -> pd.DataFrame:
    """Process BAM file and find primers in reads using multiple threads"""
    # Validate input files
    if not os.path.exists(bam_path):
        raise FileNotFoundError(f"BAM file not found: {bam_path}")
    
    # Load primers
    primers_df, longest_primer_length = load_primers(primer_file)
    search_window = 100 + longest_primer_length
    
    print(f"Loading BAM file: {bam_path}")
    try:
        bam_file = pysam.AlignmentFile(bam_path, "rb")
    except Exception as e:
        print(f"Error opening BAM file: {e}")
        return pd.DataFrame()

    # Read all reads into memory (up to max_reads)
    print("Loading reads into memory...")
    all_reads = []
    for read in tqdm(bam_file.fetch(until_eof=True), total=max_reads if max_reads > 0 else None):
        all_reads.append(read)
        if max_reads > 0 and len(all_reads) >= max_reads:
            break
    
    print(f"Processing {len(all_reads)} reads with {num_threads} threads...")
    
    # Split reads into chunks
    chunks = [all_reads[i:i + chunk_size] for i in range(0, len(all_reads), chunk_size)]
    
    all_data = []
    
    # Process chunks in parallel with progress bar
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_chunk = {
            executor.submit(
                process_read_chunk, 
                chunk, 
                primers_df, 
                search_window, 
                unaligned_only
            ): chunk for chunk in chunks
        }
        
        for future in tqdm(as_completed(future_to_chunk), total=len(chunks), desc="Processing chunks"):
            try:
                chunk_data = future.result()
                all_data.extend(chunk_data)
            except Exception as e:
                print(f"Error processing chunk: {e}")
    
    bam_file.close()
    
    if not all_data:
        print("No data was processed successfully")
        return pd.DataFrame()
        
    return pd.DataFrame(all_data)

def parallel_analysis_pipeline(bam_path: str, primer_file: str, num_threads: int = 4, 
                             max_reads: int = 200, chunk_size: int = 50):
    """Complete analysis pipeline using parallel processing"""
    print(f"Starting analysis with {num_threads} threads...")
    
    try:
        # Process BAM file in parallel
        result_df = bam_to_fasta_parallel(
            bam_path=bam_path,
            primer_file=primer_file,
            max_reads=max_reads,
            num_threads=num_threads,
            chunk_size=chunk_size
        )
        
        if result_df.empty:
            print("No results generated. Check input files and parameters.")
            return None
        
        print(f"\nProcessed {len(result_df)} reads successfully")
        
        # Load primers for analysis
        primers_df, _ = load_primers(primer_file)
        
        # Create analysis summary
        summary_df, matched_pairs, mismatched_pairs = create_analysis_summary(result_df, primers_df)
        
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

def save_results(results, output_prefix):
    """Save analysis results to files."""
    os.makedirs(os.path.dirname(output_prefix) if os.path.dirname(output_prefix) else '.', exist_ok=True)
    
    # Save summary
    results['summary'].to_csv(f"{output_prefix}_summary.csv", index=False)
    
    # Save matched pairs
    if not results['matched_pairs'].empty:
        results['matched_pairs'].to_csv(f"{output_prefix}_matched_pairs.csv", index=False)
    
    # Save mismatched pairs
    if not results['mismatched_pairs'].empty:
        results['mismatched_pairs'].to_csv(f"{output_prefix}_mismatched_pairs.csv", index=False)
    
    # Save wrong size pairs
    wrong_size_pairs = results['matched_pairs'][
        results['matched_pairs']['Correct_Orientation'] & 
        ~results['matched_pairs']['Size_Compliant']
    ]
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
        
        # Process BAM file
        result_df = bam_to_fasta_parallel(
            bam_path=args.bam,
            primer_file=args.primers,
            unaligned_only=args.unaligned_only,
            max_reads=args.max_reads,
            num_threads=args.threads,
            chunk_size=args.chunk_size
        )
        
        if result_df.empty:
            print("No results generated. Check input files and parameters.")
            return 1
        
        if args.verbose:
            print(f"\nProcessed {len(result_df)} reads successfully")
        
        # Load primers for analysis
        primers_df, _ = load_primers(args.primers)
        
        # Create analysis summary
        summary_df, matched_pairs, mismatched_pairs = create_analysis_summary(result_df, primers_df)
        
        # Prepare results dictionary
        results = {
            'results': result_df,
            'summary': summary_df,
            'matched_pairs': matched_pairs,
            'mismatched_pairs': mismatched_pairs
        }
        
        # Save results
        save_results(results, args.output)
        
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