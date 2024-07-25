#!/usr/bin/python3.7
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import sys
import os
import base64
from selenium.common.exceptions import TimeoutException
import boto3
from botocore.exceptions import NoCredentialsError
import subprocess
import json

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


def capture_map(url, outfile,wait):

    # WebDriverの設定
    # Seleniumのオプションを設定
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # ヘッドレスモードで実行
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Google Chromeのバイナリパスを指定
    options.binary_location = '/usr/bin/chromium-browser'  # 実際のパスに置き換えてください
    #options.binary_location = '/usr/bin/google-chrome'  # 実際のパスに置き換えてください
    # ChromeDriverをwebdriver_managerで管理
    #service = Service(ChromeDriverManager().install())
    service = Service('/usr/bin/chromedriver')

    # WebDriverを初期化
    driver = webdriver.Chrome(service=service, options=options)

    driver.set_window_size(1920,2600)
    # 待機時間をミリ秒で指定
    #wait_time_in_ms = 10000  
    try:
        driver.get(url)

        # 画像がロードされるまで待機
        time.sleep(5)  # ここで適切な待機時間を設定（5秒は例）
        
        # HTMLを取得
        html_content = driver.page_source
        print(html_content)

        screenshot_config = {
            "captureBeyondViewport": True,
            "clip": {
                "width": 1920,
                "height": 2600,
                "x": 0,
                "y": 0,
                "scale": 1.0,
            },
        }
        base64_image = driver.execute_cdp_cmd("Page.captureScreenshot", screenshot_config)
        # ファイル書き出し

        with open("/usr/amoeba/pub/crop/pdf/"+outfile, "wb") as fh:
            fh.write(base64.urlsafe_b64decode(base64_image["data"]))
            #driver.save_screenshot(output_file)
            print(f'Screenshot saved to {outfile}')
            
    finally:
        # WebDriverを終了
        if driver:
            driver.quit()
        
def main(url,outfile,wait):
    capture_map(url,outfile,wait)
    return 0

def s3upload(outfile):
    bucket_name = "dev-cropyield"
    s3_file_path = "/crop/pdf/"+outfile
    aws_access_key, aws_secret_key, region = get_aws_credentials()
    
    # アップロードを試みる
    upload_to_s3("/usr/amoeba/spool/"+outfile, bucket_name, s3_file_path, aws_access_key, aws_secret_key)
    
    os.remove('/usr/amoeba/spool/'+outfile)
    
    return bucket_name,s3_file_path

if __name__ == '__main__':
    contents = ["YIELD","PROG","WX"]
    state_tbl = '../state.tbl'
    state_df = pd.read_csv(state_tbl)
    num = 1
    for c in contents:
        n = f'{num:02}'
        url = 'http://prod-cropyield.wfc-internal.prod-aws-i.wni.com/crop/index.html?content='+c

        if c != "WX":
            outfile = n+'_'+c+'.png'
            wait = 5
            main(url,outfile,wait)
        else:
            
            for state in state_df.NAME.unique():
                
                urls = url + '&state='+state
                outfile = n+'_'+c+'_'+state+'_crop.png'
                wait = 1
                main(urls,outfile,wait)
                
                print(urls)
        num = num +1
        #bucket_name,fpath = main(url,outfile)
    #print("upload s3://"+bucket_name+'/'+fpath)
