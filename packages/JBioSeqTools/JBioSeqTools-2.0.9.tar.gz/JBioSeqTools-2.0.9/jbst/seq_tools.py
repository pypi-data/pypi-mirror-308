import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd
import pkg_resources
import re
import platform
import os
import RNA
import networkx as nx
import pandas as pd
import subprocess
from Bio import AlignIO
from Bio import Entrez, SeqIO
Entrez.email = "jseq.info@gmail.com"   
from pymsaviz import MsaViz 
import random
import string
from collections import Counter
import xml.etree.ElementTree as ET
import warnings
import json
import time
import random

random.seed(42)

 #       _  ____   _         _____              _                      __ _____  __  
 #      | ||  _ \ (_)       / ____|            | |                    / /|  __ \ \ \ 
 #      | || |_) | _   ___ | (___   _   _  ___ | |_  ___  _ __ ___   | | | |__) | | |
 #  _   | ||  _ < | | / _ \ \___ \ | | | |/ __|| __|/ _ \| '_ ` _ \  | | |  _  /  | |
 # | |__| || |_) || || (_) |____) || |_| |\__ \| |_|  __/| | | | | | | | | | \ \  | |
 #  \____/ |____/ |_| \___/|_____/  \__, ||___/ \__|\___||_| |_| |_|  \_\|_|  \_\/_/
 #                                   __/ |                                   
 #                                  |___/                                                                               


warnings.filterwarnings("ignore")

#Geta data directory

def get_package_directory():
    return pkg_resources.resource_filename(__name__, '')


_cwd = str(get_package_directory())


def random_name(length=30):
    # Define a string of characters to choose from
    characters = string.ascii_letters + string.digits

    # Generate a random name by selecting random characters
    name = ''.join(random.choice(characters) for _ in range(length))
    return name


## Ref_sequences download


def search_refseq(query, max_results=20):
    
    
    try:
        handle = Entrez.esearch(db="nuccore", term=query, retmax=max_results, idtype="acc")
        records = Entrez.read(handle)
        accession_numbers = records["IdList"]
        accession_numbers = [x for x in accession_numbers if 'NM_' in x]
        return accession_numbers
    except:
        
        print('\nThe problem may be due to temporary problems with the NCBI server. Try again in several minutes or contact us!')
        return None





def fetch_refseq_sequences(accession_numbers):
    try:
        refseq_sequences = {'sequences':[], 'features':[]}
    
        for accession in accession_numbers:
            handle = Entrez.efetch(db="nucleotide", id=accession, rettype="gb", retmode="text")
            record = SeqIO.read(handle, "genbank")
            if record.seq:  # Check if the sequence content is not empty
                refseq_sequences['sequences'].append(record)
                
                feature_dict = {}
    
                # Iterate through the features and extract their sequences
                for feature in record.features:
                    feature_type = feature.type
                    feature_location = feature.location
                    
                    try: 
                        # version 1.81 - error
                        
                        feature_location.start.position.real
                            
                        try:
                            tmp = {'start':int(feature_location.start.position.real),
                                   'stop':int(feature_location.end.position.real)}
                        except:
                            tmp = {'start':int(feature_location.start.position.real),
                                   'stop':int(feature_location.start.position.real)}
                            
                    except:
                        
                        #version > 1.81
                        try:
                            tmp = {'start':int(feature_location.start.real),
                                   'stop':int(feature_location.end.real)}
                        except:
                            tmp = {'start':int(feature_location.start.real),
                                   'stop':int(feature_location.start.real)}
                            
                        
                        
                        
                    feature_dict[feature_type] = tmp

                
                refseq_sequences['features'].append(feature_dict)
    
    
        return refseq_sequences
    
    except:
        
        print('\nSomething went wrong - fetch_refseq_sequences. Check the input or contact us!')
        return None






def sequences_decode(refseq_sequences):
    try:
        refseq_sequences['id'] = []
        refseq_sequences['name'] = []
        refseq_sequences['seq'] = []
    
        for n, i in enumerate(refseq_sequences['sequences']):
            refseq_sequences['id'].append(refseq_sequences['sequences'][n].id)
            refseq_sequences['name'].append(refseq_sequences['sequences'][n].description)
            refseq_sequences['seq'].append(refseq_sequences['sequences'][n].seq._data.decode('utf-8'))
            
            
        return refseq_sequences
    
    except:
        
        print('\nSomething went wrong - sequences_decode. Check the input or contact us!')
        return None


      


def get_sequences_gene(gene_name:str, species:str = 'human', max_results:int = 20):
    
    """
    This function gets sequences from NCBI database based on gene name & species
        
    Args:
        gene_name (str) - name of searching gene in the HGNC nomenclature
        species (str) - specie for which the gene sequence is searching (human / mouse / rat / both* / both2* / multi* / other**). Default: 'human'
       
            *both - gene sequences for Mus musculus and Homo sapiens
            *both2 - gene sequences for Rattus norvegicus and Homo sapiens
            *multi - gene sequences for Mus musculus, Rattus norvegicus, and Homo sapiens
       
            **other - the user can provide any species in Latin language via binomial nomenclature eg. Bos taurus, Zea mays, Sus scrofa, Danio rerio, Oryza sativa ...
       
        max_results (int) - number of maximal amount of results for the provided gene and species. Default: 20
        input_dict (dict) - dictionary of metadata provided by the user

    Returns:
        dict: Dictionary including all sequence variants, their names, features, and IDs of provided gene
       
    """
    
    gene_name = gene_name.upper()
    
    n = 0
    stop = False
    while(stop == False):
        try:
            n += 1
            if species.lower() == 'human':
                query = f"{gene_name}[Gene Name] AND Homo sapiens[Organism]"
                accession_numbers = search_refseq(query, max_results=max_results)
                refseq_sequences = fetch_refseq_sequences(accession_numbers)
                refseq_sequences = sequences_decode(refseq_sequences)
                refseq_sequences['gene_name'] = [re.sub('\).*', '', re.sub('.*\(', '', x)).upper() for x in refseq_sequences['name']]
                if len(refseq_sequences['sequences']) > 0:
                    word_counts = Counter(refseq_sequences['gene_name'])
                    df = pd.DataFrame({'Word': word_counts.keys(), 'Count': word_counts.values()})
                    df = df.sort_values('Count', ascending = False)
                    df = df.reset_index()
                    if max(df['Count']) > min(df['Count']):
                        gen = df['Word'][0]
                    elif len(df['Count']) == 1:
                        gen = df['Word'][0]
                    else: 
                        gen = gene_name
                        
                        
                    refseq_sequences = pd.DataFrame(refseq_sequences)
                    refseq_sequences = refseq_sequences[refseq_sequences['gene_name'] == gen].to_dict(orient = 'list')
                    
                else:
                    refseq_sequences = None
                    
    
            
            elif species.lower() == 'mouse':
                  query = f"{gene_name}[Gene Name] AND Mus musculus[Organism]"
                  accession_numbers = search_refseq(query, max_results=max_results)
                  refseq_sequences = fetch_refseq_sequences(accession_numbers)
                  refseq_sequences = sequences_decode(refseq_sequences)
                  refseq_sequences['gene_name'] = [re.sub('\).*', '', re.sub('.*\(', '', x)).upper() for x in refseq_sequences['name']]
                  if len(refseq_sequences['sequences']) > 0:
                      word_counts = Counter(refseq_sequences['gene_name'])
                      df = pd.DataFrame({'Word': word_counts.keys(), 'Count': word_counts.values()})
                      df = df.sort_values('Count', ascending = False)
                      df = df.reset_index()
                      if max(df['Count']) > min(df['Count']):
                          gen = df['Word'][0]
                      elif len(df['Count']) == 1:
                          gen = df['Word'][0]
                      else: 
                          gen = gene_name
                        
                        
                      refseq_sequences = pd.DataFrame(refseq_sequences)
                      refseq_sequences = refseq_sequences[refseq_sequences['gene_name'] == gen].to_dict(orient = 'list')
                    
                  else:
                      refseq_sequences = None
                     
            elif species.lower() == 'rat':
                  query = f"{gene_name}[Gene Name] AND Rattus norvegicus[Organism]"
                  accession_numbers = search_refseq(query, max_results=max_results)
                  refseq_sequences = fetch_refseq_sequences(accession_numbers)
                  refseq_sequences = sequences_decode(refseq_sequences)
                  refseq_sequences['gene_name'] = [re.sub('\).*', '', re.sub('.*\(', '', x)).upper() for x in refseq_sequences['name']]
                  if len(refseq_sequences['sequences']) > 0:
                      word_counts = Counter(refseq_sequences['gene_name'])
                      df = pd.DataFrame({'Word': word_counts.keys(), 'Count': word_counts.values()})
                      df = df.sort_values('Count', ascending = False)
                      df = df.reset_index()
                      if max(df['Count']) > min(df['Count']):
                          gen = df['Word'][0]
                      elif len(df['Count']) == 1:
                          gen = df['Word'][0]
                      else: 
                          gen = gene_name
                        
                        
                      refseq_sequences = pd.DataFrame(refseq_sequences)
                      refseq_sequences = refseq_sequences[refseq_sequences['gene_name'] == gen].to_dict(orient = 'list')
                    
                  else:
                      refseq_sequences = None
                     
                    
                    
            elif species.lower() == 'both':
                query1 = f"{gene_name}[Gene Name] AND Homo sapiens[Organism]"
                query2 = f"{gene_name}[Gene Name] AND Mus musculus[Organism]"
        
                accession_numbers1 = search_refseq(query1, max_results=max_results)
                accession_numbers2 = search_refseq(query2, max_results=max_results)
                
                accession_numbers = accession_numbers1 + accession_numbers2
        
                
                refseq_sequences = fetch_refseq_sequences(accession_numbers)
                refseq_sequences = sequences_decode(refseq_sequences)
                
                refseq_sequences['gene_name'] = [re.sub('\).*', '', re.sub('.*\(', '', x)).upper() for x in refseq_sequences['name']]
                if len(refseq_sequences['sequences']) > 0:
                    word_counts = Counter(refseq_sequences['gene_name'])
                    df = pd.DataFrame({'Word': word_counts.keys(), 'Count': word_counts.values()})
                    df = df.sort_values('Count', ascending = False)
                    df = df.reset_index()
                    if max(df['Count']) > min(df['Count']):
                        gen = df['Word'][0]
                    elif len(df['Count']) == 1:
                        gen = df['Word'][0]
                    else: 
                        gen = gene_name
                       
                       
                    refseq_sequences = pd.DataFrame(refseq_sequences)
                    refseq_sequences = refseq_sequences[refseq_sequences['gene_name'] == gen].to_dict(orient = 'list')
                   
                else:
                    refseq_sequences = None
                    
                    
            elif species.lower() == 'both2':
                query1 = f"{gene_name}[Gene Name] AND Homo sapiens[Organism]"
                query2 = f"{gene_name}[Gene Name] AND Rattus norvegicus[Organism]"
        
                accession_numbers1 = search_refseq(query1, max_results=max_results)
                accession_numbers2 = search_refseq(query2, max_results=max_results)
                
                accession_numbers = accession_numbers1 + accession_numbers2
        
                
                refseq_sequences = fetch_refseq_sequences(accession_numbers)
                refseq_sequences = sequences_decode(refseq_sequences)
                
                refseq_sequences['gene_name'] = [re.sub('\).*', '', re.sub('.*\(', '', x)).upper() for x in refseq_sequences['name']]
                if len(refseq_sequences['sequences']) > 0:
                    word_counts = Counter(refseq_sequences['gene_name'])
                    df = pd.DataFrame({'Word': word_counts.keys(), 'Count': word_counts.values()})
                    df = df.sort_values('Count', ascending = False)
                    df = df.reset_index()
                    if max(df['Count']) > min(df['Count']):
                        gen = df['Word'][0]
                    elif len(df['Count']) == 1:
                        gen = df['Word'][0]
                    else: 
                        gen = gene_name
                       
                       
                    refseq_sequences = pd.DataFrame(refseq_sequences)
                    refseq_sequences = refseq_sequences[refseq_sequences['gene_name'] == gen].to_dict(orient = 'list')
                   
                else:
                    refseq_sequences = None
                    
                    
            elif species.lower() == 'multi':
                query1 = f"{gene_name}[Gene Name] AND Homo sapiens[Organism]"
                query2 = f"{gene_name}[Gene Name] AND Rattus norvegicus[Organism]"
                query3 = f"{gene_name}[Gene Name] AND Mus musculus[Organism]"
    
        
                accession_numbers1 = search_refseq(query1, max_results=max_results)
                accession_numbers2 = search_refseq(query2, max_results=max_results)
                accession_numbers3 = search_refseq(query3, max_results=max_results)
    
                accession_numbers = accession_numbers1 + accession_numbers2 + accession_numbers3
        
                
                refseq_sequences = fetch_refseq_sequences(accession_numbers)
                refseq_sequences = sequences_decode(refseq_sequences)
                
                refseq_sequences['gene_name'] = [re.sub('\).*', '', re.sub('.*\(', '', x)).upper() for x in refseq_sequences['name']]
                if len(refseq_sequences['sequences']) > 0:
                    word_counts = Counter(refseq_sequences['gene_name'])
                    df = pd.DataFrame({'Word': word_counts.keys(), 'Count': word_counts.values()})
                    df = df.sort_values('Count', ascending = False)
                    df = df.reset_index()
                    if max(df['Count']) > min(df['Count']):
                        gen = df['Word'][0]
                    elif len(df['Count']) == 1:
                        gen = df['Word'][0]
                    else: 
                        gen = gene_name
                       
                       
                    refseq_sequences = pd.DataFrame(refseq_sequences)
                    refseq_sequences = refseq_sequences[refseq_sequences['gene_name'] == gen].to_dict(orient = 'list')
                   
                else:
                    refseq_sequences = None
                    
                    
            else:
                  query = f"{gene_name}[Gene Name] AND {species}[Organism]"
                  accession_numbers = search_refseq(query, max_results=max_results)
                  refseq_sequences = fetch_refseq_sequences(accession_numbers)
                  refseq_sequences = sequences_decode(refseq_sequences)
                  refseq_sequences['gene_name'] = [re.sub('\).*', '', re.sub('.*\(', '', x)).upper() for x in refseq_sequences['name']]
                  if len(refseq_sequences['sequences']) > 0:
                      word_counts = Counter(refseq_sequences['gene_name'])
                      df = pd.DataFrame({'Word': word_counts.keys(), 'Count': word_counts.values()})
                      df = df.sort_values('Count', ascending = False)
                      df = df.reset_index()
                      if max(df['Count']) > min(df['Count']):
                          gen = df['Word'][0]
                      elif len(df['Count']) == 1:
                          gen = df['Word'][0]
                      else: 
                          gen = gene_name
                        
                        
                      refseq_sequences = pd.DataFrame(refseq_sequences)
                      refseq_sequences = refseq_sequences[refseq_sequences['gene_name'] == gen].to_dict(orient = 'list')
                    
                  else:
                      refseq_sequences = None
                     
            
            return refseq_sequences
              
        except:
    
            print('\nSomething went wrong. This function will be repeated up to 3 times')
            time.sleep(30)
            
            if n == 3:
                print('\nSomething went wrong - get_sequences_gene. This query is unable to return. Try again later or contact us!')                
                return None







