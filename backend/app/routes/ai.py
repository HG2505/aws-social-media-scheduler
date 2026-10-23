import os
import re
import json
import httpx
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from app.schemas import AICaptionRequest, AICaptionResponse

load_dotenv(override=True)

router = APIRouter(prefix="/api/ai", tags=["AI Copilot"])

def extract_hashtags(text: str) -> list[str]:
    """Trích xuất các hashtag từ văn bản kết quả."""
    tags = re.findall(r"#[A-Za-z0-9_À-ỹ]+", text)
    if not tags:
        tags = ["#SocialMedia", "#ContentCreator", "#DigitalMarketing"]
    return tags[:6]

async def call_gemini(prompt: str, api_key: str) -> str:
    """Gọi Google Gemini API (gemini-3.5-flash-lite)."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={api_key}"
    async with httpx.AsyncClient() as client:
        res = await client.post(
            url,
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.7, "maxOutputTokens": 600}
            },
            timeout=20.0
        )
        if res.status_code != 200:
            raise Exception(f"Gemini error {res.status_code}: {res.text}")
        data = res.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

async def call_openai_compatible(base_url: str, api_key: str, model: str, prompt: str) -> str:
    """Gọi bất kỳ dịch vụ nào tuân theo chuẩn OpenAI (DeepSeek, Groq, OpenAI, Together, v.v.)."""
    endpoint = f"{base_url.rstrip('/')}/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert social media content creator and copywriter. Always write engaging captions with suitable emojis and 3-5 relevant hashtags at the end."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 600
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(endpoint, headers=headers, json=payload, timeout=20.0)
        if res.status_code != 200:
            raise Exception(f"Provider error {res.status_code}: {res.text}")
        data = res.json()
        return data["choices"][0]["message"]["content"]

async def call_aws_bedrock(prompt: str) -> str:
    """Gọi Claude 3.5 Sonnet thông qua AWS Bedrock (sử dụng AWS SDK boto3)."""
    import boto3
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    client = boto3.client("bedrock-runtime", region_name=aws_region)
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 600,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    })
    response = client.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
        body=body
    )
    result = json.loads(response["body"].read())
    return result["content"][0]["text"]

@router.post("/generate-caption", response_model=AICaptionResponse)
async def generate_caption(request: AICaptionRequest):
    """Tự động sinh Caption & Hashtag qua AI linh hoạt."""
    load_dotenv(override=True)
    ai_provider = os.getenv("AI_PROVIDER", "auto").lower()
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    groq_key = os.getenv("GROQ_API_KEY", "")
    deepseek_key = os.getenv("DEEPSEEK_API_KEY", "")
    openai_key = os.getenv("OPENAI_API_KEY", "")
    custom_base = os.getenv("CUSTOM_AI_BASE_URL", "")
    custom_key = os.getenv("CUSTOM_AI_API_KEY", "")
    custom_model = os.getenv("CUSTOM_AI_MODEL", "")

    prompt = (
        f"Viết 1 đoạn caption bài đăng mạng xã hội cho nền tảng {request.platform} "
        f"về chủ đề '{request.topic}' theo phong cách {request.tone}. "
        f"Hãy chèn emoji phù hợp và kèm 4-5 hashtag liên quan ở cuối."
    )

    caption_text = ""
    try:
        # 1. Ưu tiên theo cấu hình thủ công CUSTOM
        if custom_base and custom_key:
            caption_text = await call_openai_compatible(
                custom_base, custom_key, custom_model or "gpt-3.5-turbo", prompt
            )
        # 2. Hoặc Google Gemini
        elif gemini_key and (ai_provider in ["gemini", "auto"]):
            caption_text = await call_gemini(prompt, gemini_key)
        # 3. Hoặc Groq (Siêu nhanh - Miễn phí)
        elif groq_key and (ai_provider in ["groq", "auto"]):
            caption_text = await call_openai_compatible(
                "https://api.groq.com/openai/v1", groq_key, "llama-3.3-70b-versatile", prompt
            )
        # 4. Hoặc DeepSeek
        elif deepseek_key and (ai_provider in ["deepseek", "auto"]):
            caption_text = await call_openai_compatible(
                "https://api.deepseek.com", deepseek_key, "deepseek-chat", prompt
            )
        # 5. Hoặc AWS Bedrock (Claude 3.5 Sonnet)
        elif ai_provider == "bedrock":
            caption_text = await call_aws_bedrock(prompt)
        # 6. Hoặc OpenAI
        elif openai_key and (ai_provider in ["openai", "auto"]):
            caption_text = await call_openai_compatible(
                "https://api.openai.com/v1", openai_key, "gpt-4o-mini", prompt
            )
        # 7. Fallback nếu chưa điền key nào
        else:
            caption_text = (
                f"🚀 [{request.tone}] Khám phá ngay về {request.topic}! "
                f"Giải pháp đột phá giúp bạn nâng tầm trải nghiệm trên {request.platform}. "
                f"Liên hệ ngay để nhận ưu đãi đặc biệt hôm nay! ✨"
            )
            return AICaptionResponse(
                caption=caption_text,
                hashtags=["#AWS", "#CloudDevelopment", f"#{request.topic.replace(' ', '')}", "#SocialMedia", "#Marketing"]
            )

        hashtags = extract_hashtags(caption_text)
        return AICaptionResponse(caption=caption_text, hashtags=hashtags)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Service Error: {str(e)}")
