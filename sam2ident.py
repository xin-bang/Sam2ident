#!usr/bin/python
import pysam
import argparse
import re

parser = argparse.ArgumentParser(
    prog='sam2ident.py',
    description="Tools to filter SAM/BAM files by percent identity or percent of matched sequence,\n\
        For example: python sam2ident -input samfile -ident ident_value -show_ident True/Flase -o1 fastq -o2 text",
    epilog="  \n",
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument("bam", type=str,
                    help="the input sam/bam file")
parser.add_argument("-i",  '--identity',metavar = '',type=float, default=0.8,
                    help="filter by given percent identity,Default:0.8")
parser.add_argument("-s", '--show_ident',metavar = '',type=bool, default="Flase",
                    help="whether output identity of each filtered read or not,Default:Flase")
parser.add_argument("-o1",'--output1',metavar = '', type=str,
                    help="Path to output the filtered reads in FASTQ format")
parser.add_argument("-o2", '--output2',metavar = '',type=str,
                    help="Path to output the identity of each filtered read in text format. Only works when the '-show_ident' is 'True.'")
args = parser.parse_args()



# open sam file
def process_sam(sam_filename):
    with pysam.AlignmentFile(sam_filename, "r") as sam_file:
        filter_hub =[]
        ident_hub =[]
        
        for record in sam_file:
            length = record.query_length
            
            # catch MD tag
            try:
                md_tag = record.get_tag("MD")
                # calculation the match base
                match = sum(map(int, re.findall(r'\d+', md_tag)))

                #Pysam module recognition of the length of the query alignment section is to identify the mapping length of the query in ref.
                #i.e,query_alignment_length = query_alignment_end - query_alignment_start. You can visualize this alignment by sam2pairwirse tool.
                length = record.query_alignment_length   
                
                try:
                    ident = match / length
                    if ident > args.identity:
                        filter_read = "@"+str(record.query_name)+"\n"+str(record.query)+"\n"+"+"+"\n"+str(record.qqual)
                        filter_hub.append(filter_read)

                        filter_ident = str(record.query_name) + "\t" + str(record.reference_name) + "\t" + str(ident)+"\t" + str(record.cigarstring) + "\t" +str(md_tag)
                        ident_hub.append(filter_ident)
                except ZeroDivisionError:
                    unfilter_ident = str(record.query_name) + "\t" + str(record.reference_name) + "\t" +"NULL"+"\t" + str(record.cigarstring) + "\t" +str(md_tag)
                    ident_hub.append(unfiler_ident)
                    pass
            except KeyError:
                # print (f"{record.query_name} can not align any reference")
                pass





        return filter_hub,ident_hub
    
def filter_hub_t_fq(filter_hub,ident_hub):
    fastq_output_filename = args.output1
    with open(fastq_output_filename, "w") as output_file:
        for filter_read in filter_hub:
            output_file.write(filter_read + "\n")

    if args.show_ident:
        ident_out_filename = args.output2
        with open(ident_out_filename,'w') as output_file:
            output_file.write('read_name'+"\t"+'ref_name'+"\t"+"ident"+"\t"+"cigar"+"\t"+"MD tag"+"\n")
            for filter_ident in ident_hub:
                output_file.write(filter_ident+"\n")
    else:
        pass


    
def main():
    filter_hub,ident_hub = process_sam(args.bam)
    filter_hub_t_fq(filter_hub=filter_hub,ident_hub=ident_hub)

if __name__ == "__main__":
    main()