def get_sequences_accesion(accesion_list:list):
    
    """
    This function gets sequences from NCBI database based on accession numbers
        
    Args:
       accesion_list (list) - accession numbers or number of searching sequences inside list eg. ['X81403.1', 'KJ890665.1']; ['KJ890665.1']
       

    Returns:
        dict: Dictionary including all sequences from the provided query, their names, features, and IDs
       
    """
    
    
    try:
        
        refseq_sequences = fetch_refseq_sequences(accesion_list)
        refseq_sequences = sequences_decode(refseq_sequences)
        refseq_sequences['gene_name'] = [re.sub('\).*', '', re.sub('.*\(', '', x)).upper() for x in refseq_sequences['name']]
        if len(refseq_sequences['sequences']) > 0:
            word_counts = Counter(refseq_sequences['gene_name'])
            df = pd.DataFrame({'Word': word_counts.keys(), 'Count': word_counts.values()})
            df = df.sort_values('Count', ascending = False)
            df = df.reset_index()
                
                
            refseq_sequences = pd.DataFrame(refseq_sequences)
            refseq_sequences = refseq_sequences.to_dict(orient = 'list')
            
        else:
            refseq_sequences = None
         
                 
        
        return refseq_sequences
    
    except:

        print('\nSomething went wrong - get_sequences_accesion. Check the input or contact us!')
        return None




def generate_fasta_string(data_dict:dict):
    
    """
    This function trnasform dictionaries from get_sequences_accesion() or get_sequences_gene() into FASTA format.
        
    Args:
       data_dict (dict) - dictionaries from get_sequences_accesion() or get_sequences_gene()
       

    Returns:
        txt: FASTA format of input dictionary
       
    """
    
    try:
        
        fasta_string = ""
        names = data_dict["name"]
        sequences = data_dict["seq"]
        for name, sequence in zip(names, sequences):
            fasta_string += f">{re.sub(' ', '_', name)}\n{sequence}\n"
        
    
    except:
        
        print('\nSomething went wrong - generate_fasta_string. Check the input or contact us!')
        return None

        
    return fasta_string


###############################################################################


# alignments


def MuscleMultipleSequenceAlignment(fasta_string:str, gapopen = 10, gapextend = 0.5, output = None, source = _cwd):
    
    """
    This function conducts alignments of sequences provided in FASTA format
    
    Args:
       fasta_string (str\FASTA) - sequences provided in FASTA format from generate_fasta_string() or loaded from external sources
       gapopen (int | float) -  description under the link provided below. Default: 10 
       gapextend (int | float) - description under the link provided below. Default:  0.5 
       output (str | None) - path to the TMP alignment file. If None then the current working directory and the TMP file are removed. Default: None 
       
       More information in the source code of the primary function authors:
           - https://www.drive5.com/muscle/

    Returns:
        txt: FASTA format of input dictionary
       
    """
    
    
    try:
        # Write the sequences to the FASTA file
        if source == None:
            source = os.getcwd()
            
        random_prefix = random_name(length=30)
        input_file = os.path.join(source,  'tmp', random_prefix + '_tmp_fasta.fasta')
        with open(input_file, "w") as fasta_file:
                fasta_file.write(fasta_string)
    
        system = platform.system()
        
        
        
        if system == "Windows":
            print("\nWindows operating system")
            muscle_path = os.path.join(source, 'muscle/windows/')
            muscle_executable = 'muscle3.8.31_i86win32.exe'
    
    
        elif system == "Linux":
            print("\nLinux operating system")
            muscle_path = os.path.join(source, 'muscle/linux/')
            muscle_executable = './muscle'
    
        if output != None: 
            
            output_file = os.path.join(source, output)
            if not output_file.endswith('fasta'):
                output_file = output_file + '_out.fasta'
    
                
        else:
            
            random_prefix = random_name(length=30)
            output_file = os.path.join(source, 'tmp', random_prefix + '_tmp_alignment.fasta')

         
        muscle_cmd = [muscle_executable, '-in', input_file, '-out', output_file, '-gapopen', str(gapopen), '-gapextend', str(gapextend)]
        
        # Run the MUSCLE command
        try:
            
            if system == "Windows":
                subprocess.run(muscle_cmd, cwd=muscle_path, shell= True)

        
        
            elif system == "Linux":
                subprocess.run(muscle_cmd, cwd=muscle_path, shell= False)

    
            # Read the alignment from the file
            alignment = AlignIO.read(output_file, "fasta")
            
            os.remove(input_file)
            
            if output == None: 
                os.remove(output_file)
            else:
                print("\nMUSCLE alignment completed successfully. Output saved to", output_file)
    
            
            return alignment
    
    
        except subprocess.CalledProcessError as e:
            print("\nError running MUSCLE:", e)
            
            return None
        
    except:
        
        print('\nSomething went wrong - MuscleMultipleSequenceAlignment. Check the input or contact us!')
        return None

    
    


def decode_alignments(alignment_file):
    
        
    """
    This function decodes the alignment file from MuscleMultipleSequenceAlignment() and converts it to FASTA-ALIGNMENT
    
    Args:
       alignment_file (Bio.Align.MultipleSeqAlignment class) - the output file from MuscleMultipleSequenceAlignment()
      

    Returns:
        txt: FASTA-ALIGNMENT format of input file
       
    """
    try:
        
        seq_list = []
        name = []
        for n, i in enumerate(alignment_file): 
            name.append(alignment_file[n].id)
            seq_list.append(str(alignment_file[n]._seq._data.decode('utf-8')))
            
        
        name_len = len(max(name, key=len))
        
        padded_list = [word.ljust(name_len) + ' | ' for word in name]
        
        txt = ''
        for j in range(len(seq_list)):
            txt += padded_list[j] +  seq_list[j] + '\n'
            
        return txt
    
    except:
        
        print('\nSomething went wrong - decode_alignments. Check the input or contact us!')
        return None




