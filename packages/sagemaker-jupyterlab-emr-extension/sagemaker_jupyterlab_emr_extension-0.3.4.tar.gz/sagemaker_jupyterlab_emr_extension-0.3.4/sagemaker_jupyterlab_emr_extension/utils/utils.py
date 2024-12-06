import logging
import traceback

import botocore

DOMAIN = "amazonaws.com"
# China regions use different domain: https://docs.amazonaws.cn/en_us/aws/latest/userguide/endpoints-Ningxia.html
CHINA_DOMAIN = "amazonaws.com.cn"
CHINA_REGION_PREFIX = "cn-"


def get_credential(role_arn, region_name):
    session = botocore.session.get_session()
    if region_name.startswith(CHINA_REGION_PREFIX):
        endpoint_url = f"https://sts.{region_name}.{CHINA_DOMAIN}"
    else:
        endpoint_url = f"https://sts.{region_name}.{DOMAIN}"
    sts_client = session.create_client("sts", endpoint_url=endpoint_url)

    try:
        credential = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName="SagemakerAssumableSession",
        )
    except (
        botocore.exceptions.BotoCoreError,
        botocore.exceptions.ClientError,
    ) as error:
        logging.error(
            "Error in get credential in EMR {}".format(traceback.format_exc())
        )
        raise error
    return credential["Credentials"]
