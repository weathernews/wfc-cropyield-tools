#!/usr/bin/env python 
import os
import img2pdf
from PIL import Image # img2pdfと一緒にインストールされた
import pandas as pd
import sys
import os
import base64
from selenium.common.exceptions import TimeoutException
import boto3
from botocore.exceptions import NoCredentialsError
import subprocess
import json

def s3upload(outfile):
    bucket_name = "prod-cropyield"
    s3_file_path = "crop/pdf/output.pdf"
    aws_access_key, aws_secret_key, region = get_aws_credentials()
    
    # アップロードを試みる
    upload_to_s3("/usr/amoeba/pub/crop/pdf/output.pdf", bucket_name, s3_file_path, aws_access_key, aws_secret_key)
    
    #os.remove("/usr/amoeba/pub/crop/pdf/"+outfile)
    
    return bucket_name,s3_file_path

def get_aws_credentials():
    try:
        # aws configure list コマンドを実行し、JSON形式で出力を取得
        output = subprocess.check_output(['aws', 'configure', 'list'], universal_newlines=True)

        # 出力をJSONとしてパース
        config_data = json.loads(output)

        # 認証情報を取得
        access_key = config_data.get('aws_access_key_id')
        secret_key = config_data.get('aws_secret_access_key')
        region = config_data.get('region')

        return access_key, secret_key, region

    except subprocess.CalledProcessError as e:
        print(f"コマンドがエラーで終了しました。エラーコード: {e.returncode}")
        return None, None, None
    except json.JSONDecodeError as e:
        #print(f"JSONの解析中にエラーが発生しました。エラーメッセージ: {e}")
        return None, None, None


def upload_to_s3(local_file_path, bucket_name, s3_file_path, aws_access_key, aws_secret_key):
    """
    Uploads a local file to an S3 bucket.
    :param local_file_path: Path to the local file to upload.
    :param bucket_name: S3 bucket name.
    :param s3_file_path: Path and filename to store in S3.
    :param aws_access_key: Your AWS Access Key ID.
    :param aws_secret_key: Your AWS Secret Access Key.
    :return: True if the file was uploaded successfully, else False.
    """
    try:
        # Create an S3 client
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

        # Upload the file
        s3.upload_file(local_file_path, bucket_name, s3_file_path)

        print("File uploaded successfully.")
        return True
    except NoCredentialsError:
        print("Credentials not available.")
        return False


if __name__ == '__main__':
    pdf_FileName = "../pdf/output.pdf" # 出力するPDFの名前
    png_Folder = "../pdf/" # 画像フォルダ
    extension  = ".png" # 拡張子がPNGのものを対象
    
    with open(pdf_FileName,"wb") as f:
    #    # 画像フォルダの中にあるPNGファイルを取得し配列に追加、バイナリ形式でファイルに書き込む
        f.write(img2pdf.convert([Image.open(png_Folder+j).filename for j in os.listdir(png_Folder)if j.endswith(extension)]))
    s3upload(pdf_FileName)
