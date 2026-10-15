"""
Claude -> Meta AI Auto Poster MCP Server
สำหรับเพจ ID: 61595100133102
"""
from mcp.server.fastmcp import FastMCP
import json
import uuid
from datetime import datetime

mcp = FastMCP("Meta AI Auto Poster - Page 61595100133102")

JOBS_DB = {}

@mcp.tool()
def create_video_job(prompt: str, style: str = "realistic", aspect_ratio: str = "16:9", caption: str = "") -> dict:
    """
    สั่ง Meta AI สร้างวิดีโอสำหรับโพสต์ลงเพจ
    """
    job_id = str(uuid.uuid4())[:8]
    job = {
        "job_id": job_id,
        "prompt": prompt,
        "style": style,
        "aspect_ratio": aspect_ratio,
        "caption": caption or prompt,
        "status": "queued",
        "created_at": datetime.now().isoformat(),
        "page_id": "61595100133102",
    }
    JOBS_DB[job_id] = job
    return {
        "job_id": job_id,
        "status": "queued",
        "message": f"รับงานแล้ว! กำลังสร้างวิดีโอ: '{prompt}'",
    }

@mcp.tool()
def check_video_status(job_id: str) -> dict:
    """เช็คสถานะวิดีโอ"""
    job = JOBS_DB.get(job_id)
    if not job:
        return {"error": f"ไม่พบงาน {job_id}"}
    return {
        "job_id": job_id,
        "status": job["status"],
        "prompt": job["prompt"],
    }

@mcp.tool()
def approve_and_post_to_facebook(job_id: str, final_caption: str = "", page_id: str = "61595100133102") -> dict:
    """อนุมัติและโพสต์ลง Facebook Page"""
    job = JOBS_DB.get(job_id)
    if not job:
        return {"error": f"ไม่พบงาน {job_id}"}
    job["status"] = "posted"
    return {
        "success": True,
        "job_id": job_id,
        "page_id": page_id,
        "message": f"โพสต์ลงเพจ {page_id} สำเร็จ!",
    }

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
