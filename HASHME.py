"""
HashMe Simple File Hasher

Provides hash values of a file or directory of files using MD5, SHA1, or SHA256.
Option to export plain hash list or CSV file of hashes and file names.
"""
#Imports
import os, hashlib, time, logging
from multiprocessing import Pool as ThreadPool
from pathlib import Path
import sys

#Function to validate if the target file or directory is valid.
#Takes the target name and returns the type (directory or file) or False if invalid
def validateTarget(target):
    path = Path(target)
    if target == '':
        return False
    elif path.is_file():
        return('file')
    elif path.is_dir():
        return('directory')
    else:
        return False

#Function to hash the individual file.  Takes two arguments: the file name 
#and choice of hashing algorithm. Returns 0 if no data or 1 if can't hash.
def hasher(file, alg):
    md5Hash = hashlib.md5()
    sha1Hash = hashlib.sha1()
    sha256Hash = hashlib.sha256()
    try:
        with open (file, 'rb') as f:
            data = f.read()
            if alg == 'md5':
                md5Hash.update(data)
                return md5Hash.hexdigest()
            elif alg == 'sha1':
                sha1Hash.update(data)
                return sha1Hash.hexdigest()
            elif alg == 'sha256':
                sha256Hash.update(data)
                return sha256Hash.hexdigest()
            else:
                print(f'Error: Invalid Hashing Algorithm when Processing {file}')
                return 0
    except:
        print(f'Error Hashing File: {file}')
        return 1
    
#Function prepare files for hashing, calls the hasher() function and outputs results
def startHasher(targetName, exportMode, alg, runType):
    userProfile = os.environ['USERPROFILE']
    start_time = time.time()
    file_count = 0
    byte_count = 0
    error_count = 0
    zero_count = 0
    if exportMode == 1:
        fileExt = '.txt'
    elif exportMode == 2:
        fileExt = '.csv'
    if runType == 'file':
            file_size = os.stat(targetName)[6]
            print('=' * 17)
            print('+++File Hashes+++')
            print('=' * 17)
            if file_size != 0:
                hashValue = hasher(targetName, alg)
                if hashValue != 0 or hashValue != 1:
                    hashValue = hashValue
                    file_count += 1
                    byte_count += file_size
                    print(f'{targetName}:  {hashValue}')
                    if exportMode == 1 or exportMode == 2:
                        with open(f'{userProfile}/Desktop/HashList{fileExt}', 'w') as output_file:
                            if exportMode == 1:
                                print(f'{hashValue}', file = output_file)
                            elif exportMode == 2:
                                print(f'{targetName}, {hashValue}', file = output_file)      
                else:
                    error_count += 1
            else:
                print(f'{targetName} contains no data and was not hashed')
                zero_count += 1
    elif runType == 'directory':
        print('=' * 17)
        print('+++File Hashes+++')
        print('=' * 17)
        if exportMode == 1 or exportMode == 2:
            with open(f'{userProfile}/Desktop/HashList{fileExt}', 'w') as output_file:
                pool = ThreadPool(4)
                for (r,d,f) in os.walk(targetName):
                    for x in f:
                        filePath = os.path.join(r, x)
                        file_size = os.stat(filePath)[6]
                        if file_size != 0:
                            hashValue = pool.apply_async(hasher, ([filePath, alg])).get()
                            if hashValue != 0 or hashValue != 1:
                                hashValue = hashValue
                                file_count += 1
                                byte_count += file_size                            
                                print(f'{filePath}:  {hashValue}')
                                if exportMode == 1 or exportMode == 2:
                                    if exportMode == 1:
                                        print(f'{hashValue}', file = output_file)
                                    elif exportMode == 2:
                                        print(f'{filePath}, {hashValue}', file = output_file)
                            else:
                                error_count += 1
                        else:
                            print(f'{targetName} contains no data and was not hashed')
                            zero_count += 1
            pool.close()
            pool.join()
        elif exportMode == 3:
            pool = ThreadPool(4)
            for (r,d,f) in os.walk(targetName):
                for x in f:
                    filePath = os.path.join(r,x)
                    file_size = os.stat(filePath)[6]
                    if file_size != 0:
                        hashValue = pool.apply_async(hasher, ([filePath, alg])).get()
                        if hashValue != 0 or hashValue != 1:
                            hashValue = hashValue
                            file_count += 1
                            byte_count += file_size                            
                            print(f'{filePath}:  {hashValue}')
                        else:
                            error_count += 1
                    else:
                        print(f'{targetName} contains no data and was not hashed')
                        zero_count += 1
            pool.close()
            pool.join()  
    end_time = time.time()
    print('=' * 17) 
    print('Hashing Complete')
    print(f'Total Files Hashed: {file_count}')
    print(f'Total Bytes Hashed: {byte_count}')
    print(f'Total files not-hashed with errors:  {error_count}')
    print(f'Total files not hashed-contains zero bytes: {zero_count}')
    print(f'Total Time: {end_time - start_time}')
    print('=' * 17)
    print('')


#Accepting input from user through command line prompts
def verbose():
    print('')
    print("=" * 42)
    print(f"HashMe - Simple File Hasher Version {version}")
    print("=" * 42)
    while True:
        targetName = input("Enter the single file or directory of files to hash:  ")
        runType = validateTarget(targetName)
        if runType != False:
            break
        else:
            print("Target isn't valid, try again")
            continue        
    while True:
        alg = str(input("Enter md5, sha1, or sha256 as the hashing algorithm:  ")).lower()
        if alg == 'md5' or alg == 'sha1' or alg == 'sha256':
            break
        else:
            print ("Unrecognized hashing algorithm, try again")
            continue
    while True:
        try:
            exportMode = int(input("Enter (1) for text file, (2) for csv file, or (3) for display only:  "))
        except: 
            print("Invalid option, try again")
            continue
        if exportMode == 1 or exportMode == 2 or exportMode == 3:
            break
        else:
            print("Invalid option, try again")
            continue
    print(runType, targetName, alg, exportMode)
    try:
        startHasher(targetName, exportMode, alg, runType)
    except:
        print('ERROR: Unable to start hasher')
        sys.exit()

#Accepting inputs directly from user through the command line system arguments     
def arguments():
    while True:
        targetName = sys.argv[1]
        alg = sys.argv[2]
        if alg.lower() == 'md5' or alg == 'sha1' or alg == 'sha256':
            alg = alg.lower()
        else:
            print("Invalid hash value argument")
            verbose()
            break
        runType = validateTarget(targetName)
        if runType == False:
            verbose()
            break
        exportMode = int(sys.argv[3])
        if exportMode != 1 and exportMode != 2 and exportMode != 3:
            print("Invalid export mode")
            verbose() 
            break
        print("=" * 42)
        print(f"HashMe-Simple File Hasher Version {version}")
        print("=" * 42)
        try:
            startHasher(targetName, exportMode, alg, runType)
            break
        except:
            print("ERROR: Unable to start hasher")
            break

#Main program, determines input method.  Defaults to verbose()
def main():
    if len(sys.argv) == 1:
        verbose()
    elif len(sys.argv) == 4:
        arguments()
    else:
        print("Invalid numer of arguments")
        verbose()
    
#Main Program
if __name__ == '__main__':
    version = .99
    main()

