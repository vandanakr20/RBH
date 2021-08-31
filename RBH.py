#!/usr/bin/env python

#loop through both sorted files --> used Leslie's data
file1 = 'sorted_human_vs_Zfish_DB'
file2 = 'sorted_Zfish_vs_human_DB'

#initialize empty dicts for both files
Human_Zfish_DB = {}
Zfish_human_DB = {}

#open the human vs zfish DB file
with open(file1, 'r') as fh1:
    cur_human_ID = ''
    cur_Zfish_ID = '' 
    cur_evalue = '' 
    good_flag = True

    # split the lines to extract the human id, zfish id, and the evalue      
    for line in fh1:
        line_list = line.split('\t')
        run_human_ID = line_list[0]
        run_Zfish_ID = line_list[1]
        run_evalue = line_list[10]

        # if another ID (not the current one)
        if cur_human_ID != run_human_ID:
            # if it is a possible RBH, add to dict
            if good_flag:
                Human_Zfish_DB[cur_human_ID] = cur_Zfish_ID

            # set the new IDs
            cur_human_ID = line_list[0]
            cur_Zfish_ID = line_list[1]
            cur_evalue = line_list[10]
            good_flag = True

        
        else: #same id
            # if the ids are the same and the evalues are the same, it is not an RBH hit
            if cur_evalue == run_evalue:
                good_flag = False

    #add the last record to the dict if it is a possible RBH 
    if good_flag:
        Human_Zfish_DB[cur_human_ID] = cur_Zfish_ID


#open the zfish vs human DB file
with open(file2, 'r') as fh2:
    cur_human_ID = ''
    cur_Zfish_ID = '' 
    cur_evalue = '' 
    good_flag = True   

    # split the lines to extract the human id, zfish id, and the evalue    
    for line in fh2:
        line_list = line.split('\t')
        run_human_ID = line_list[1]
        run_Zfish_ID = line_list[0]
        run_evalue = line_list[10]

        # if another ID (not the current one)
        if cur_Zfish_ID != run_Zfish_ID:

            # if it is a possible RBH, add to dict
            if good_flag:
                Zfish_human_DB[cur_Zfish_ID] = cur_human_ID
            # set the new IDs
            cur_human_ID = line_list[1]
            cur_Zfish_ID = line_list[0]
            cur_evalue = line_list[10]
            good_flag = True
        
        else: #same id
            # if the ids are the same and the evalues are the same, it is not an RBH hit
            if cur_evalue == run_evalue:
                good_flag = False

    #add the last record to the dict if it is a possible RBH 
    if good_flag:
        Zfish_human_DB[cur_Zfish_ID] = cur_human_ID


# loop through both files to find the RBHs
RBH_dict = {}
for h_ID in Human_Zfish_DB:
    for z_ID in Zfish_human_DB:
        # if the match is both ways 
        if h_ID == Zfish_human_DB[z_ID] and Human_Zfish_DB[h_ID] == z_ID:
            RBH_dict[h_ID] = z_ID


human_dict = {}
zfish_dict = {}

#open both biomart files and make them into a dict
with open ("Human_mart.txt", "r") as human_bio:
    for line in human_bio:
        #split the lines and append to dict
        gene_ids = line.split("\t")[0]
        protein_ids = (line.split("\t")[1])
        gene_names = line.split("\t")[2].strip()

        #append to dict
        human_dict[protein_ids] = []
        human_dict[protein_ids].append(gene_ids)
        human_dict[protein_ids].append(gene_names)


with open ("Zfish_mart.txt", "r") as zfish_bio:
    for line in zfish_bio:
        #split the lines and append to dict
        gene_ids = line.split("\t")[0]
        protein_ids = (line.split("\t")[1])
        gene_names = line.split("\t")[2].strip()

        #append to dict
        zfish_dict[protein_ids] = []
        zfish_dict[protein_ids].append(gene_ids)
        zfish_dict[protein_ids].append(gene_names)


#write the Gene Id, protein Id, and protein name for each species to the output file
with open ('Human_Zebrafish_RBH.tsv', 'w') as fh3:
    for key in RBH_dict:
        if key == '':
            continue
        print(key + '\t' + human_dict[key][0] + '\t' + human_dict[key][1] + '\t' + RBH_dict[key] + '\t' + zfish_dict[RBH_dict[key]][0] + '\t' + zfish_dict[RBH_dict[key]][1], file = fh3)
        
         
