import yaml
import boto3

with open("s3.yml", "r") as f:
    s3_config = yaml.safe_load(f)

session = boto3.session.Session(
    aws_access_key_id=s3_config["aws_access_key_id"],
    aws_secret_access_key=s3_config["aws_secret_access_key"],
    region_name=s3_config["region"]
)

s3 = session.client("s3", endpoint_url=s3_config["endpoint"], use_ssl=s3_config["secure"])


def download_s3_file(bucket: str, key: str, target_file: str):
    s3.download_file(bucket, key, target_file)
