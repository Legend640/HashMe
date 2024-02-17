"""
HashMe Simple File Hasher

Provides hash values of a file or directory of files using MD5, SHA1, or SHA256.
Option to export plain hash list or CSV file of hashes and file names.
"""
#Imports
import os, hashlib, time, logging
from multiprocessing.pool import ThreadPool

#Function to validate if the target file or directory is valid.
#Takes the target name and returns the type (directory or file) or False if invalide
def validateTarget(target):
    if os.path.isdir(target) == True:
        return('directory')
    elif os.path.isfile(target) == True:
        return('file')
    else:
        return False

#Function to hash the individual file.  Takes two arguments: the file name 
#and choice of hashing algorithm.
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
    except:
        print(f'Error Hashing File: {file}')
    
#Function prepare files for hashing, calls the hasher() function and outputs results
def startHasher(targetName, exportMode, alg, runType):
    userProfile = os.environ['USERPROFILE']
    start_time = time.time()
    file_count = 0
    byte_count = 0
    if exportMode == 1:
        fileExt = '.txt'
    elif exportMode == 2:
        fileExt = '.csv'
    if runType == 'file':
            hashValue = hasher(targetName, alg)
            file_count += 1
            file_size = os.stat(targetName)[6]
            byte_count += file_size
            print('=' * 15)
            print('+++File Hashes+++')
            print(f'{targetName}:  {hashValue}')
            if exportMode == 1 or exportMode == 2:
                with open(f'{userProfile}/Desktop/HashList{fileExt}', 'w') as output_file:
                    print(f'{hashValue}', file = output_file)
            print('=' * 15) 
    elif runType == 'directory':
        print('=' * 15)
        print('+++File Hashes+++')
        if exportMode == 1 or exportMode == 2:
            with open(f'{userProfile}/Desktop/HashList{fileExt}', 'w') as output_file:
                for (r,d,f) in os.walk(targetName):
                    pool = ThreadPool(4)
                    for x in f:
                        filePath = os.path.join(r, x)
                        hashValue = pool.apply_async(hasher, ([filePath, alg])).get()
                        file_count += 1
                        file_size = os.stat(filePath)[6]
                        byte_count += file_size                            
                        print(f'{filePath}:  {hashValue}')
                        if exportMode == 1 or exportMode == 2:
                                if exportMode == 1:
                                    print(f'{hashValue}', file = output_file)
                                elif exportMode == 2:
                                    print(f'{filePath}, {hashValue}', file = output_file)
                pool.close()
                pool.join()
        elif exportMode == 3:
            for (r,d,f) in os.walk(targetName):
                pool = ThreadPool(4)
                for x in f:
                    filePath = os.path.join(r, x)
                    hashValue = pool.apply_async(hasher, ([filePath, alg])).get()
                    file_count += 1
                    file_size = os.stat(filePath)[6]
                    byte_count += file_size                            
                    print(f'{filePath}:  {hashValue}')
                pool.close()
                pool.join()
        print('=' * 15) 
    end_time = time.time()
    print('Hashing Complete')
    print(f'Total Files Hashed: {file_count}')
    print(f'Total Bytes Hashed: {byte_count}')
    print(f'Total Time: {end_time - start_time}')
    print('=' * 15)
    print('')


#Main program function
def main():
    print('')
    print("=" * 40)
    print(f"HashMe-Simple File Hashing version {version}")
    print("=" * 40)
    while True:
        targetName = input("Enter the single file or directory of files to hash:  ")
        runType =validateTarget(targetName)
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
        exportMode = int(input("Enter (1) for text file, (2) for csv file, or (3) for display only:  "))
        if exportMode > 0 or exportMode <3:
            break
        else:
            print("Invalid option, try again")
            continue
    print(runType, targetName, alg, exportMode)
    #try:
    startHasher(targetName, exportMode, alg, runType)
    #except:
        #print('Unable to start hashing')
    

#Main Program
if __name__ == '__main__':
    version = .05
    main()