def write_fasta(fasta_string:str, path = None, name:str = 'fasta_file'):
    
    """
    This function saves into FASTA *.fasta
    
    Args:
        fasta_string (str/FASTA) - sequences provided in FASTA format from generate_fasta_string() or loaded from external sources
        path (str | None) - the path to save. If None save it to the current working directory. Default: None
        name (str) - the name of the saving file. Default: 'fasta_file'

    """
    try:
        
        if path == None:
            path = os.getcwd()
            
        path = os.path.join(path, name + '.fasta')
        with open(path, 'w') as file:
            file.write(fasta_string + '\n')
            
    except:
        
        print('\nSomething went wrong - write_fasta. Check the input or contact us!')

        
def write_alignments(decoded_alignment_file:str, path = None, name:str = 'alignments_file'):
    
    """
    This function saves into FASTA-ALIGNMENT *.align
    
    Args:
       decoded_alignment_file (str/FASTA) - sequences provided in FASTA format from decode_alignments()
       path (str | None) - the path to save. If None save it to the current working directory. Default: None
       name (str) - the name of the saving file. Default: 'alignments_file'

       
    """
    try:
        if path == None:
            path = os.getcwd()
        
        path = os.path.join(path, name + '.align')
        with open(path, 'w') as file:
            file.write(decoded_alignment_file + '\n')
            
    except:
        
        print('\nSomething went wrong - write_alignments. Check the input or contact us!')






def ExtractConsensuse(alignment_file, refseq_sequences = None):
    
            
    """
    This function extracts consensus fragments of sequences alignments from alignment_file obtained in the MuscleMultipleSequence Alignment() function
    
    Args:
       alignment_file (Bio.Align.MultipleSeqAlignment class) - the output file from MuscleMultipleSequenceAlignment()
       refseq_sequences (dict | None) - dictionary obtained from get_sequences_gene() or get_sequences_accesion(), which add additional information to results. If None results will be reduced to only consensus sequences.
    
    Returns:
        dict: The dictionary containing consensus fragments
       
    """
    

    try:
    
        def find_string_range(main_string, substring):
            start = main_string.find(substring[0:1000])
            end = start + len(substring)
            if start != -1:
                return (start, end)
            else:
                return None
        
        seq_list = []
        for n, i in enumerate(alignment_file): 
            seq_list.append(str(alignment_file[n]._seq._data.decode('utf-8')))
        
                    
        con_tmp = ""
        consesnuses = []
        for j, i in enumerate(seq_list[0]):
            nuc = []
            for c in range(len(seq_list)):
                nuc.append(seq_list[c][j])
                
            if len(set(nuc)) == 1 and '-' not in nuc and j != len(seq_list[0]) - 1:
                con_tmp = con_tmp + str(seq_list[c][j]) 
            else:
                if len(con_tmp) > 30:
                     consesnuses.append(con_tmp)
                     con_tmp = ""
                else:
                    con_tmp = ""
                    
    #
        # Create a dictionary for the consensus sequence
    
        if refseq_sequences != None:
    
            
            
            consensuse_dictionary = {'sequence': [], 'range_to_ref':[], 'side':[]}
            range_3 = range(refseq_sequences['features'][0]['CDS']['stop'], int(refseq_sequences['features'][0]['CDS']['stop']*2))
            range_5 = range(int(refseq_sequences['features'][0]['CDS']['start']/2), refseq_sequences['features'][0]['CDS']['start'])
            range_cds = range(refseq_sequences['features'][0]['CDS']['start'], refseq_sequences['features'][0]['CDS']['stop'])
            
            
            for con in consesnuses:
                consensuse_dictionary['sequence'].append(con)
                rang = find_string_range(refseq_sequences['seq'][0], str(con))
                consensuse_dictionary['range_to_ref'].append(rang)
                
                side = []
                
                if rang[-1] >= range_5[0] and range_5[-1] >= rang[0]:
                    side.append('5`UTR')
                if rang[-1] >= range_cds[0] and range_cds[-1] >= rang[0]:
                    side.append('CDS')
                if rang[-1] >= range_3[0] and range_3[-1] >= rang[0]:
                    side.append('3`UTR')
                    
                consensuse_dictionary['side'].append(','.join(side))
            
                
    
        else:
            consensuse_dictionary = {'sequence': [], 'range_to_ref':[], 'side':[]}
            for con in consesnuses:
                consensuse_dictionary['sequence'].append(con)
                consensuse_dictionary['range_to_ref'].append(None)
                consensuse_dictionary['side'].append(None)
    
        
    
        return consensuse_dictionary
    
    except:
        
        print('\nSomething went wrong - ExtractConsensuse. Check the input or contact us!')
        return None




# graph structure

def DisplayAlignment(alignment_file, color_scheme:str = "Taylor", wrap_length:int = 80, show_grid:bool = True, show_consensus:bool = True):
    
    
    """
    This function makes the graphical presentation of the alignments
    
    Args:
       alignment_file (Bio.Align.MultipleSeqAlignment class) - the output file from MuscleMultipleSequenceAlignment()
       color_scheme (str) - color palette for plotting. Default: "Taylor"
       wrap_length (int) - max number of nucleotides shown in a row on the graph. Default: 80 
       show_grid (bool) - show the grid on the graph. Default: True
       show_consensus (bool) - highlight the consensus sequences. Default: True
       
       More information in the source code of the primary function authors:
           - https://pypi.org/project/pyMSAviz/

    Returns:
        graph: The graphical presentation of sequences alignments
               
       
    """
    
    try:

        mv_plot = MsaViz(alignment_file, color_scheme=color_scheme, wrap_length=wrap_length, show_grid=show_grid, show_consensus=show_consensus)
        
        
        return mv_plot
    
    except:
        
        print('\nSomething went wrong - Displayalignment. Check the input or contact us!')
        return None



###############################################################################

#Sequences adjustment

def load_sequence():
        
    """
    This function makes it easy to load the genetic sequences to variable
    
    
    Returns:
        str: Input sequence in a variable
       
    """
    
    try:
        check = True
        while (check == True):
            sequence = input('\n Enter sequence: ')
            
            if (len(sequence) < 3):
                print("\n Sequence not provided. Sequence length equals 0")
                
            else:
                check = False
       
        return sequence  
    
    except:
        
        print('\nSomething went wrong - load_sequence. Check the input or contact us!')
        return None




def clear_sequence(sequence:str, upac_code:list() = ['A','C','T','G','N','M','R','W','S','Y','K','V','H','D','B','U', 'Ψ']):
    
        
    """
    This function clear sequence from special characters, spaces, numbers that may be in the sequence when copied from external sources.
    
    Args:
        sequence (str) - nucleotide sequence provided in UPAC code
        upac_code (list) - list of nucleotides in which the sequence is encoded. Default: ['A','C','T','G','N','M','R','W','S','Y','K','V','H','D','B','U', 'Ψ']

    Returns:
        str: The genetic sequence after clearing
       
    """
    try:
        
        tmp_sequence = list(sequence)
        tmp_sequence = ''.join(c.upper() for c in tmp_sequence if c.isalpha() and c.upper() in upac_code)
        
        sequence = tmp_sequence.upper()
        
        return sequence
    
    except:
        
        print('\nSomething went wrong - clear_sequence. Check the input or contact us!')
        return None



    
    
    
def check_coding(sequence:str):
    
    
    """
    This function checks that the input sequence belongs to the (CDS) coding sequence. Checkpoints include the start with ATG and include 3-nucleotide repeats.
    
    Args:
        sequence (str) - nucleotide sequence provided in UPAC code

    Returns:
        bool: True/False
       
    """

    try:
        tmp_seq = [sequence[y:y+3] for y in range(0, len(sequence), 3)]
        
        if len(tmp_seq[-1]) == 3 and tmp_seq[0].upper() == 'ATG':
            dec = True
        else:
            dec = False
            
        return dec
    
    except:
        
        print('\nSomething went wrong - check_coding. Check the input or contact us!')
        return None




def check_upac(sequence:str, upac_code:list() = ['A','C','T','G','N','M','R','W','S','Y','K','V','H','D','B','U', 'Ψ']):
    
    """
    This function checks that the input sequence elements are included in UPAC code.
    
    Args:
        sequence (str) - nucleotide sequence provided in UPAC code
        upac_code (list) - list of nucleotides in which the sequence is encoded. Default: ['A','C','T','G','N','M','R','W','S','Y','K','V','H','D','B','U', 'Ψ']

    Returns:
        bool: True/False
       
    """
    
    try:
        
        dec = True
        for h in sequence:
            if h.upper() not in upac_code:
                dec = False
                print('\nIn sequence is the letter not included in UPAC code for DNA / RNA. UPAC: ')
                print(upac_code)
    
                break
            
        return dec
        
    except:
        
        print('\nSomething went wrong with UPAC code. Check the input or contact us!')
        return None
    


    
    

def reverse(sequence:str):
    
            
    """
    This function reverses the input genetic sequence from 5' -> 3' to 3' -> 5' and opposite.
    
    Args:
        sequence (str) - nucleotide sequence provided in UPAC code

    Returns:
        str: The genetic sequence after reversing
       
    """
    
    try:
        
        reversed_sequence = ''
    
        for character in reversed(sequence.upper()):
            reversed_sequence += character
    
        return reversed_sequence
    
    except:
        
        print('\nSomething went wrong - reverse. Check the input or contact us!')
        return None



 
def complement(sequence:str):
    
    """
    This function makes a complementary sequence to the input genetic sequence on the nucleotide pairs from the extended UPAC code.
    
    Args:
        sequence (str) - nucleotide sequence provided in UPAC code

    Returns:
        str: The complementary sequence
       
    """
    
    try:
        complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'R':'Y', 'Y':'R', 'S':'S', 'W':'W', 'K':'M', 'M':'K', 'B':'V', 'V':'B', 'D':'H', 'H':'D', 'N':'N', 'U':'A'}
        complement_seq = ''
    
        for nucleotide in sequence.upper():
            complement_seq += complement[nucleotide]
    
        return complement_seq
    
    except:
        
        print('\nSomething went wrong - complement. Check the input or contact us!')
        return None




def dna_to_rna(sequence:str, enrichment:bool = False):
    
        
    """
    This function changes the sequence from DNA format to RNA.
    
    Args:
        sequence (str) - nucleotide sequence provided in UPAC code
        enrichment (bool) - If True, the nucleotides in the RNA sequence instead of uracil (U) will be replaced with pseudouridine (Ψ) (True/False). Default: False

    Returns:
        str: The RNA sequence
       
    """
    
    try:
        complement = {'T': 'U'}
        if enrichment == True:
            complement = {'T': 'Ψ'}
         
        complement_seq = ''
        
        for nucleotide in sequence.upper():
            if nucleotide in complement.keys():
                complement_seq += complement[nucleotide]
            else:
                complement_seq += nucleotide
                
        
        return complement_seq
    
    except:
        
        print('\nSomething went wrong - dna_to_rna. Check the input or contact us!')
        return None



