import os
import boto3
import argparse
from configparser import ConfigParser

def loginToAWS(profile):
    if profile:
        aws_session = boto3.Session(profile_name=profile)
    else:
        aws_session = boto3.Session(profile_name="default")
    return aws_session

def setAwsCredentials(aws_session, profile):
    profile = profile + "_sts"
    sts_client = aws_session.client('sts')
    iam_client = aws_session.client('iam')
    response = iam_client.list_mfa_devices()
    mfa_serial_number = response['MFADevices']
    mfa_serial_number = mfa_serial_number[0]['SerialNumber']
    aws_config = ConfigParser()
    token_code = input("Put the token code from your MFA Device: ")
    response =  sts_client.get_session_token(SerialNumber=mfa_serial_number, TokenCode=token_code)
    temp_credentials = response['Credentials']
    aws_config.read(os.getenv("HOME") + "/.aws/credentials")
    sts_config = ConfigParser()
    sts_config.read(os.getenv("HOME") + "/.aws/credentials")
    sections = aws_config.sections()
    if not profile in sections:
        sts_config.add_section(profile)
    sts_config.set(profile, "aws_access_key_id", temp_credentials['AccessKeyId'])
    sts_config.set(profile, "aws_secret_access_key", temp_credentials['SecretAccessKey'])
    sts_config.set(profile, "aws_session_token", temp_credentials['SessionToken'])
    with open(os.getenv("HOME") + "/.aws/credentials", "w") as aws_config:
        sts_config.write(aws_config)
    print("Temporary credentials created under profile", profile)

if __name__ == "__main__":
    mode = 0o775
    parser = argparse.ArgumentParser(description='Obtain and set temporary credentials to aws')
    parser.add_argument('-p', '--profile', type=str, help='Define profile to login to AWS')
    args = parser.parse_args()
    session = loginToAWS(args.profile)
    setAwsCredentials(session, args.profile)