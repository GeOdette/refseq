"""
Find what NCBI RefSeq genomes match  your sequence data
"""

import subprocess
from pathlib import Path
import os
from latch import small_task, workflow
from latch.types import LatchFile


@small_task
def refseq_masher_task(input_file: LatchFile, option: str) -> LatchFile:

    # A reference to our output dir.
    output_file = Path("refseq").resolve()

    _refseq_cmd = [
        "refseq_masher",
        "-vv",
        str(option),
        input_file.local_path,

    ]
    with open(output_file, "w") as f:
        subprocess.run(_refseq_cmd, stderr=f, stdout=f)

    return LatchFile(str(output_file), f"latch:///{output_file}")


@ workflow
def refseq(input_file: LatchFile, option: str) -> LatchFile:
    """Find what NCBI RefSeq genomes match  your sequence data



    __metadata__:
        display_name: Find what NCBI RefSeq genomes match  your sequence data
        author:
            name:
            email:
            github:
        repository:
        license:
            id: MIT

    Args:

        input_file:
          FASTA/FASTQ file with sequence

          __metadata__:
            display_name: Input File

        option:
          Option to run

          __metadata__:
            display_name: Option
    """
    return refseq_masher_task(input_file=input_file, option=option)