def rna_to_dna(sequence:str):
    
            
    """
    This function changes the sequence from RNA format to DNA.
    
    Args:
        sequence (str) - nucleotide sequence provided in UPAC code

    Returns:
        str: The DNA sequence
       
    """
    
    try:

        complement = {'U': 'T', 'Ψ' : 'T'}
         
        complement_seq = ''
        
        for nucleotide in sequence.upper():
            if nucleotide in complement.keys():
                complement_seq += complement[nucleotide]
            else:
                complement_seq += nucleotide
                
        
        return complement_seq
    
    except:
        
        print('\nSomething went wrong - rna_to_dna. Check the input or contact us!')
        return None
        
        
        
def seuqence_to_protein(sequence:str, metadata):
    
                
    """
    This function changes the sequence from (CDS) RNA or DNA format to protein sequence.
    
    Args:
        sequence (str) - nucleotide sequence provided in UPAC code
        metadata (dict) - set of metadata loaded vie load_metadata()

    Returns:
        str: The protein sequence
       
    """
    
    
    codons = metadata['codons']
    
    if 'U' in sequence or 'Ψ' in sequence:
        sequence = rna_to_dna(sequence)
        
    dec = check_coding(sequence)
    dec2 = check_upac(sequence)
    
    if dec and dec2:
        

        seq_codon = [sequence[y:y+3] for y in range(0, len(sequence), 3)]
        
        prot_seq = []
        for element in seq_codon:
            tmp = codons['Amino acid'][codons['Triplet'] == element.upper()]
            tmp = tmp.reset_index()
            prot_seq.append(tmp['Amino acid'][0])
            
        
        prot_seq = [x for x in prot_seq if x != '*']
        prot_seq = ''.join(prot_seq)
        
        return prot_seq
    
    else:
        
        print("\nWrong sequence. The condition of three-nucleotide repeats in the coding sequence is not met.")
        return None

   

###############################################################################



#RNAi selection
#find RNAi


def FindRNAi(sequence:str, metadata, length:int = 23, n:int = 200, max_repeat_len:int = 3, max_off:int = 1, species:str = 'human', output = None, database_name:str = "refseq_select_rna",  evalue = 1e-3, outfmt =  5, word_size:int = 7, max_hsps:int = 20, reward = 1, penalty = -3, gapopen = 5, gapextend = 2, dust = "no", extension:str = 'xml', source = _cwd):

        
    """
    This function predicts the set of RNAi's, based on properties defined by the user and provided target sequence. Obtained set of RNAi can be used to prepare siRNA, shRNA, etc.
    
    Args:
       sequence (str) - nucleotide sequence provided in UPAC (ATGC) code that will be used the for RNAi sequence estimation
       metadata (dict) - set of metadata loaded vie load_metadata()
       length (int) - length of searching RNAi sequences. Default: 23
       n (int) - maximal number of selected RNAi. Default: 200
       max_repeat_len (int) - maximal number of repeat the same nucleotide in a row eg. AAA. Default: 3
       max_off (int) - maximal number of patrialy off-targeted genes by predicted RNAi. Default: 1
           *sometimes two genes are such similar that is difficult to create RNAi fully specific to one target eg. Human SMN1 & SMN2 genes
       species (str) - specie for which the gene sequence is searching (human / mouse / rat / both* / both2* / multi* ). Default: 'human'
        
            *both - gene sequences for Mus musculus and Homo sapiens
            *both2 - gene sequences for Rattus norvegicus and Homo sapiens
            *multi - gene sequences for Mus musculus, Rattus norvegicus, and Homo sapiens
            
       output (str) - path to the TMP alignment file. If None then the current working directory and the TMP file are removed. Default: None 
       database_name (str) - NCBI database on which the algorithm searching RNAi is based. Default: "refseq_select_rna" (other databases are not installed, if you need to install another, contact us!)
       evalue (int | float) - description under the link provided below. Default: 1e-3
       outfmt (int | float) - description under the link provided below. Default: 5
       word_size (int) - description under the link provided below. Default: 7
       max_hsps (int) - description under the link provided below. Default: 0
       reward (int | float) - description under the link provided below. Default: 1
       penalty (int | float) - description under the link provided below. Default: -3
       gapopen (int | float) - description under the link provided below. Default: 5
       gapextend (int | float) - description under the link provided below. Default: 2
       dust (str) - description under the link provided below. Default: "no"
       extension (str) - extension of TMP file readable for application. Default: 'xml'
       
       
       Link to variables explanation:
       https://www.ncbi.nlm.nih.gov/books/NBK279684/table/appendices.T.options_common_to_all_blast/
      

    Returns:
        DataFrame: Data frame containing predicted RNAi sequence (sense / antisense), target, scores and statistics.
       
    """
    
    try:
        # Write the sequences to the FASTA file
        if source == None:
            source = os.getcwd()
            
    
        system = platform.system()
        
    
        if system == "Windows":
            print("\nWindows operating system")
            blast_executable = os.path.join(source, 'blast/windows/ncbi-blast-2.14.1+/bin/')
            command = "blastn.exe"
    
    
        elif system == "Linux":
            print("\nLinux operating system")
            blast_executable = os.path.join(source, 'blast/linux/ncbi-blast-2.14.1+/bin/')
            command = "./blastn"
    
    
        if output != None: 
            output_file = os.path.join(source, output)
            if not output_file.endswith(extension):
                output_file = output_file + '_blast_out.' + extension
    
                
        else:
            
            random_prefix = random_name(length=30)
            output_file = os.path.join(source, 'tmp', random_prefix + '_tmp_blast.' + extension)
            

        def rnai_scroing_base(sequence):
            
            sequence = reverse(sequence = complement(sequence = sequence))
            
            scoring = metadata['rnai']
            
            score = 0
            
            for i in sequence[:3]:
                if i in ['G', 'C']:
                    score = score + 1
                elif i in ['A', 'T']:
                    score = score - 1
            
            for i in sequence[-3:]:
                if i in ['G', 'C']:
                    score = score - 1
                elif i in ['A', 'T']:
                    score = score + 1
    
            
            for j in scoring.index:
                if scoring['position'][j] != 'last':
                    if sequence[scoring['position'][j]] == scoring['element'][j]:
                        if '+' in scoring['operation'][j]:
                            score = score + float(scoring['score'][j])
                        elif '-' in scoring['operation'][j]:
                            score = score - float(scoring['score'][j])
                elif scoring['position'][j] == 'last':
                    if sequence[-1] == scoring['element'][j]:
                        if '+' in scoring['operation'][j]:
                            score = score + float(scoring['score'][j])
                        elif '-' in scoring['operation'][j]:
                            score = score - float(scoring['score'][j])
                            
                
            
            return score, sequence
        
        
        def find_self_complementarity(sequence, min_length=3):
            complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
            self_complementary_regions = []
    
            for i in range(len(sequence) - min_length + 1):
                for j in range(i + min_length, len(sequence) + 1):
                    subsequence = sequence[i:j]
                    reverse_complement = ''.join(complement[base] for base in subsequence[::-1])
                    
                    if subsequence == reverse_complement:
                        self_complementary_regions.append(subsequence)
    
            return self_complementary_regions
    
        def repeat_scoring(seq, max_repeat_len):
            
            repeat_list = []
            
            repeat = ''
     
            for n, s in enumerate(seq):
                if n == 0 and seq[n+1] == s:
                    repeat = repeat + s
                elif n == len(seq) - 1 and seq[n-1] == s:
                    repeat = repeat + s
                elif n == len(seq) - 1:
                    break
                elif seq[n+1] == s or seq[n-1] == s:
                    repeat = repeat + s
                    
                if repeat[:1] != repeat[-1:]:
                    if len(repeat[0:-1]) > max_repeat_len:
                        repeat_list.append(repeat[0:-1])
                        repeat = repeat[-1:]
                    else:
                        repeat = repeat[-1:]
                elif n == len(seq) - 1:
                    if len(repeat) > max_repeat_len:
                        repeat_list.append(repeat)
                        
                        
                full_len = 0
                
                for i in repeat_list:
                    full_len = full_len + len(i)
                    
                pct = round(full_len / len(seq), 2)
                    
                            
            return repeat_list, pct
         
        if len(sequence) > length:
            predicted_rnai = []
            
            br = False
            while(True):
    
                if br == True or len(sequence) < length:
                    break
                else:
                    t = 0
                    for x in range(int(len(sequence)/length)):
                        if len(sequence[t:t+length]) == length:
                            predicted_rnai.append(sequence[t:t+length])
                        t += length
                        
                        predicted_rnai = list(set(predicted_rnai))
                        if len(predicted_rnai) >= n or len(sequence) < length:
                            br = True
                            break
                
                    sequence = sequence[1:]
        
            # def additional_selection_of_the_best_rani()
            predicted_rnai = [reverse(sequence = complement(sequence = x)) for x in predicted_rnai]
            fasta_string = ""
            names = ['RNAi'] * len(predicted_rnai)
            unique_names = [f'{name}_{i}' for i, name in enumerate(names, start=1)]
            for name, seq in zip(unique_names, predicted_rnai):
                fasta_string += f">{re.sub(' ', '_', name)}\n{seq}\n"
            
            random_prefix = random_name(length=30)

            input_file = os.path.join(source,  'tmp', random_prefix + '_tmp_rnai.fasta')

            with open(input_file, "w") as fasta_file:
                    fasta_file.write(fasta_string)
           
            command_list = [command, "-query", input_file, "-db", database_name, "-out", output_file, "-evalue", str(evalue),  "-outfmt", str(outfmt) , "-word_size" , str(word_size), "-max_hsps", str(max_hsps), "-reward" , str(reward), "-penalty", str(penalty), "-gapopen", str(gapopen), "-gapextend", str(gapextend),  "-dust",  str(dust)]        
            
            if system == "Windows":
                subprocess.run(command_list, cwd=blast_executable, shell=True)


            elif system == "Linux":
                subprocess.run(command_list, cwd=blast_executable, shell=False)

            
            
            try:
                os.remove(input_file)
                print(f'{input_file} successfully deleted.')
            except OSError as e:
                print(f'Error: {input_file} - {e.strerror}')
                
             
            tree = ET.parse(output_file)
            
            try:
                os.remove(output_file)
                print(f'{output_file} successfully deleted.')
            except OSError as e:
                print(f'Error: {output_file} - {e.strerror}')
             
            root = tree.getroot()
            
            # Create lists to store data
            query_ids = []
            subject_ids = []
            e_values = []
            bit_scores = []
            alignment_lengths = []
            query_sequences = []
            subject_sequences = []
         
            # Iterate through the XML tree and extract relevant data
            for iteration in root.findall(".//Iteration"):
                query_id = iteration.find(".//Iteration_query-def").text
                for hit in iteration.findall(".//Hit"):
                    subject_id = hit.find(".//Hit_def").text
                    e_value = hit.find(".//Hsp_evalue").text
                    bit_score = hit.find(".//Hsp_bit-score").text
                    alignment_length = hit.find(".//Hsp_align-len").text
                    query_sequence = hit.find(".//Hsp_qseq").text
                    subject_sequence = hit.find(".//Hsp_hseq").text
            
                    query_ids.append(query_id)
                    subject_ids.append(subject_id)
                    e_values.append(float(e_value))
                    bit_scores.append(float(bit_score))
                    alignment_lengths.append(int(alignment_length))
                    query_sequences.append(query_sequence)
                    subject_sequences.append(subject_sequence)
            
            # Create a DataFrame
            data = {
                'target': subject_ids,
                'e-value': e_values,
                'bit_score': bit_scores,
                'alignment_length': alignment_lengths,
                'target_seq': subject_sequences,
                'RNAi_name':query_ids,
            }
            
            df = pd.DataFrame(data)
            
            name_mapping = dict(zip(unique_names, predicted_rnai))
            df['RNAi_seq'] = df['RNAi_name'].map(name_mapping)
            
            df['target_gene_name'] = [re.sub('\).*', '', re.sub('.*\(', '', x)).upper() for x in df['target']]
            
            df['species'] = [' '.join(re.sub('PREDICTED: ', '', x).split()[:2]) for x in df['target']]
            
            
            try:
                if species.lower() == 'human':
                    df = df[df['species'] == "Homo sapiens"]
                elif species.lower() == 'mouse':
                    df = df[df['species'] == "Mus musculus"]
                elif species.lower() == 'rat':
                    df = df[df['species'].isin(["Rattus norvegicus"])]
                elif species.lower() == 'both':
                    df = df[df['species'].isin(["Mus musculus","Homo sapiens"])]
                elif species.lower() == 'both2':
                    df = df[df['species'].isin(["Rattus norvegicus","Homo sapiens"])]
                elif species.lower() == 'multi':
                    df = df[df['species'].isin(["Mus musculus", "Rattus norvegicus","Homo sapiens"])]
                    
            except:
                None
            
            df = df.groupby(['RNAi_name', 'RNAi_seq'])[['target', 'e-value', 'bit_score', 'alignment_length', 'target_seq', 'target_gene_name', 'species']].agg(list).reset_index()
    
            df['specificity'] = None        
            df['complemenatry_regions'] = None
            df['complemenatry_pct'] = None
            df['RNAi_sense'] = None
            df['repeated_motif'] = None
            df['repeated_motif_pct'] = None
            df['score'] = None
            df['GC%'] = None
           
    
           
            for i in df.index:
                df['specificity'][i] = len(df['target_gene_name'][i])
                df['complemenatry_regions'][i] = list(set(find_self_complementarity(df['RNAi_seq'][i], min_length=3)))
                amount = 0
                for l in df['complemenatry_regions'][i]:
                    amount = amount + len(l)
                
                try:
                    df['complemenatry_pct'][i] = amount/len(df['RNAi_seq'][i])
                except:
                    df['complemenatry_pct'][i] = 0
                    
                    
                df['RNAi_sense'][i] = rnai_scroing_base(df['RNAi_seq'][i])[1]
                df['score'][i] = rnai_scroing_base(df['RNAi_seq'][i])[0]
                
                df['repeated_motif'][i] = repeat_scoring(df['RNAi_seq'][i], max_repeat_len)[0]
                df['repeated_motif_pct'][i] = repeat_scoring(df['RNAi_seq'][i], max_repeat_len)[1]
                df['GC%'][i] = round(df['RNAi_seq'][i].count('C') + df['RNAi_seq'][i].count('G') / len(df['RNAi_seq'][i]) * 100, 2)
           
           
            
            df = df.sort_values(by=['specificity', 'repeated_motif_pct', 'complemenatry_pct', 'score'], ascending=[True, True, True, False])
            
            
            df = df.reset_index(drop=True)
            

            return df
        
        else:
            return pd.DataFrame()
        
    except:
        
        print('\nSomething went wrong - FindRNAi. Check the input or contact us!')
        return pd.DataFrame()
        

        

