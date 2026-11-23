from app.config import settings
import boto3
from botocore.config import Config
from botocore.errorfactory import ClientError
import asyncio


class StorageService:
    def __init__(self):
        self.client = boto3.client(
            's3',
            endpoint_url=settings.s3_endpoint_url,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.s3_region,
            config=Config(
                signature_version="s3v4"
            )
        )

        self.bucket = settings.s3_bucket_name

    async def upload_file(
        self,
        file,
        object_key: str,
        content_type: str
    ):
        await asyncio.to_thread(
            self.client.upload_fileobj,
            file,
            self.bucket,
            object_key,
            ExtraArgs={
                "ContentType": content_type
            }
        )

    async def generate_presigned_url(
        self,
        object_key: str,
        expires_in: int = 3600
    ) -> str:
        return await asyncio.to_thread(
            self.client.generate_presigned_url,
            "get_object",
            Params={
                "Bucket": self.bucket,
                "Key": object_key
            },
            ExpiresIn=expires_in
        )

    async def delete_file(self, object_key: str):
        await asyncio.to_thread(
            self.client.delete_object,
            Bucket=self.bucket,
            Key=object_key
        )

    async def file_exists(self, object_key: str) -> bool:
        try:
            await asyncio.to_thread(
                self.client.head_object,
                Bucket=self.bucket,
                Key=object_key
            )
            return True

        except ClientError as e:
            if e.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
                return False

            raise


storage = StorageService()
