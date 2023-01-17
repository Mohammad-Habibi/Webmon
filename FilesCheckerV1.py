import argparse
import os
import sys
import hashlib

# First Install argparse:
#> pip install argparse

File_List_A = []
File_List_B = []

File_List_Updated= []  # used for compare hash

Suspect_Files = [] # suspect file

Output_file = [""]

def sha256sum(filename):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest()
        

def check_hash(fls,pat1,pat2):
    for uu in fls:
        gh = str((uu.split(pat1))[1])
        newf = pat1 + gh
        oldf = pat2 + gh
        
        if sha256sum(newf)!= sha256sum(oldf):
            print ("File : "+ gh + " Changed :")
            print(newf + "  "+ sha256sum(newf))
            print(oldf + "  "+ sha256sum(oldf))
            print ("---------------------------------")

            fr = open(Output_file[0],"a")
            fr.write("\nFile : "+ gh + " Changed :\n")
            fr.write(newf + "  "+ sha256sum(newf))
            fr.write("\n"+oldf + "  "+ sha256sum(oldf))
            fr.write("\n---------------------------------")
            fr.close()


def find_new_file(dirn,diro):

    for root, dirs, files in os.walk(dirn):
        for file in files:
            cvr = os.path.join(root, file)
            File_List_A.append(str(cvr))

    for root, dirs, files in os.walk(diro):
        for file in files:
            cvr = os.path.join(root, file)
            File_List_B.append(str(cvr))
    for ccc in File_List_A:
        gh = str((ccc.split(dirn))[1])
        gh1 = (diro+gh)
        if gh1 in File_List_B:
            File_List_Updated.append(ccc)
        else:
            Suspect_Files.append(ccc)

           
    print ("==================================================")
    print (" + "+str(len(File_List_A))+" File Founded In "+dirn+ " Directory")
    print (" + "+str(len(File_List_B))+" File Founded In "+diro+ " Directory")
    print ("==================================================")

    fr = open(Output_file[0],"a")
    fr.write("\n==================================================")
    fr.write("\n + "+str(len(File_List_A))+" File Founded In "+dirn+ " Directory")
    fr.write("\n + "+str(len(File_List_B))+" File Founded In "+diro+ " Directory")
    fr.write("\n==================================================")
    fr.close()
    

    
    if len(Suspect_Files) > 0:
        fr = open(Output_file[0],"a")
        fr.write("\n New File List:")
        fr.close()
        print (" New File List:")
        for vvv in Suspect_Files:
            print("    !---- "+ vvv )
            fr = open(Output_file[0],"a")
            fr.write("\n    !---- "+ vvv )
            fr.close()

    print ("==================================================")
    fr = open(Output_file[0],"a")
    fr.write("\n==================================================")
    fr.close()
    check_hash(File_List_Updated,dirn,diro)
    
            
    

def main():
    parser = argparse.ArgumentParser(description='File Integrity Check')
    parser.add_argument("-n", "--new" , help='New Files Directory',required=True)
    parser.add_argument("-p", "--old" , help='Old Files Directory',required=True)
    parser.add_argument("-o", "--output" , help='Output Text File',required=True)
    

    args = parser.parse_args()
    Output_file[0] = args.output
    find_new_file(args.new,args.old)

main()


# python FilesCheckerV1.py -n .\new -p .\old -o out.txt