def loop_complementary_adjustment(RNAi_data:pd.DataFrame, loop_seq:str, min_length:int = 3):
    
    """
    This function takes output DataFrame from Find RNAi() or remove_specific_to_sequence() reducing the RNAi score on their complementarity to the provided loop sequence.
    It allows the choice of RNAi with better biological functionality.
    
    Args:
       RNAi_data (DataFrame) - data frame obtained in the FindRNAi() or remove_specific_to_sequence() function
       loop_seq (str) - sequence of the loop in the UPAC code for siRNA / shRNA creation
       min_length (int) - min value of loop complementary nucleotides. Default: 3
      

    Returns:
        DataFrame: Data frame containing predicted RNA sequence (sense / antisense), target, scores, and statistics corrected by reducing complementary to loop sequence.
       
    """
    
    try:
        
        def loop_complementary(sequence, loop_seq, min_length):
            complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
            complementary_regions = []
        
            for i in range(len(sequence) - len(loop_seq) + 1):
                subsequence = sequence[i:i+len(loop_seq)]
                reverse_complement = ''.join(complement[base] for base in subsequence[::-1])
        
                if reverse_complement == loop_seq:
                    complementary_regions.append((i, i+len(loop_seq)))
        
            return complementary_regions
    
        
        RNAi_data['sense_loop_complementary'] = None
        RNAi_data['sense_loop_complementary_pct'] = None
        RNAi_data['antisense_loop_complementary'] = None
        RNAi_data['antisense_loop_complementary_pct'] = None
        
        
        for i in RNAi_data.index:
            RNAi_data['sense_loop_complementary'][i] = list(set(loop_complementary(RNAi_data['RNAi_sense'][i],loop_seq, min_length)))
            amount = 0
            for l in RNAi_data['sense_loop_complementary'][i]:
                amount = amount + len(l)
                
            try:
                RNAi_data['sense_loop_complementary_pct'][i] = amount/len(RNAi_data['RNAi_seq'][i])
            except:
                RNAi_data['sense_loop_complementary_pct'][i] = 0
                
                
                
            RNAi_data['antisense_loop_complementary'][i] = list(set(loop_complementary(RNAi_data['RNAi_seq'][i],loop_seq, min_length)))
            amount = 0
            for l in RNAi_data['antisense_loop_complementary'][i]:
                amount = amount + len(l)
            
            try:
                RNAi_data['antisense_loop_complementary_pct'][i] = amount/len(RNAi_data['RNAi_seq'][i])
            except:
                RNAi_data['antisense_loop_complementary_pct'][i] = 0
                
                
        
        RNAi_data = RNAi_data.sort_values(by=['specificity', 'repeated_motif_pct', 'complemenatry_pct', 'antisense_loop_complementary_pct', 'sense_loop_complementary_pct',  'score'], ascending=[True, True, True,True,True, False])
    
    
        RNAi_data = RNAi_data.reset_index(drop=True)
            
        return RNAi_data
    
    except:
        
        print('\nSomething went wrong - loop_complementary_adjustment. Check the input or contact us!')
        return pd.DataFrame()




def remove_specific_to_sequence(RNAi_data:pd.DataFrame, sequences, min_length:int = 4):
    
    """
    This function takes output DataFrame from Find RNAi() or loop_complementary_adjustment() reducing the RNAi score on their complementarity to the provided external genetic sequence. eg sequence after codon optimization which is not included in NCBI ref_seq db.
    It allows the choice of RNAi with better biological functionality.
    
    Args:
       RNAi_data (DataFrame) - data frame obtained in the FindRNAi() or loop_complementary_adjustment() function
       sequences (list | str) - nucleotide sequence provided in UPAC code
       min_length (int) - min value of sequence complementary nucleotides. Default: 4
      

    Returns:
        DataFrame: Data frame containing predicted RNA sequence (sense / antisense), target, scores, and statistics corrected by reducing complementary to another sequence.
       
    """
    
    
    try:
        
        
        if not isinstance(sequences, list):
            sequences = [sequences]
            
        def complementary_seq(seq1, seq2, min_length):
            complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
            complementary_regions = []
        
            for i in range(len(seq1) - len(seq2) + 1):
                subsequence = seq1[i:i+len(seq2)]
                reverse_complement = ''.join(complement[base] for base in subsequence[::-1])
        
                if reverse_complement == seq2:
                    complementary_regions.append((i, i+len(seq2)))
        
            return complementary_regions
        
        inx_to_rm = []
        for s in RNAi_data.index:
            for seq in sequences:
                comp = complementary_seq(RNAi_data['RNAi_sense'][s], seq, min_length)
                if len(comp) > 0:
                    inx_to_rm.append(s)
                    break
                
                
        RNAi_data = RNAi_data.drop(inx_to_rm)
        
        RNAi_data = RNAi_data.reset_index(drop = True)
                    
    
        return RNAi_data
    
    except:
        
        print('\nSomething went wrong - remove_specific_to_sequence. Check the input or contact us!')
        return pd.DataFrame()
    
    
    

# prediction_structure

