from crypto_utils import ecc_signature_create
import base64
import argparse
import time

def write_lic_data(fn, key, data):
    lines = ["FO extractor license file", "-" * 50]
    for lic, value in data.items():
        lines.append(f"{lic}={value}")
    lines.append("-" * 50)
    lines.append(base64.b64encode(ecc_signature_create(key, "\n".join(lines).encode("utf-8"))).decode("utf-8"))
    with open(fn, "wb") as f:
        f.write("\n".join(lines).encode("utf-8"))

parser = argparse.ArgumentParser()
parser.add_argument("--exp-days", type=int)
args = parser.parse_args()

if args.exp_days is not None:
    exp_date = time.strftime("%Y-%m-%d", time.localtime(time.time() + args.exp_days * 86400))
else:
    exp_date = input("LIC_EXP_DATE (YYYY-MM-DD): ")

private_key = """-----BEGIN PRIVATE KEY-----
MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgD171hE24St0NOTP4
FIU9dM1uKl1UPoUqN1OGehhOpyehRANCAARRpi+H0nQWOxvN43fpfh8gN1Y1et+d
gKyeC1ojhnngsCPAIRELdQ/HzciKD/hqBVxJddFbi9verUYwnTkvWmCk
-----END PRIVATE KEY-----"""

write_lic_data("lic.txt", private_key, {"LIC_EXP_DATE": exp_date})
