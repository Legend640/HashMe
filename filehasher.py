import os, hashlib


####FILE HASHING PROGRAM


####Select Options (HASH FUNCTION / OUTPUT FILE / Directory)


####Hash Functions

def hashFile(file, alg):
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
                print('Invalid Hashing Algorithm')
    except:
        print('Error Hashing File')
    
def validateTarget(target):
    if os.path.isdir(target) == True:
        return True
    else:
        return False

print("HashMe version 1.0")
print("================")

while True:
    targetDirectory = input('Enter Directory Containing Files to Hash:'  )
    if validateTarget(targetDirectory) == True:
        break
    else:
        print('Invalid Directory')
        continue

while True:   
    hashAlg = input('What hash would you like: MD5, SHA1, or SHA256?  ')
    if hashAlg.lower() == 'md5':
        break
    elif hashAlg.lower() == 'sha1':
        break
    elif hashAlg.lower() == 'sha256':
        break
    else:
        print('Invalid Entry')
        continue

while True:
    exportMode = input('Enter (1) for text file with hashes, (2) for CSV with filename and hashes:  ')
    if exportMode == '1' or exportMode == '2':
        break
    else:
        print('Invalid Entry')
        continue

exportFile = input('Enter Filename for Export:  ')
if exportFile == '':
    exportFile = 'Hash List'

userProfile = os.environ['USERPROFILE']

try:
    if exportMode == '1':
        fileExt = '.txt'
    elif exportMode == '2':
        fileExt = '.csv'
    with open(f'{userProfile}//Desktop/{exportFile}{fileExt}', 'w') as F:
        for (r,d,f) in os.walk(targetDirectory):
            if exportMode == '1':
                for x in f:
                    filePath = os.path.join(r, x)
                    hashValue = hashFile(filePath, hashAlg)
                    print(f'{filePath}:  {hashValue}')
                    print(f'{hashValue}', file = F)
            elif exportMode == '2':
                for x in f:
                    filePath = os.path.join(r, x)
                    hashValue = hashFile(filePath, hashAlg)
                    print(f'{filePath}:  {hashValue}')
                    print(f'{filePath}, {hashValue}', file = F)
            else:
                print('Error Starting Hash Process')
                
except:
    print('Error Exporting File')     
else:
    print('Export File Complete')
        