def predict_structure(sequence:str, height = None, width = None, len_factor:float = 0.028, show_plot:bool = True):
    
    """
    This function makes the graphical of genetic RNA or DNA sequences.
    
    Args:
       sequence (str) - nucleotide sequence provided in UPAC (ATGC) code 
       height (int | float | None) - height of the graph
       width (int | float | None) - height of the graph
       len_factor (float) - is the factor regulating/correcting structure shape depending on sequence length. If your predicted structure looks different than the user expects, regulate this value (0.001-0.1). Default: 0.028
       show_plot (bool) - if True the plot will be displayed, if False only the graph will be returned to the variable. Default: True
       
    Returns:
        Graph: Graphical presentation of secondary DNA or RNA structure
        DOT-graph: DOT presentation of secondary DNA or RNA structure

       
    """
    
    try:
    
        (s, mfe) = RNA.fold(sequence)
        
        pairs = RNA.ptable(s)
        
        pairs = [(i, pairs[i]) for i in range(1, len(pairs))]
        
        dot_bracket_structure = s
        
        
        #prepare pair dic
        
        initial_point = []
        pair = []
        
        
        for i, j in pairs:
            if j > 0:
                initial_point.append(i)
                pair.append(j)
            else:
                initial_point.append(i)
                pair.append(None)
            
        if len(sequence)*len_factor < 7:
            fc = 7
        else:
            fc = len(sequence)*len_factor
        

        w1 = [fc]* len(initial_point)
        
        
        l1 = [initial_point[i] for i in range(0, len(initial_point)-1, 1)]
        l2 = [initial_point[i+1] for i in range(0, len(initial_point)-1, 1)]
        w2 = [2]* len(l1)
        
        
        dict_of_pairs = {'points': initial_point + [1010101010, 101010], 'sequence':list(sequence) + ['5`', '3`']}
             
        
        dict_of_pairs = pd.DataFrame(dict_of_pairs)
        
        name_mapping = dict(zip(['A', 'T', 'U', 'Ψ', 'C', 'G', '5`', '3`'], ['blue', 'yellow', 'yellow', 'yellow', 'red', 'green', 'white', 'white']))

        default_color = 'orange'
        
        dict_of_pairs['color'] = dict_of_pairs['sequence'].map(lambda x: name_mapping.get(x, default_color))
                
        
        initial_point = initial_point + l1
        pair = pair + l2
        
        w = w1 + w2
        
        conection_df = pd.DataFrame({'nc1':initial_point + [101010, 1010101010], 'nc2':pair + [max(initial_point),1], 'weight':w + [2.5,2.5]})
        
        conection_df = conection_df.dropna()
        
        conection_df = conection_df.reset_index(drop = True)
        
        
        nucleotide_pairs = {'A': 'TUΨ', 'T': 'A', 'C': 'G', 'G': 'C', 'R':'Y', 'Y':'R', 'S':'S', 'W':'W', 'K':'M', 'M':'K', 'B':'V', 'V':'B', 'D':'H', 'H':'D', 'N':'N', 'U':'A'}
    
        
        G = nx.Graph()
        
        for i in dict_of_pairs.index:
            if dict_of_pairs['points'][i] == 1010101010:
                G.add_node(dict_of_pairs['points'][i], name = dict_of_pairs['sequence'][i], color=dict_of_pairs['color'][i])
            elif dict_of_pairs['points'][i] == 101010:
                G.add_node(dict_of_pairs['points'][i], name = dict_of_pairs['sequence'][i], color=dict_of_pairs['color'][i])
            else:
                G.add_node(dict_of_pairs['points'][i], name = dict_of_pairs['sequence'][i], color=dict_of_pairs['color'][i])
            
            
        for i in conection_df.index:
            if conection_df['weight'][i] == fc:
                if dict_of_pairs['sequence'][dict_of_pairs['points'] == conection_df['nc2'][i]][dict_of_pairs['sequence'][dict_of_pairs['points'] == conection_df['nc2'][i]].index[0]] in nucleotide_pairs[dict_of_pairs['sequence'][dict_of_pairs['points'] == conection_df['nc1'][i]][dict_of_pairs['sequence'][dict_of_pairs['points'] == conection_df['nc1'][i]].index[0]]]:
                    G.add_edge(conection_df['nc1'][i], conection_df['nc2'][i], weight= conection_df['weight'][i])
            else:
                G.add_edge(conection_df['nc1'][i], conection_df['nc2'][i], weight= conection_df['weight'][i])
    
        if  height == None or width == None:
            if len(sequence)/5 > 10:     
                fig = plt.figure(figsize=(len(sequence)/5, len(sequence)/7))  # Adjust the size (width, height) as needed
            else:
                fig = plt.figure(figsize=(10, 7))  
                
        else:
            fig = plt.figure(figsize=(width, height))  
    
        pos = nx.kamada_kawai_layout(G)
        
        node_labels = {node: data['name'] for node, data in G.nodes(data=True)}
        node_colors = [data['color'] for node, data in G.nodes(data=True)]
        
    
    
        
        # Create a dictionary of edge weights
        
        # Draw the graph with node colors and edge weights as labels
        nx.draw(G, pos, with_labels=True, labels=node_labels, node_size=500 , node_color=node_colors, node_shape = 'o', font_size=13, edge_color='gray')
        
        
        if show_plot == True:
            plt.show()
        elif show_plot == False:
            plt.close(fig)
        
        return fig, dot_bracket_structure
    
    except:
        
        print('\nSomething went wrong - predict_structure. Check the input or contact us!')
        return None, None



#sequences



def load_metadata(linkers:bool = True, loops:bool = True, regulators:bool = True, fluorescent_tag:bool = True, promoters:bool = True,  polya:bool = True, marker:bool = True, utr5:bool = True, utr3:bool = True, source = _cwd):
    
    """
    This function loads the metadata from library repository, which includes such elements like: 'codons', 'vectors', 'linkers', 'regulators', 'fluorescent_tag', 'backbone', 'promoters', 'restriction', 'polya_seq', 'selection_markers', 'rnai', 'capacity', 'utr5', 'utr3'.
    These elements are necessary for algorithms, as well as, the database of regulatory genetic sequences for users to project vectors and other genetic therapeutics.
    
    Args:
        
       Some metadata is not necessary for algorithms of plasmid vector creation, such as:

           linkers (bool) - linkers (sequences between coding sequences) and their  description, Default: True
           loops (bool) - loops (sequences for creating shRNA / siRNA) and their  description, Default: True
           regulators (bool) - regulators (regulatory sequence elements for expression enhancement) and their  description, Default: True
           fluorescent_tag (bool) - fluorescent_tag (sequences coding fluorescent proteins) and their  description, Default: True 
           promoters (bool) - promoters (previously described promoter sequences for providing coding and non-coding sequence transcription) and their  description, Default: True
           polya (bool) - signal of polyadenylation sequences and their description, Default: True
           marker (bool) - selection marker sequences for bacterial selection by resistance to antibiotics and their description, Default: True
           utr5 (bool) - 5`UTR sequences and their  description, Default: True
           utr3 (bool) - 3`UTR sequences and their  description, Default: True
       
      If the user uses external sources for providing these sequences and names, it can be set to False and these metadata will not load and reduce RAM usage.        
          
    Returns:
        dict: Dictionary with the crucial set of metadata

    """
    
    try:
        

        # must have to loaded for proper working algorithms
        codons = os.path.join(source, 'data/codons.xlsx')
        codons = pd.read_excel(codons)

        vectors = os.path.join(source, 'data/vectors.xlsx')
        vectors = pd.read_excel(vectors)
        
        backbone = os.path.join(source, 'data/backbone.xlsx')
        backbone = pd.read_excel(backbone)
        
        restriction = os.path.join(source, 'data/restriction_enzymes.xlsx')
        restriction = pd.read_excel(restriction)
        
        rnai = os.path.join(source, 'data/rnai_scoring.xlsx')
        rnai = pd.read_excel(rnai)

        capacity = os.path.join(source, 'data/vector_capacity.xlsx')
        capacity = pd.read_excel(capacity)

    

            
        if linkers == True:
            linkers = os.path.join(source,  'data/linkers.xlsx')
            linkers = pd.read_excel(linkers)
        else:
            linkers = None
        
        
        if regulators == True:
            regulators = os.path.join(source, 'data/regulators.xlsx')
            regulators = pd.read_excel(regulators)
        else:
            regulators = None
            
            
        if fluorescent_tag == True:
            fluorescent_tag = os.path.join(source,  'data/fluorescent_tag.xlsx')
            fluorescent_tag = pd.read_excel(fluorescent_tag)
        else:
            fluorescent_tag = None

         
        if promoters == True:
            promoters = os.path.join(source, 'data/promoters.xlsx')
            promoters = pd.read_excel(promoters)
        else:
            promoters = None

  
        if polya == True: 
            polya = os.path.join(source, 'data/polya.xlsx')
            polya = pd.read_excel(polya)
        else:
            polya = None


        if marker == True: 
            marker = os.path.join(source, 'data/selectors.xlsx')
            marker = pd.read_excel(marker)
        else:
            marker = None
            
            
        
        if loops == True: 
            loops = os.path.join(source, 'data/sh_loops.xlsx')
            loops = pd.read_excel(loops)
        else:
            loops = None



        if utr5 == True: 
            utr5 = os.path.join(source, 'data/utr5.json')
              
            with open(utr5, 'r') as file:
                utr5 = pd.DataFrame(json.load(file))
        else:
            utr5 = None
             

             
        if utr3 == True: 

            utr3 = os.path.join(source, 'data/utr3.json')
            
            with open(utr3, 'r') as file:
                utr3 = pd.DataFrame(json.load(file))
        
        else:
            utr3 = None
        

            
        metadata = {'linkers':linkers, 'loops':loops, 'regulators':regulators, 'fluorescent_tag':fluorescent_tag, 'promoters':promoters, 'polya_seq':polya, 'selection_markers':marker, 'utr5':utr5, 'utr3':utr3, 'codons':codons, 'vectors':vectors, 'rnai':rnai, 'capacity':capacity, 'backbone':backbone, 'restriction':restriction,}
    
        print('\nMetadata has loaded successfully')
        return metadata

    except:
        
        print('\nSomething went wrong - load_metadata. Check the input or contact us!')
        return None





