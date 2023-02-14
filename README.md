
# Temporary Credentials to AWS Using MFA

The script will read the credentials set in the .aws/credentials file and connect to your account, create a new profile with temporary credentials using your associated MFA device.

## Appendix

The script logic only tolerates one associated MFA device.
If you don't put a profile using flag -p or --profile, the script will use default profile.

Your profile must be able to list mfa devices.

[manage iam mfa policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_examples_iam_mfa-selfmanage.html)


## Tech Requirements

**Python version:** 3.x

**Packages:** boto3, configparse, argparse


## Run Script

```bash
   python3 temporary-credentials.py -p myProfile
```

```bash
  Put the token code from your MFA Device: 768982
```

```bash
  Temporary credentials created under profile myProfile_sts
```

## Support

For support, email matiasquin@gmail.com.


## Feedback

If you have any feedback, please reach out to me at matiasquin@gmail.com

