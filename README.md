# sam2ident.py

A python tool to filter sam/bam files by percent identity which be calculated with this tool.

### NOTE:

you need to install pysam first with this command:

`pip install pysam`

### USAGE:

```python
usage: sam2ident.py [-h] [-i] [-s] [-o1] [-o2] bam
Tools to filter SAM/BAM files by percent identity or percent of matched sequence,
        For example: python sam2ident -input samfile -ident ident_value -show_ident True/Flase -o1 fastq -o2 text

positional arguments:
  bam                 the input sam/bam file

options:
  -h, --help          show this help message and exit
  -i , --identity     filter by given percent identity,Default:0.8
  -s , --show_ident   whether output identity of each filtered read or not,Default:Flase
  -o1 , --output1     Path to output the filtered reads in FASTQ format
  -o2 , --output2     Path to output the identity of each filtered read in text format. Only works when the '-show_ident' is 'True.'

Example:
python sam2ident.py -i 0.8 -s Ture -o1 toy_sample_filter.fq -o2 toy_sample_filter_ident.txt toy_sample.sam
```

It's worth noting that, 

1):The calculation of query seq length is based on the mapping to reference section with pysam module. i.e, query_alignment_length = query_alignment_end - query_alignment_start. You can visualize this alignment by sam2pairwirse tool.

2):when you set the `-s` parameter to ` 'True'`, you will obtain the `toy_sample_filter_ident.txt` file containing `'read_name', 'ref_name', 'ident', 'cigar', 'MD tag'` informations.
