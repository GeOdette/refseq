"""
Find what NCBI RefSeq genomes match  your sequence data
"""

import subprocess
from pathlib import Path
import os
from latch import small_task, workflow
from latch.types import LatchFile, LatchDir
from typing import Optional


@small_task
def refseq_masher_task(
    input_dir: Optional[LatchDir],
    output_dir: LatchDir,
    match_option: bool = False,
    contains_option: bool = False,
    display_results: int = 50,
    threads_spawn: int = 1,
) -> LatchDir:

    # specifying the input
    file_extensions = ['.fasta', '.fa', '.fastq',
                       '.fq', '.FASTA', '.FA', '.FASTQ', '.FQ', '.gz']
    input_files = [f for f in Path(
        input_dir).iterdir()if f.suffix in file_extensions]
    files = [f.as_posix() for f in input_files]

    # creat directory
    out_dir = Path("local_dir").resolve()

    if match_option == True:
        _refseq_cmd = [
            "refseq_masher",
            "-vv",
            "matches",
            "-o",
            str(out_dir),
            "--output-type",
            "tab",
            *files,

        ]

    if contains_option == True:

        _refseq_cmd = [
            "refseq_masher",
            "-vv",
            "contains",
            "--top-n-results",
            str(display_results),
            "-p",
            str(threads_spawn),
            "-o",
            str(out_dir),
            "--output-type",
            "tab",
            *files,

        ]

    subprocess.run(_refseq_cmd, check=True)

    return LatchDir(str(out_dir), output_dir.remote_path)


@ workflow
def refseq(
    input_dir: Optional[LatchDir],
    output_dir: LatchDir,
    match_option: bool = False,
    contains_option: bool = False,
    display_results: int = 50,
    threads_spawn: int = 1,
) -> LatchDir:
    """Find what NCBI RefSeq genomes match  your sequence data



    __metadata__:
        display_name: Find what NCBI RefSeq genomes match or are contained in your sequence data
        author:

            name:

            email:

            github: 
        repository: https://github.com/phac-nml/refseq_masher.git

        license:
            id: MIT

    Args:

        input_dir:
          The input directory with FASTA or FASTQ files

          __metadata__:
            display_name: Input Directory

        output_dir:
          Where you wish to store your files. *Tip: Create an output directory at the latch console

          __metadata__:
            display_name: Output Directory

        match_option:
          *Choose this if you wish to find the closest matching NCBI RefSeq Genomes in your input sequences

          __metadata__:
            display_name: Match Option

        contains_option:
          Choose this if you want to find what NCBI RefSeq Genomes are contained in your input sequences

          __metadata__:
            display_name: Contain option

        display_results:
          *Enter as interger Output top N results sorted by identity in ascending orde

          __metadata__:
            display_name: Display results

        threads_spawn:
          Number of threads to spawn

          __metadata__:
            display_name: Number of threads to spawn
    """
    return refseq_masher_task(
        input_dir=input_dir,
        output_dir=output_dir,
        match_option=match_option,
        contains_option=contains_option,
        display_results=display_results,
        threads_spawn=threads_spawn,)
