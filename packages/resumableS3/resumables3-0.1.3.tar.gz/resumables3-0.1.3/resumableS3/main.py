import boto3
from botocore import UNSIGNED
from botocore.config import Config
from concurrent.futures import ThreadPoolExecutor
import os
from tqdm import tqdm
import click


def load_downloaded_chunks():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return set(tuple(map(int, line.strip().split('-'))) for line in f)
    return set()


def record_chunk_downloaded(start_byte, end_byte):
    with open(PROGRESS_FILE, 'a') as f:
        f.write(f"{start_byte}-{end_byte}\n")


def download_chunk(s3_bucket, s3_object_key, start_byte, end_byte, local_file_path):
    try:
        response = s3.get_object(Bucket=s3_bucket, Key=s3_object_key, Range=f"bytes={start_byte}-{end_byte}")
        with open(local_file_path, 'r+b') as f:
            f.seek(start_byte)
            f.write(response['Body'].read())
        # print(f"Chunk {start_byte}-{end_byte} downloaded.")
        # update with tqdm
        record_chunk_downloaded(start_byte, end_byte)

    except Exception as e:
        print(f"An error occurred while downloading chunk {start_byte}-{end_byte}: {e}")


def download_file_with_resume(s3_bucket: str, s3_object_key: str, local_file_path: str, workers: int):
    try:
        # obtain metadata
        metadata = s3.head_object(Bucket=s3_bucket, Key=s3_object_key)
        file_size = metadata['ContentLength']

        # create file
        if not os.path.exists(local_file_path):
            with open(local_file_path, 'wb') as f:
                f.truncate(file_size)
        
        # load downloaded info
        downloaded_chunks = load_downloaded_chunks()

        # parallel download
        with ThreadPoolExecutor(max_workers = workers) as executor:
            futures = []
            for start in range(0, file_size, CHUNK_SIZE):
                end = min(start + CHUNK_SIZE - 1, file_size - 1)

                # skip downloaded
                if (start, end) in downloaded_chunks:
                    continue

                # download missing
                future = executor.submit(download_chunk, s3_bucket, s3_object_key, start, end, local_file_path)
                futures.append(future)
            
            pbar = tqdm(total=len(futures), desc="Downloading sectors", unit="sector")

            # wait all till completed
            for i in range(len(futures)):
                futures[i].add_done_callback(lambda p: pbar.update(1))
                futures[i].result()

        print(f"File downloaded to {local_file_path}")
            
    except Exception as e:
        print(f"An error occurred: {e}")



def split_s3(link: str) -> tuple:
    s = link.split('/')
    clean = list()
    for i in s:
        if i and i != "s3:":
            clean.append(i)

    if len(clean) < 2:
        raise ValueError("Please check the s3 input link")

    return (clean[0], clean[-1], '/'.join(clean[1: ]))



def config_s3(id, key, region) -> None:
    global s3
    if not(id) and not(key):
        if region:
            s3 = boto3.client("s3", config = Config(signature_version=UNSIGNED), region_name = region)
        else:
            s3 = boto3.client("s3", config = Config(signature_version=UNSIGNED))
    elif id and key:
        if region:
            s3 = boto3.client("s3", aws_access_key_id = id, aws_secret_access_key = key, region_name = region)
        else:
            s3 = boto3.client("s3", aws_access_key_id = id, aws_secret_access_key = key)
    else:
        raise ValueError("Please provide valid id and key or download anonymously")




@click.command()
@click.option("-i", "--input", required = True, help = "S3 link, must be a specific downloadable object")
@click.option("-o", "--output", required = True, help = "Path to output")
@click.option("-t", "--temp", default = "SAMEASOUTPUT", help = "Path to the record file, default : download_progress.txt in output directory")
@click.option("-w", "--workers", default = os.cpu_count(), help = "Max workder for download, default: max CPU threads in your system")
@click.option("--chunk-size", default = 25, help = "Chunk size for parallel download in MB")
@click.option("--id", default = None, help = "AWS access key id, default: None (anonymous)")
@click.option("--key", default = None, help = "AWS secert access key, default: None (anonymous)")
@click.option("--region-name", default = None, help = "AWS region name, default: None")
@click.version_option(version="0.1.3", prog_name = r"s3 resumable download (s3r), based on Python 3.7+")
def main(input, output, temp, workers, chunk_size, id, key, region_name):
    s3_bucket_name, target_file_name, s3_object_key = split_s3(input)
    real_output = os.path.join(os.path.abspath(output), target_file_name)

    global PROGRESS_FILE
    if temp == "SAMEASOUTPUT":
        PROGRESS_FILE = os.path.join(os.path.abspath(output), "download_progress.txt")
    else:
        if os.path.isfile(temp):
            PROGRESS_FILE = os.path.abspath(temp)
        else:
            PROGRESS_FILE = os.path.join(os.path.abspath(temp), "download_progress.txt")

    global CHUNK_SIZE 
    CHUNK_SIZE = chunk_size * 1024 * 1024
    
    print("Configuring s3 download.")
    config_s3(id, key, region_name)
    print("Configure of s3 download, DONE")
    
    print("Starting download")
    download_file_with_resume(s3_bucket_name, s3_object_key, real_output, workers)
    




if __name__ == "__main__":
    main()