def codon_otymization(sequence:str, metadata, species:str = 'human'):
    
          
    """
    This function optimize procided genetic sequence.
    
    Args:
       sequence (str) - nucleotide sequence provided in UPAC (ATGC)
       metadata (dict) - set of metadata loaded vie load_metadata()
       species (str) - species for which the codons are optimized in the sequence (human / mouse / rat). Default: 'human'
      

    Returns:
        DataFrame: Data frame containing the optimized sequence / input sequence and their statistics
       
    """
    
    try:
        if species.lower() in ['both', 'both2', 'multi']:
            species = 'human'
            
        codons = metadata['codons']
        
        codons = codons[codons['Species'] == species.lower()]
        seq_codon = [sequence[y:y+3].upper() for y in range(0, len(sequence), 3)]
        seq_codon_fr = [codons['Fraction'][codons['Triplet'] == seq.upper()][codons['Fraction'][codons['Triplet'] == seq.upper()].index[0]] for seq in seq_codon]
        seq_codon_fr = round(sum(seq_codon_fr) / len(seq_codon_fr),2)
        
        seq_codon_GC = (''.join(seq_codon).count('C') + ''.join(seq_codon).count('G')) / len(''.join(seq_codon)) * 100
        seq_aa = []
        for element in seq_codon:
            tmp = codons['Amino acid'][codons['Triplet'] == element.upper()]
            tmp = tmp.reset_index()
            seq_aa.append(tmp['Amino acid'][0])
            
        mean_GC = (len(sequence)-1)*58/100/len(sequence)*3
        
        seq_tmp = []
        
        for element in seq_aa:
            tmp = codons[codons['Amino acid'] == element].sort_values(['Fraction', 'GC_content'], ascending=[False, False])
            tmp = tmp.reset_index()
            seq_tmp.append(tmp['Triplet'][0])
            
        c = []
        g = []
    
        for n, codon in enumerate(seq_tmp):
            c.append(int(seq_tmp[n].count('C')))
            g.append(int(seq_tmp[n].count('G')))
        
        tmp2 = [x + y for x, y in zip(c, g)]
        df = np.array([seq_tmp, tmp2])
    
        m = 1
        for i in tqdm(range(1, len(df[1]))):
            if m/(i) > mean_GC*1.05:
                aa_1 =  str(codons['Amino acid'][codons['Triplet'] == df[0,i-1]][codons['Amino acid'][codons['Triplet'] == df[0,i-1]].index[0]])
                aa_2 =  str(codons['Amino acid'][codons['Triplet'] == df[0,i]][codons['Amino acid'][codons['Triplet'] == df[0,i]].index[0]])
                tmp_1 = codons[codons['Amino acid'] == aa_1].sort_values(['Fraction', 'GC_content'], ascending=[False, False])
                tmp_1 = tmp_1.reset_index()
                fr1_up = tmp_1['Fraction'][0]
                tmp_1 = tmp_1[tmp_1['GC_content'] < int(df[1,i-1])]
                if len(tmp_1) > 0:
                    tmp_1 = tmp_1.reset_index()
                    fr1_down = tmp_1['Fraction'][0]
                    diff1 = fr1_up - fr1_down
                else: 
                    diff1 = 1000
                tmp_2 = codons[codons['Amino acid'] == aa_2].sort_values(['Fraction', 'GC_content'], ascending=[False, False])
                tmp_2 = tmp_2.reset_index()
                fr2_up = tmp_2['Fraction'][0]
                tmp_2 = tmp_2[tmp_2['GC_content'] < int(df[1,i])]
                if len(tmp_2) > 0:
                    tmp_2 = tmp_2.reset_index()
                    fr2_down = tmp_2['Fraction'][0]
                    diff2 = fr2_up - fr2_down
                else: 
                    diff2 = 1000
    
    
                if diff1 <= diff2 and diff1 != 1000:
                   df[0,i-1] = tmp_1['Triplet'][0]
                   df[1,i-1] = tmp_1['GC_content'][0]
                   m += int(tmp_1['GC_content'][0])
                elif diff1 > diff2:
                    df[0,i] = tmp_2['Triplet'][0]
                    df[1,i] = tmp_2['GC_content'][0]
                    m += int(tmp_2['GC_content'][0])
                elif diff1 == 1000 &  diff2 == 1000:
                    next
            else:
                m += int(df[1,i])
                        
                      
        seq_tmp_GC_2 = (''.join(df[0]).count('C') + ''.join(df[0]).count('G')) / len(''.join(df[0])) * 100
        
        seq_aa_2 = []
        for element in df[0]:
            tmp = codons['Amino acid'][codons['Triplet'] == element]
            tmp = tmp.reset_index()
            seq_aa_2.append(tmp['Amino acid'][0])
            
        seq_codon_fr2 = [codons['Fraction'][codons['Triplet'] == seq][codons['Fraction'][codons['Triplet'] == seq].index[0]] for seq in df[0]]
        seq_codon_fr2 = round(sum(seq_codon_fr2) / len(seq_codon_fr2),2)
            
        df_final = {'status':[], 'sequence_na':[], 'sequence_aa':[], 'frequence':[], 'GC%': []}
        df_final['status'].append('not_optimized')
        df_final['status'].append('optimized')
        df_final['sequence_na'].append(''.join(seq_codon))
        df_final['sequence_na'].append(''.join(list(df[0])))
        df_final['sequence_aa'].append(''.join(seq_aa))
        df_final['sequence_aa'].append(''.join(seq_aa_2))
        df_final['frequence'].append(seq_codon_fr)
        df_final['frequence'].append(seq_codon_fr2)
        df_final['GC%'].append(seq_codon_GC)
        df_final['GC%'].append(seq_tmp_GC_2)
        
        df_final = pd.DataFrame(df_final)
        
        return df_final
    
    except:
        
        print('\nSomething went wrong - codon_otymization. Check the input or contact us!')
        return None

    


def check_restriction(sequence:str, metadata):
    
              
    """
    This function finds restriction places inside the sequence.    
    
    Args:
       sequence (str) - nucleotide sequence provided in UPAC (ATGC)
       metadata (dict) - set of metadata loaded vie load_metadata()
      

    Returns:
        DataFrame: Data frame containing the restriction places and position of its occurrence in the provided genetic sequence
        DataFrame: Data frame containing the parsed information about restriction places and their indexes to mapping to the first DataFrame

    """
    
    try:
   
        restriction = metadata['restriction']
        
        enzyme_restriction = {'name':[], 'restriction_place':[], 'restriction_sequence':[], 'start':[], 'stop':[]}
        
        #repaired :D
        bmp = list(sequence.upper())
        for r in tqdm(restriction.index):
            if restriction['sequence'][r] in sequence.upper():
                for n in range(0,len(restriction['sequence'][r])):
                    for j in range(n,len(bmp), len(restriction['sequence'][r])):
                       lower = j                       
                       upper = j + len(restriction['sequence'][r])
                       if upper < len(bmp) and ''.join(bmp[lower:upper]) == restriction['sequence'][r]:
                            enzyme_restriction['name'].append(restriction['name'][r])
                            enzyme_restriction['restriction_sequence'].append(restriction['sequence'][r])
                            enzyme_restriction['restriction_place'].append(restriction['restriction_place'][r])
                            enzyme_restriction['start'].append(lower)
                            enzyme_restriction['stop'].append(upper)
                            
    
                                   
        enzyme_restriction = pd.DataFrame.from_dict(enzyme_restriction)
        enzyme_restriction = enzyme_restriction.drop_duplicates()
        enzyme_restriction = enzyme_restriction.reset_index(drop=True)
        
        if len(enzyme_restriction['name']) > 0:
            restriction_df = enzyme_restriction.copy()
            restriction_df['index'] = restriction_df.index
            restriction_df = restriction_df[['name', 'index']]
            restriction_df['index'] = [[x] for x in restriction_df['index']]
            restriction_df = restriction_df.groupby('name').agg({'index': 'sum'})
            restriction_df = restriction_df.reset_index()
        
        else:
            restriction_df = enzyme_restriction
            print('\nAny restriction places were not found')
        
        return enzyme_restriction, restriction_df
    
    except:
        
        print('\nSomething went wrong - check_restriction. Check the input or contact us!')
        return None





def choose_restriction_to_remove(restriction_df, enzyme_list:list = []):
    
    if len(restriction_df) != 0 and len(enzyme_list) == 0:
        for i in restriction_df.index:
            print('-------------------------------------------------------------')
            print('id : ' + str(i))
            print('name : ' + restriction_df['name'][i])

    
        enzyme_list = []
        check = True
        enzyme_n = 1
        while (check == True):
            print('\n Provide enzyme id, if no restriction sites are relevant to your experiment or you have already provided all enzyme ids, write "x"')
            enzyme = input('\n Write enzyme '+ str(enzyme_n) + ' id: ')
            if len(enzyme) != 0 and not enzyme.isalpha() and int(enzyme) in restriction_df.index:
                enzyme_n += 1
                enzyme_list = enzyme_list + restriction_df['index'][int(enzyme)]
            elif len(enzyme) != 0 and enzyme.upper() == 'X':
                check = False
        
        enzyme_list = np.unique(enzyme_list)
    elif len(enzyme_list) > 0:
        print('\nRestriction places has chosen before!')     
    else:
        print('\nLack of restriction places to choose')
        
    return np.asarray(enzyme_list)       





def repair_sequences(sequence, metadata, restriction_df, enzyme_list, species):
    
    if species.lower() in ['both', 'both2', 'multi']:
        species = 'human'
        
    codons = metadata['codons']
    restriction = metadata['restriction']
        
    restriction = pd.DataFrame(restriction)
    if len(pd.DataFrame(restriction_df)) != 0:
        not_repaired = []
        codons = codons[codons['Species'] == species.lower()]
        seq_codon = [sequence[y:y+3].upper() for y in range(0, len(sequence), 3)]
        seq_codon_fr = [codons['Fraction'][codons['Triplet'] == seq.upper()][codons['Fraction'][codons['Triplet'] == seq.upper()].index[0]] for seq in seq_codon]
        seq_codon_fr = round(sum(seq_codon_fr) / len(seq_codon_fr),2)
        
        seq_aa = []
        for element in seq_codon:
            tmp = codons['Amino acid'][codons['Triplet'] == element]
            tmp = tmp.reset_index()
            seq_aa.append(tmp['Amino acid'][0])
        
        dic = {'seq':[], 'range':[], 'codon_n':[], 'aa':[]}
        n = 0
        for num, seq in enumerate(seq_codon):
            for i in range(0,3):
                dic['seq'].append(seq)
                dic['range'].append(n)
                dic['codon_n'].append(num)
                dic['aa'].append(seq_aa[num])
                n += 1
                
        dic = pd.DataFrame.from_dict(dic)
        
        print('\nCodon changing...')
        for eid in tqdm(enzyme_list):
            check = dic[['seq','codon_n']].drop_duplicates()
            check = ''.join(check['seq'])
            if restriction_df['restriction_sequence'][eid] in check:
                dic_tmp = dic[(dic['range'] >= restriction_df['start'][eid]) & (dic['range'] < restriction_df['stop'][eid])] 
                tmp = codons[codons['Triplet'].isin(np.unique(dic['seq']))]
                dictionary = {'seq':[], 'aa':[], 'triplet':[], 'freq':[], 'gc':[]}
                for i in np.unique(dic_tmp['seq']):
                    t = tmp[tmp['Triplet'] == i]
                    t = t.reset_index(drop = True)
                    t = tmp[tmp['Amino acid'] == t['Amino acid'][0]]
                    for n in t.index:
                        dictionary['seq'].append(i)
                        dictionary['aa'].append(t['Amino acid'][n])
                        dictionary['triplet'].append(t['Triplet'][n])
                        dictionary['freq'].append(t['Fraction'][n])
                        dictionary['gc'].append(t['GC_content'][n])
        
                
                dictionary = pd.DataFrame.from_dict(dictionary)
                dictionary = dictionary[~dictionary['triplet'].isin(dictionary['seq'])]
                dictionary = dictionary.sort_values(['freq', 'gc'], ascending=[False, False])
                dictionary = dictionary.reset_index()
        
        
                all_enzymes_variant = restriction[restriction['name'] == restriction_df['name'][eid]]
                
                
                seq_new = dic_tmp[['seq','codon_n']].drop_duplicates()
                seq_old = ''.join(seq_new['seq'])
                
                for d in dictionary.index:
                    seq_new = dic_tmp[['seq','codon_n']].drop_duplicates()
                    dictionary['seq'][d]
                    dictionary['triplet'][d]
                    seq_new['seq'][seq_new['seq'] == dictionary['seq'][d]] = dictionary['triplet'][d]
                    if ''.join(seq_new['seq']) in all_enzymes_variant['sequence']:
                        break
                    
                if seq_old == ''.join(seq_new['seq']):
                    not_repaired.append(restriction_df['name'][eid])
                elif seq_old != ''.join(seq_new['seq']):
                    for new in seq_new.index:
                        dic['seq'][dic['codon_n'] == seq_new['codon_n'][new]]  = seq_new['seq'][new]
        
    
            
        final_sequence = dic[['seq','codon_n']].drop_duplicates()
        final_sequence = ''.join(final_sequence['seq'])
        
        not_repaired = list(set(not_repaired))
        
        if len(not_repaired) == 0:    
            print('\nRestriction places in the sequence has repaired...')
        else:
            print('\nRestriction places for:')
            for i in not_repaired:
                print('\n'+ str(i))
                
            print('\nwere unable to optimize:')
            print('\nRest of chosen restriction places in the sequence has repaired...')
    
            
        print('\nChecking the new restriction places...')
        
        enzyme_restriction, restriction_df2  = check_restriction(final_sequence, metadata)
                                   
        enzyme_restriction = pd.DataFrame.from_dict(enzyme_restriction)
        enzyme_restriction = enzyme_restriction.drop_duplicates()
        enzyme_restriction = enzyme_restriction.reset_index(drop=True)
        enzyme_restriction = enzyme_restriction[~enzyme_restriction['name'].isin(restriction_df['name'])]
        
        
        if len(enzyme_restriction['name']) == 0:
            print('\nAny new restriction places were not created')
        else:
            print('\nNew restriction places were created:')
            for name in enzyme_restriction['name']:
                print(name)
    
    
    else:
        enzyme_restriction = {'name':[], 'restriction_place':[], 'restriction_sequence':[], 'start':[], 'stop':[]}
        enzyme_restriction = pd.DataFrame.from_dict(enzyme_restriction)
        not_repaired = []
        final_sequence = sequence

    return final_sequence, not_repaired, enzyme_restriction, pd.DataFrame(restriction_df2)



