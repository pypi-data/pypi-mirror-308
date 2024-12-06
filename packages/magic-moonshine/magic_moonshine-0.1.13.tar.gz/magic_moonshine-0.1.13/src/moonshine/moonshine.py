# moonshine.py
import os
import urllib.parse
import requests
import mimetypes
from typing import Dict, Union, Optional, Callable, Any
import boto3
from botocore.config import Config
from concurrent.futures import ThreadPoolExecutor
import cv2
import math

# Private configuration
_CONFIG = {
    'api_token': None
}

_CREDENTIALS = {
    "aws_access_key_id": "AKIAYT3WIFOIJO6OUCHV",
    "aws_secret_access_key": "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",
}

_S3_CONFIG_MEDIA = {
    'bucket_name': 'moonshine-media',
    'region': 'us-east-1'
}

_S3_CONFIG_LARGE_MEDIA = {
    'bucket_name': 'moonshine-large-media',
    'region': 'us-east-1'
}

_MULTIPART_UPLOAD_THRESHOLD = 50 * 1024 * 1024  # 50 MB
_PART_SIZE = 15 * 1024 * 1024  # 15 MB
_MAX_CONCURRENT_UPLOADS = 5

# Private helper functions
def _is_video(filename: str) -> bool:
    """Determine if a file is a video based on its extension."""
    video_extensions = {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv'}
    return os.path.splitext(filename.lower())[1] in video_extensions

def _get_video_info(filename: str) -> tuple[Optional[float], Optional[float]]:
    """Get video duration in seconds and FPS using OpenCV."""
    try:
        video = cv2.VideoCapture(filename)
        if not video.isOpened():
            return None, None
            
        fps = video.get(cv2.CAP_PROP_FPS)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        video.release()
        
        return duration, fps
        
    except Exception as e:
        print(f"Error reading video file: {e}")
        return None, None
    
def _does_bucket_exist(bucket: str) -> bool:
    """
    Check if a bucket exists in the Moonshine API.
    
    Args:
        bucket (str): The bucket to check
    
    Returns:
        bool: True if the bucket exists, False otherwise
        
    Raises:
        ValueError: If API token is not configured
        requests.RequestException: If the API request fails
    """
    if not _CONFIG['api_token']:
        raise ValueError("API token not configured. Call moonshine.config(API='your-token') first.")
    
    base_url = "https://www.moonshine-edge-compute.com/does-group-exist"
    
    params = {
        'projectid': _CONFIG['api_token'] + bucket
    }
    
    # Construct URL with properly encoded parameters
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('exists', False)
    except requests.RequestException as e:
        raise requests.RequestException(f"API request failed: {str(e)}")

def _get_bucket_config(file_path: str) -> Dict:
    """Determine which bucket to use based on file size and type."""
    file_size = os.path.getsize(file_path)
    content_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
    
    if content_type.startswith('video/'):
        return _S3_CONFIG_LARGE_MEDIA if file_size > 1024**3 else _S3_CONFIG_MEDIA
    else:
        return _S3_CONFIG_MEDIA
    
def _get_file_info(file_path: str) -> tuple[int, str]:
    """Get the file size and content type of a file."""
    file_size = os.path.getsize(file_path)
    content_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
    return file_size, content_type

def _upload_part(s3_client: Any, bucket: str, key: str, upload_id: str, 
                part_number: int, data: bytes) -> Dict:
    """Upload a single part of a multipart upload."""
    response = s3_client.upload_part(
        Bucket=bucket,
        Key=key,
        UploadId=upload_id,
        PartNumber=part_number,
        Body=data
    )
    return {
        'PartNumber': part_number,
        'ETag': response['ETag']
    }

async def _pre_upload_media(filename: str, project_id: str, duration: Optional[float] = None, 
                          fps: Optional[int] = None, user_id: str = "api") -> Optional[str]:
    """Call the pre-upload API to get a file ID."""
    base_url = 'https://moonshine-edge-compute.com/media-pre-upload'
    encoded_filename = urllib.parse.quote(filename)
    
    url = f"{base_url}?userid={user_id}&filename={encoded_filename}&projectid={project_id}"
    if duration is not None:
        url += f"&duration={math.ceil(duration)}"
    if fps is not None:
        url += f"&fps={round(fps)}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['key'] if data.get('status') == 'success' and 'key' in data else None
    except requests.RequestException:
        return None
    
async def _get_signed_upload(filename: str, project_id: str, duration: Optional[float] = None, 
                          fps: Optional[int] = None, content_type: Optional[str] = None, file_size: Optional[int] = None, sender: str = "api") -> Optional[tuple[str, str]]:
    """Call the pre-upload API to get a file ID."""
    base_url = 'https://moonshine-edge-compute.com/api-pre-upload'
    
    url = f"{base_url}?sender={sender}&filename={urllib.parse.quote(filename)}&projectid={project_id}"
    if duration is not None:
        url += f"&duration={math.ceil(duration)}"
    if fps is not None:
        url += f"&fps={round(fps)}"
    if content_type is not None:
        url += f"&content={urllib.parse.quote(content_type)}"
    if file_size is not None:
        url += f"&filesize={file_size}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['key'], data['url']
    except requests.RequestException:
        return None
    
async def _get_multipart_upload_urls(filename: str, project_id: str, part_count: int, 
                                   duration: Optional[float] = None, fps: Optional[int] = None, 
                                   content_type: Optional[str] = None, file_size: Optional[int] = None) -> Optional[tuple[str, list[str]]]:
    """Get signed URLs for all parts of a multipart upload."""
    base_url = 'https://moonshine-edge-compute.com/api-multipart-init'
    
    url = f"{base_url}?filename={urllib.parse.quote(filename)}&projectid={project_id}&parts={part_count}"
    if duration is not None:
        url += f"&duration={math.ceil(duration)}"
    if fps is not None:
        url += f"&fps={round(fps)}"
    if content_type is not None:
        url += f"&content={urllib.parse.quote(content_type)}"
    if file_size is not None:
        url += f"&filesize={file_size}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['key'], data['urls']
    except requests.RequestException:
        return None

async def _complete_multipart_upload(file_id: str, project_id: str, parts: list[dict]) -> bool:
    """Signal the server to complete a multipart upload."""
    base_url = 'https://moonshine-edge-compute.com/api-multipart-complete'
    
    try:
        response = requests.post(
            base_url,
            json={
                'key': file_id,
                'projectid': project_id,
                'parts': parts
            }
        )
        response.raise_for_status()
        return response.json().get('status') == 'success'
    except requests.RequestException:
        return False

async def _abort_multipart_upload(file_id: str, project_id: str) -> bool:
    """Signal the server to abort a multipart upload."""
    base_url = 'https://moonshine-edge-compute.com/api-multipart-abort'
    
    try:
        response = requests.post(
            base_url,
            json={
                'key': file_id,
                'projectid': project_id
            }
        )
        response.raise_for_status()
        return response.json().get('status') == 'success'
    except requests.RequestException:
        return False

# Public functions
def moo() -> None:
    """Print a cow saying hello."""
    print("  __________________")
    print(" < MOO, its Harold! >")
    print("  ------------------")
    print("         \\   ^__^")
    print("          \\  (oo)\\_______")
    print("             (__)\\       )\\/\\")
    print("                 ||----w |")
    print("                 ||     ||")

def config(API: str) -> None:
    """
    Configure the Moonshine client with your API token.
    
    Args:
        API (str): Your Moonshine API token
    """
    base_url = "https://www.moonshine-edge-compute.com/check-token"
    
    params = {
        'token': API,
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        if (response.json()["valid"]):
            _CONFIG['api_token'] = API
        else:
            raise ValueError("Invalid API token")
    except requests.RequestException as e:
        raise requests.RequestException(f"Could not validate your token: {str(e)}")

def create(index: str) -> Dict:
    """
    Create a new Moonshine index.
    
    Args:
        bucket (str): The project/bucket to create
    
    Returns:
        Dict: The API response
        
    Raises:
        ValueError: If API token is not configured
        requests.RequestException: If the API request fails
    """
    if not _CONFIG['api_token']:
        raise ValueError("API token not configured. Call moonshine.config(API='your-token') first.")
    
    if _does_bucket_exist(index):
        raise ValueError(f"Index {index} already exists.")
    
    base_url = "https://www.moonshine-edge-compute.com/create-media-group"
    
    params = {
        'userid': _CONFIG['api_token'],
        'projectname': _CONFIG['api_token'] + index,
        'projectdescription': "api",
        'from': "api",
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise requests.RequestException(f"API request failed: {str(e)}")

def search(index: str, query: str) -> Dict:
    """
    Search media using the Moonshine API.
    
    Args:
        index (str): The project/bucket ID to search in
        query (str): The search query
    
    Returns:
        Dict: The API response
        
    Raises:
        ValueError: If API token is not configured
        requests.RequestException: If the API request fails
    """
    if not _CONFIG['api_token']:
        raise ValueError("API token not configured. Call moonshine.config(API='your-token') first.")
    
    base_url = "https://www.moonshine-edge-compute.com/media-query"
    
    params = {
        'projectid': _CONFIG['api_token'] + index,
        'api': _CONFIG['api_token'],
        'query': query,
        'numargs': 5,
        'threshold': 15
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise requests.RequestException(f"API request failed: {str(e)}")
    
def interpret(index: str, prompt: str) -> Dict:
    """
    Generate responses to open ended prompts using the Moonshine API.
    
    Args:
        index (str): The project/bucket ID to search in
        prompt (str): The prompt query
    
    Returns:
        dict: The generated response
        
    Raises:
        ValueError: If API token is not configured
        requests.RequestException: If the API request fails
    """
    if not _CONFIG['api_token']:
        raise ValueError("API token not configured. Call moonshine.config(API='your-token') first.")
    
    base_url = "https://www.moonshine-edge-compute.com/search-and-generate"
    
    params = {
        'projectid': _CONFIG['api_token'] + index,
        'prompt': prompt,
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise requests.RequestException(f"API request failed: {str(e)}")

async def upload(file_path: str, index: str, 
                progress_callback: Optional[Callable[[float], None]] = None) -> Union[str, bool]:
    """
    Upload a file using a pre-signed URL with progress tracking.
    
    Args:
        file_path: Path to the file to upload
        index: Project name/ID
        progress_callback: Optional callback function to report upload progress
        
    Returns:
        str: File ID if upload successful
        bool: False if upload failed
        
    Raises:
        ValueError: If API token is not configured or project doesn't exist
    """
    if not _CONFIG['api_token']:
        raise ValueError("API token not configured. Call moonshine.config(API='your-token') first.")
    
    if not _does_bucket_exist(index):
        raise ValueError(f"Index {index} doesn't exist. Create it first. Hint: moonshine.create('{index}')")
    
    index = _CONFIG['api_token'] + index
    
    try:
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        # Get file metadata
        duration = None
        fps = None
        file_size, content_type = _get_file_info(file_path)
        if _is_video(file_path) and content_type.startswith('video/'):
            duration, fps = _get_video_info(file_path)
            print(f"Video duration: {duration:.2f} seconds")
            print(f"Video FPS: {fps:.2f}")
        else:
            raise ValueError("Only video files are supported.")
        
        if file_size < _MULTIPART_UPLOAD_THRESHOLD:
            # Single-part upload
            file_upload = await _get_signed_upload(filename, index, duration, fps, content_type, file_size)
            if not file_upload:
                raise ValueError("Unable to index media, insufficient account balance.")
            
            file_id, signed_upload_url = file_upload
            
            with open(file_path, 'rb') as file:
                response = requests.put(
                    signed_upload_url,
                    data=_ProgressFileReader(file, file_size, progress_callback),
                    headers={'Content-Type': content_type}
                )
                response.raise_for_status()
        else:
            # Calculate number of parts
            part_count = math.ceil(file_size / _PART_SIZE)
            
            # Get signed URLs for all parts
            upload_info = await _get_multipart_upload_urls(
                filename, index, part_count, duration, fps, content_type, file_size
            )
            if not upload_info:
                raise ValueError("Unable to initialize multipart upload.")
            
            file_id, signed_urls = upload_info
            uploaded_bytes = 0
            parts = []
            
            with ThreadPoolExecutor(max_workers=_MAX_CONCURRENT_UPLOADS) as executor:
                futures = []
                
                with open(file_path, 'rb') as file:
                    for part_number, signed_url in enumerate(signed_urls, 1):
                        data = file.read(_PART_SIZE)
                        if not data:
                            break
                        
                        future = executor.submit(
                            _upload_part_with_signed_url,
                            requests.Session(),
                            signed_url,
                            part_number,
                            data,
                            content_type
                        )
                        futures.append((future, len(data)))
                
                for future, part_size in futures:
                    try:
                        etag = future.result()
                        parts.append({
                            'PartNumber': len(parts) + 1,
                            'ETag': etag
                        })
                        uploaded_bytes += part_size
                        if progress_callback:
                            progress_callback(uploaded_bytes / file_size * 100)
                    except Exception as e:
                        await _abort_multipart_upload(file_id, index)
                        raise e
            
            # Complete multipart upload
            if not await _complete_multipart_upload(file_id, index, parts):
                raise ValueError("Failed to complete multipart upload")
        
        if progress_callback:
            progress_callback(100)
        return file_id
        
    except Exception as e:
        print(f"Upload failed: {str(e)}")
        if progress_callback:
            progress_callback(-1)
        return False

class _ProgressFileReader:
    """Wrapper for file object that reports read progress."""
    def __init__(self, file, total_size, callback=None):
        self.file = file
        self.total_size = total_size
        self.callback = callback
        self.bytes_read = 0
        
    def read(self, size=-1):
        data = self.file.read(size)
        self.bytes_read += len(data)
        if self.callback:
            self.callback(self.bytes_read / self.total_size * 100)
        return data
        
async def _upload_part_with_signed_url(
    session: requests.Session,
    signed_url: str,
    part_number: int,
    data: bytes,
    content_type: str
) -> str:
    """Upload a single part using a signed URL."""
    response = session.put(
        signed_url,
        data=data,
        headers={'Content-Type': content_type}
    )
    response.raise_for_status()
    return response.headers['ETag']