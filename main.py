import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# สร้าง FastAPI แทน MCP แบบเก่า เพื่อให้ Render รันได้
app = FastAPI(title="Claude Meta AI MCP - Page 61595100133102")

JOBS_DB = {}

@app.get("/")
def home():
    return {
        "status": "live",
        "service": "Claude Meta AI Auto Poster",
        "page_id": "61595100133102",
        "message": "MCP Server is running! Use /tools to see available tools",
        "tools": ["create_video_job", "check_video_status", "approve_and_post"]
    }

@app.get("/tools")
def get_tools():
    return {
        "tools": [
            {
                "name": "create_video_job",
                "description": "สั่ง Meta AI สร้างวิดีโอสำหรับโพสต์ลงเพจ",
                "params": ["prompt", "style", "aspect_ratio", "caption"]
            },
            {
                "name": "check_video_status",
                "description": "เช็คสถานะวิดีโอ",
                "params": ["job_id"]
            },
            {
                "name": "approve_and_post_to_facebook",
                "description": "อนุมัติและโพสต์ลง Facebook Page",
                "params": ["job_id", "final_caption", "page_id"]
            }
        ]
    }

@app.post("/create_video_job")
def create_video_job(prompt: str, style: str = "realistic", aspect_ratio: str = "16:9", caption: str = ""):
    import uuid
    from datetime import datetime
    job_id = str(uuid.uuid4())[:8]
    JOBS_DB[job_id] = {
        "job_id": job_id,
        "prompt": prompt,
        "style": style,
        "aspect_ratio": aspect_ratio,
        "caption": caption or prompt,
        "status": "queued",
        "created_at": datetime.now().isoformat(),
        "page_id": "61595100133102"
    }
    return {"job_id": job_id, "status": "queued", "message": f"รับงานแล้ว: {prompt}"}

@app.get("/check/{job_id}")
def check_video_status(job_id: str):
    job = JOBS_DB.get(job_id)
    if not job:
        return JSONResponse(status_code=404, content={"error": f"ไม่พบงาน {job_id}"})
    return job

# ให้ Render รันได้
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