def sequence_restriction_removal(sequence:str, metadata, restriction_places:list = [], species:str = 'human'):
    
    """
    This function finds and removes restriction places inside the sequence.    
    
    Args:
       sequence (str) - nucleotide sequence provided in UPAC (ATGC)
       metadata (dict) - set of metadata loaded vie load_metadata()
       restriction_places (list) - list of potential restriction places defined by the user to remove from the sequence. Default: []
           *if the user did not define (empty list []) the potential restriction places to remove, the algorithm checks all possible restriction places, present it to the user (print), and asks him to choose which should be removed by writing IDs in consol.
       species (str) - species for which the codons are exchanged to remove restriction places (human / mouse / rat). Default: 'human'      

    Returns:
        DataFrame: Data frame containing the sequence before restriction removal and sequence after restriction removal and their statistics
       
    """
    
    try:
        enzyme_restriction, restriction_df = check_restriction(sequence, metadata)
        
        restriction_df['name_upper'] = [x.upper() for x in restriction_df['name']]
        
        enzyme_list = []
        for rp in restriction_places:
            try:
                enzyme_list += list(restriction_df['index'][restriction_df['name_upper'] == rp.upper()])[0]
            except:
                None
              
        
        if len(enzyme_list) > 0:
            enzyme_list = choose_restriction_to_remove(restriction_df, enzyme_list = enzyme_list)
        elif len(enzyme_list) == 0 and len(restriction_places) == 0:
            enzyme_list = choose_restriction_to_remove(restriction_df, enzyme_list = [])
        
        if len(enzyme_list) > 0:
            final_sequence, not_repaired, enzyme_restriction, restriction_df = repair_sequences(sequence, metadata, enzyme_restriction, enzyme_list, species)
        else:
            final_sequence = sequence
            not_repaired = []
            
        codons = metadata['codons']
        input_seq = [sequence[y:y+3].upper() for y in range(0, len(sequence), 3)]
        
        input_seq_GC_ = round((sequence.count('C') + sequence.count('G')) / len(sequence) * 100, 2)
        
        input_seq__aa = []
        for element in input_seq:
            tmp = codons['Amino acid'][codons['Triplet'] == element]
            tmp = tmp.reset_index()
            input_seq__aa.append(tmp['Amino acid'][0])
            
        input_seq__fr = [codons['Fraction'][codons['Triplet'] == seq][codons['Fraction'][codons['Triplet'] == seq].index[0]] for seq in input_seq]
        input_seq__fr = round(sum(input_seq__fr) / len(input_seq__fr),2)
        
        
        
        output_seq = [final_sequence[y:y+3].upper() for y in range(0, len(final_sequence), 3)]
        
        output_seq_GC_ = round((final_sequence.count('C') + final_sequence.count('G')) / len(final_sequence) * 100, 2)
        
        output_seq_aa = []
        for element in input_seq:
            tmp = codons['Amino acid'][codons['Triplet'] == element]
            tmp = tmp.reset_index()
            output_seq_aa.append(tmp['Amino acid'][0])
            
        output_seq___fr = [codons['Fraction'][codons['Triplet'] == seq][codons['Fraction'][codons['Triplet'] == seq].index[0]] for seq in output_seq]
        output_seq___fr = round(sum(output_seq___fr) / len(output_seq___fr),2)
            
        df_final = {'status':[], 'sequence_na':[], 'sequence_aa':[], 'frequence':[], 'GC%': [], 'unable_repaire': []}
        df_final['status'].append('before_restriction_removal')
        df_final['status'].append('after_restriction_removal')
        df_final['sequence_na'].append(sequence)
        df_final['sequence_na'].append(final_sequence)
        df_final['sequence_aa'].append(''.join(input_seq__aa))
        df_final['sequence_aa'].append(''.join(output_seq_aa))
        df_final['frequence'].append(input_seq__fr)
        df_final['frequence'].append(output_seq___fr)
        df_final['GC%'].append(input_seq_GC_)
        df_final['GC%'].append(output_seq_GC_)
        df_final['unable_repaire'].append('X')
        df_final['unable_repaire'].append(not_repaired)
    
        
        df_final = pd.DataFrame(df_final)
            
        return df_final
    
    except:
        
        print('\nSomething went wrong - sequence_restriction_removal. Check the input or contact us!')
        return None

   
        
    



def load_fasta(path:str):
    
    """
    This function finds and removes restriction places inside the sequence.    
    
    Args:
       path (str) - path to the FASTA file *.FASTA
       

    Returns:
        str: Loaded FASTA file to the string object
       
    """
    
    try:
        with open(path, 'r') as f:
            fasta = f.read()
           
        return fasta
    except:
        
        print('\nSomething went wrong - load_fasta. Check the input or contact us!')
        return None

    
    


def decode_fasta_to_dataframe(fasta_file:str):
    
    """
    This function decodes the FASTA file from the string to the data frame   
    
    
    Args:
       fasta_file (str) - FASTA file (string) loaded by load_fasta() from external source

    Returns:
        DataFrame: Data frame containing in separate columns FASTA headers and sequences
       
    """
    try:
        
        headers = []
        sequences = []
    
      
        lines = fasta_file.split('\n')
    
        header = None
        sequence = []
    
        for line in lines:
            line = line.strip()
    
            if line.startswith('>'):
                # If it's a header line
                if header is not None:
                    # Save the previous sequence and header
                    headers.append(header)
                    sequences.append(''.join(sequence))
                
                # Start a new header
                header = line[1:]
                sequence = []
            else:
                # If it's a sequence line
                sequence.append(line)
    
        # Add the last sequence and header
        if header is not None:
            headers.append(header)
            sequences.append(''.join(sequence))
            
        df = pd.DataFrame({'header':headers, 'sequence':sequences})
    
        return df
    
    except:
        
        print('\nSomething went wrong - decode_fasta_to_dataframe. Check the input or contact us!')
        return None





def extract_header_info(df_fasta:pd.DataFrame):
    
    """
    This function extracts the necessary information from headers for vector plotting using plot_vector()
    
    For decoding headers the FASTA structure should be:
            
        >name1_start:1_stop:130_length:130 visible=True
        CTGCGCGCTCGCTCGCTCACTGAGGCCGCCCGGGCAAAGCCCGGGCGTCGGGCGACC
        
        >name2_start:131_stop:157_length:27 visible=False
        TCTAGACAACTTTGTATAGAAAAGTTG
        
        >name3_start:158_stop:617_length:460 visible=True
        GGGCTGGAAGCTACCTTTGACATCATTTCCTCTGCGAATGCATGTATAATTTCTAC
        
        Header explanation:
            name1,2,3,... - the name of the sequence element
            start - beginning of the sequence in the plasmid vector
            stop - end of the sequence in the plasmid vector
            length - the length of the sequence
            visible - True or False, if the element ought to 
            be displayed and signed or not on the graph

    
    Args:
       df_fasta (DataFrame) - FASTA data frame obtained from decode_fasta_to_dataframe()
       
       

    Returns:
        DataFrame: Data frame with additional columns of decoded headers for plot_vector() function 
       
    """
    try:
        
        def extract_values(string):
            pattern = r"(.*?)_start:(\d+)_stop:(\d+)_length:(\d+) visible=(\w+)"
            match = re.search(pattern, string)
            if match:
                return [match.group(1), match.group(2), int(match.group(3)), int(match.group(4)), str(match.group(5))]
            else:
                return None
        element = []
        start = []
        end = []
        length = []
        visible = []
        
        for h in df_fasta['header']:
            hed = extract_values(h)
            element.append(hed[0])
            start.append(hed[1])
            end.append(hed[2])
            length.append(hed[3])
            visible.append(hed[4])
            
        df_fasta['element'] = element
        df_fasta['start'] = start
        df_fasta['end'] = end
        df_fasta['length'] = length
        df_fasta['visible'] = visible
        
        return df_fasta
    
    except:
        
        print('\nSomething went wrong - extract_header_info. Check the input or contact us!')
        return None





 #       _  ____   _         _____              _                      __ _____  __  
 #      | ||  _ \ (_)       / ____|            | |                    / /|  __ \ \ \ 
 #      | || |_) | _   ___ | (___   _   _  ___ | |_  ___  _ __ ___   | | | |__) | | |
 #  _   | ||  _ < | | / _ \ \___ \ | | | |/ __|| __|/ _ \| '_ ` _ \  | | |  _  /  | |
 # | |__| || |_) || || (_) |____) || |_| |\__ \| |_|  __/| | | | | | | | | | \ \  | |
 #  \____/ |____/ |_| \___/|_____/  \__, ||___/ \__|\___||_| |_| |_|  \_\|_|  \_\/_/
 #                                   __/ |                                   
 #                                  |___/      