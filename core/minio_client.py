import asyncio
from minio import Minio
from minio.error import S3Error
from core.config import settings

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE
)

def _upload_file(bucket_name: str, object_name: str, data, length, content_type):
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)
    minio_client.put_object(bucket_name, object_name, data, length, content_type=content_type)
    return f"http://{settings.MINIO_ENDPOINT}/{bucket_name}/{object_name}"

async def upload_file_to_minio(bucket_name: str, object_name: str, data, length, content_type):
    return await asyncio.to_thread(_upload_file, bucket_name, object_name, data, length, content_type)
