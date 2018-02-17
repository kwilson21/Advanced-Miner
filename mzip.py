import logging
import json
import os
import wget
import zipfile
import io
import calclog
import sys

FILEPATH = os.path.dirname(os.path.realpath(__file__))

miner_info = json.load(open('miners.json'))

ziplog = logging.getLogger('miner')

def download_miners(miner_info):
    downloaded = True

    if not os.path.exists(FILEPATH + "/hsrminer_neoscrypt_fork.zip") or not os.path.exists(FILEPATH + "/0.3.4b.7z") \
        or not os.path.exists(FILEPATH + "/ccminer-x86-2.2.7z") or not os.path.exists(FILEPATH + "/ccminer_x86.7z") \
        or not os.path.exists(FILEPATH + "/ccminer-hsr-alexis-x86-cuda8.7z") or not os.path.exists(FILEPATH + "/ccminer-x86-2.2.4-cuda9.7z"):
        downloaded = False

    if not downloaded:
        ziplog.info("Downloading miners...")

        if not os.path.exists(FILEPATH + "/hsrminer_neoscrypt_fork.zip"):
            ziplog.debug("hsrminer not downloaded, downloading...")
            wget.download(miner_info['algo']['neoscrypt'])
        if not os.path.exists(FILEPATH + "/0.3.4b.7z"):
            ziplog.debug("EWBF not downloaded, downloading...")
            wget.download(miner_info['algo']['equihash'])
        if not os.path.exists(FILEPATH + "/ccminer-x86-2.2.7z"):
            ziplog.debug("CCminer TPruvot not downloaded, downloading...")
            wget.download(miner_info['algo']['skunkhash'])
        if not os.path.exists(FILEPATH + "/ccminer_x86.7z"):
            ziplog.debug("CCminer Alexis78cuda9 not downloaded, downloading...")
            wget.download(miner_info['algo']['xevan'])
        if not os.path.exists(FILEPATH + "/ccminer-hsr-alexis-x86-cuda8.7z"):
            ziplog.debug("CCminer Alexis78cud8 not downloaded, downloading...")
            wget.download(miner_info['algo']['nist5'])
        if not os.path.exists(FILEPATH + "/ccminer-x86-2.2.4-cuda9.7z"):
            ziplog.debug("CCminer TPruvotcuda9 not downloaded, downloading...")
            wget.download(miner_info['algo']['tribus'])

        ziplog.debug("Download successful.")

        downloaded = True
    else:
        ziplog.info("Loading miners...")

    return downloaded

def extract_miners():
    extracted = True
    
    if not os.path.exists(FILEPATH + "/bin/NVIDIA-hsrminer-neoscrypt") or not os.path.exists(FILEPATH + "/bin/NVIDIA-EWBF") \
        or not os.path.exists(FILEPATH + "/bin/NVIDIA-TPruvot") or not os.path.exists(FILEPATH + "/bin/NVIDIA-Alexis78cuda9") \
        or not os.path.exists(FILEPATH + "/bin/NVIDIA-Alexis78cuda8") or not os.path.exists(FILEPATH + "/bin/NVIDIA-TPruvotcuda9"):
        extracted = False

    if not extracted:
        ziplog.info("Extracting miners...")

        if not os.path.exists(FILEPATH + "/bin/NVIDIA-hsrminer-neoscrypt"):
            ziplog.debug("Hsrminer not extracted, extracting...")
            os.system('7za x hsrminer_neoscrypt_fork.zip -o' + FILEPATH + "/bin/NVIDIA-hsrminer-neoscrypt")
        if not os.path.exists(FILEPATH + "/bin/NVIDIA-EWBF"):
            ziplog.debug("EWBF not extracted, extracting...")
            os.system('7za x 0.3.4b.7z -o' + FILEPATH + "/bin/NVIDIA-EWBF")
        if not os.path.exists(FILEPATH + "/bin/NVIDIA-TPruvot"):
            ziplog.debug("CCminer TPruvot not extracted, extracting...")
            os.system('7za x ccminer-x86-2.2.7z -o' + FILEPATH + "/bin/NVIDIA-TPruvot")
        if not os.path.exists(FILEPATH + "/bin/NVIDIA-Alexis78cuda9"):
            ziplog.debug("CCminer Alexis78cuda9 not extracted, extracting...")
            os.system('7za x ccminer_x86.7z -o' + FILEPATH + "/bin/NVIDIA-Alexis78cuda9")
        if not os.path.exists(FILEPATH + "/bin/NVIDIA-Alexis78cuda8"):
            ziplog.debug("CCminer Alexis78cud8 not extracted, extracting...")
            os.system('7za x ccminer-hsr-alexis-x86-cuda8.7z -o' + FILEPATH + "/bin/NVIDIA-Alexis78cuda8")
        if not os.path.exists(FILEPATH + "/bin/NVIDIA-TPruvotcuda9"):
            ziplog.debug("CCminer TPruvotcuda9 not extracted, extracting...")
            os.system('7za x ccminer-x86-2.2.4-cuda9.7z -o' + FILEPATH + "/bin/NVIDIA-TPruvotcuda9")

        ziplog.debug("Miners extracted.")

        extracted = True

    return extracted

if __name__ == "__main__":
    # For testing purposes
    download_miners(miner_info)
    extract_miners()
    input("")