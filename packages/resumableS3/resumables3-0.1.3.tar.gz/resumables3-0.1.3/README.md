# resumableS3
## Introduction
This software is mainly for resumable S3 cp download. When using S3 cp to download a very large file, original [AWS S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) may fail and just report an error `("Connection broken: ConnectionResetError(104, 'Connection reset by peer')", ConnectionResetError(104, 'Connection reset by peer'))`, without writing the file to output.

## Installation
Use pip to install
```bash
pip install resumables3;
```
Better to install in a new envs.


## Usage
Only two parameter is mandatory: `-i/--input` and `-o/--output`
```
Usage: rs3 [OPTIONS]

Options:
  -i, --input TEXT       S3 link, must be a specific downloadable object [required]
  -o, --output TEXT      Path to output  [required]
  -t, --temp TEXT        Path to the record file, default : download_progress.txt in output directory
  -w, --workers INTEGER  Max workder for download, default: max CPU threads in your system
  --chunk-size INTEGER   Chunk size for parallel download in MB
  --id TEXT              AWS access key id, default: None (anonymous)
  --key TEXT             AWS secert access key, default: None (anonymous)
  --region-name TEXT     AWS region name, default: None
  --version              Show the version and exit.
  --help                 Show this message and exit.
```

## Example
```
rs3 \
-i s3://human-pangenomics/working/HPRC_PLUS/HG01109/assemblies/year1_freeze_assembly_v2/HG01109.maternal.f1_assembly_v2.fa.gz \
-o ./output 
```

## Citation
Just cite this repositroy.

