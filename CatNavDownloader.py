

import os
import urllib.request, json 
import requests
import hashlib
import time
import getopt
import sys
from sys import argv
from os import path
from multiprocessing import Pool, TimeoutError

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(32768), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def fetchURL(url, destination, hash):
    if(path.exists(destination)):
        calcMd5 = md5(destination)
        if(hash is None):
            print("No Checksum, deleting: " + destination)
            os.remove(destination)
        elif(calcMd5 == hash):
            print(destination + " already exists with correct checksum, skipping...")
            return
        else:
            print("fetched MD5:" + calcMd5)
            print("expected MD5:" + hash)
            print("Invalid checksum, deleting: " + destination)
            os.remove(destination)
    with requests.get(url, stream=True) as r:
        print("Fetching: " + destination + " (" + sizeof_fmt(int(r.headers['Content-length'])) + ")...")
        r.raise_for_status()
        with open(destination, 'wb') as f:
            for chunk in r.iter_content(chunk_size=32768): 
                f.write(chunk)
            print("Completed: " + destination + " (" + sizeof_fmt(int(r.headers['Content-length'])) + ")")        
    calcMd5 = md5(destination)
    if((hash is not None) and (calcMd5 != hash)):
        print("fetched MD5:" + calcMd5)
        print("expected MD5:" + hash)
        raise RuntimeError   
    return


if __name__ == '__main__':

    catalog=None
    outputDir=None

    try:
        opts, args = getopt.getopt(argv[1:],"u:d:")
    except getopt.GetoptError:
        print ('test.py -u URL -d output dir')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -u URL to catalog file -d output directory')
            sys.exit()
        elif opt in ("-u", "--url"):
            catalog = arg
        elif opt in ("-d", "--output-dir"):
            outputDir = arg

    print("Starting CatNavDownloader....")
    print("Catalog URL: " + catalog)
    print("Output Directory: " + outputDir) 
    
    print("Catalog: " + catalog[17:])
    if(catalog[:17] == "heremapdownloader"):
        catalog="https" + catalog[17:]
    
    
    print("Catalog URL: " + catalog)
        
    outputDir=outputDir + "/HereV1/"

    if not path.exists(outputDir):
        os.mkdir(outputDir)

    totalBytes=0
    print("Fetching catalog from: " + catalog)

    with urllib.request.urlopen(catalog) as url:
        data = json.loads(url.read().decode())
        #TODO check for distrition other than '1' and abort
        with Pool(processes=8) as pool:
            metaDataDone = False
            for link in data['distribution']['1']['links']:
                if(link['rel'] == 'drm'):
                    pool.apply_async(fetchURL,(link['href'],outputDir + "update.xml", None))
                elif((link['rel'] == 'dataGroup') or (link['rel'] == 'voice')):
                    totalBytes += link['length']
                    pool.apply_async(fetchURL,(link['href'],outputDir + link['otherAttributes']['local-id'] + ".zip", (link['hash'])[4:]))
                elif(link['rel'] == 'metaData'):
                    if(not metaDataDone):
                        totalBytes += link['length']
                        pool.apply_async(fetchURL,(link['href'],outputDir + "Metadata.zip", (link['hash'])[4:]))
                        metaDataDone = True
                else:
                    print("Unexpected value for link rel: " + link['rel'])
                    raise RuntimeError
            
            print("Total Map Size: " + sizeof_fmt(totalBytes))    
            pool.close()
            print("Waiting for processing to complete...")
            pool.join()
            print("Done!")