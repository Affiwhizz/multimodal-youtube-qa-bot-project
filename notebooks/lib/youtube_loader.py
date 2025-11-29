"""
youtube_loader.py

Transcript loading + curated collections for MindDish.ai
Local-first, YouTube-second strategy.
"""

from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
import json
import logging
from time import sleep
from urllib.parse import urlparse, parse_qs

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

# -----------------------------------------------------------------------------
# Optional YouTubeTranscriptApi import
# -----------------------------------------------------------------------------

try:
    from youtube_transcript_api import (
        YouTubeTranscriptApi,
        TranscriptsDisabled,
        NoTranscriptFound,
        CouldNotRetrieveTranscript,
    )
    YT_AVAILABLE = True
except ImportError:
    YT_AVAILABLE = False
    logger.warning("YouTubeTranscriptApi not installed. Live transcripts disabled.")

# -----------------------------------------------------------------------------
# Directory setup
# -----------------------------------------------------------------------------

DATA_DIR = Path("data")
TRANSCRIPTS_DIR = DATA_DIR / "transcripts"

TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Video ID extractor
# -----------------------------------------------------------------------------

def extract_video_id(video_url_or_id: str) -> str:
    """Extract video ID from URL or return raw ID."""
    if "youtube.com" not in video_url_or_id and "youtu.be" not in video_url_or_id:
        return video_url_or_id.strip()

    parsed = urlparse(video_url_or_id)

    # Standard URL
    if "youtube.com" in parsed.netloc:
        params = parse_qs(parsed.query)
        if "v" in params:
            return params["v"][0]

    # Short URL
    if "youtu.be" in parsed.netloc:
        return parsed.path.lstrip("/")

    # Fallback
    return parsed.path.strip("/").split("/")[-1]

# -----------------------------------------------------------------------------
# Local transcript loading/saving
# -----------------------------------------------------------------------------

def load_local_transcript(video_id: str) -> Optional[str]:
    path = TRANSCRIPTS_DIR / f"{video_id}.txt"
    if not path.exists():
        return None
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        logger.error(f"Failed to read local transcript for {video_id}: {e}")
        return None

def save_local_transcript(video_id: str, text: str) -> Path:
    path = TRANSCRIPTS_DIR / f"{video_id}.txt"
    try:
        path.write_text(text, encoding="utf-8")
        return path
    except Exception as e:
        logger.error(f"Failed to save transcript for {video_id}: {e}")
        return path

# -----------------------------------------------------------------------------
# YouTubeTranscriptApi wrapper
# -----------------------------------------------------------------------------

def fetch_youtube_transcript(video_id: str, languages: Optional[List[str]] = None) -> Optional[str]:
    """Fetch transcript using YouTubeTranscriptApi (captions only)."""

    if not YT_AVAILABLE:
        return None

    if languages is None:
        languages = ["en", "en-US"]

    try:
        segments = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)

        text = "\n".join(
            s.get("text", "").strip()
            for s in segments
            if s.get("text", "").strip()
        )

        return text if text else None

    except (TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript):
        return None
    except Exception:
        return None

# -----------------------------------------------------------------------------
# Unified transcript loader
# -----------------------------------------------------------------------------

def get_or_create_transcript(
    video_url_or_id: str,
    *,
    use_youtube_fallback: bool = True,
    save_downloaded: bool = True,
    languages: Optional[List[str]] = None
) -> Tuple[Optional[str], Dict[str, Any]]:
    """
    Strategy:
    1. Local transcript
    2. YouTubeTranscriptApi (optional)
    """

    video_id = extract_video_id(video_url_or_id)
    meta = {
        "video_id": video_id,
        "source": "none",
        "saved_locally": False,
    }

    # 1 — local
    local = load_local_transcript(video_id)
    if local:
        meta["source"] = "local"
        return local, meta

    # 2 — YouTube
    if use_youtube_fallback:
        yt = fetch_youtube_transcript(video_id, languages=languages)
        if yt:
            meta["source"] = "youtube"
            if save_downloaded:
                save_local_transcript(video_id, yt)
                meta["saved_locally"] = True
            return yt, meta

    return None, meta

# -----------------------------------------------------------------------------
# Curated collections
# -----------------------------------------------------------------------------

curated_videos: Dict[str, List[Dict[str, str]]] = {
    "african_cuisine": [
        {"title": "Nigerian Efo Riro", "url": "https://youtu.be/vIIyn8LH1_E"},
        {"title": "Nigerian Moi-Moi", "url": "https://youtu.be/8ACC_oqhQRQ"},
        {"title": "Ghanaian Kontomire Stew", "url": "https://youtu.be/6VXYzN_gDNs"},
        {"title": "South African Chakalaka", "url": "https://youtu.be/FiiTy8FpxqY"},
    ],
    "french_cuisine": [
        {"title": "Flognarde Dessert", "url": "https://youtu.be/Q5uBEWjNeTw"},
        {"title": "Coq au Vin", "url": "https://youtu.be/GFuBsSrIVaE"},
        {"title": "Poulet au Vinaigre", "url": "https://youtu.be/tOgH_ElyGQg"},
        {"title": "Ratatouille", "url": "https://youtu.be/9qCO2qKrfr4"},
    ],
    "portuguese_cuisine": [
        {"title": "Bacalhau", "url": "https://youtu.be/xuUelAOuH3o"},
        {"title": "Carne Estufada", "url": "https://youtu.be/4sRwu9BnLAU"},
        {"title": "Pastel de Nata", "url": "https://youtu.be/MA4LEjxZ7io"},
        {"title": "Bifanas", "url": "https://youtu.be/2PoVTipLxoI"},
    ],
    "jamaican_cuisine": [
        {"title": "Pork Shoulder", "url": "https://youtu.be/d6IKVNRDjUk"},
        {"title": "Jamaican Curry Chicken", "url": "https://youtu.be/QIG6weWWB4Q"},
        {"title": "Sweet and Sour Fish", "url": "https://youtu.be/RlZx52eyW4M"},
        {"title": "Rice and Peas", "url": "https://youtu.be/qHC2WBx8Cvg"},
    ],
    "syrian_cuisine": [
        {"title": "Shrakiye", "url": "https://youtu.be/tB5XsB91-fQ"},
        {"title": "Tabouleh", "url": "https://youtu.be/HMXByWj_TAY"},
        {"title": "Knafe Nabulsieh", "url": "https://youtu.be/DJD4QQkItT4"},
        {"title": "Fatteh", "url": "https://youtu.be/xF4XRASGaC0"},
    ],
    "italian_cuisine": [
        {"title": "Chicken Cacciatore", "url": "https://youtu.be/bGJMHjG85BM"},
        {"title": "Cannelloni", "url": "https://youtu.be/E--DfY3w15k"},
        {"title": "Zozzona", "url": "https://youtu.be/WttUeyXPCbU"},
        {"title": "Gnocchi alla Sorrentina", "url": "https://youtu.be/llV1kYg5zNo"},
    ],
    "indian_cuisine": [
        {"title": "Chana Masala", "url": "https://youtu.be/PRw88q0NkiY"},
        {"title": "Chilli Garlic Tawa Chicken", "url": "https://youtu.be/nilVmkdmabs"},
        {"title": "Coconut Dosa", "url": "https://youtu.be/s6h3b4tuhCE"},
        {"title": "Garlic Naan Bread", "url": "https://youtu.be/wmbpOb9neLY"},
    ],
}

# -----------------------------------------------------------------------------
# Bulk preload
# -----------------------------------------------------------------------------

def preload_curated_transcripts(
    curated_map: Dict[str, List[Dict[str, str]]],
    *,
    use_youtube_fallback: bool = True,
    delay_seconds: float = 1.5
) -> List[Dict[str, Any]]:

    index: List[Dict[str, Any]] = []

    for collection, videos in curated_map.items():
        logger.info(f"Processing: {collection} ({len(videos)} videos)")

        for v in videos:
            url = v["url"]
            title = v.get("title", "")

            transcript, meta = get_or_create_transcript(
                url,
                use_youtube_fallback=use_youtube_fallback,
                save_downloaded=True,
            )

            video_id = meta["video_id"]

            path = TRANSCRIPTS_DIR / f"{video_id}.txt"
            if not path.exists():
                path = None

            entry = {
                "collection": collection,
                "title": title,
                "url": url,
                "video_id": video_id,
                "transcript_source": meta["source"],
                "transcript_path": str(path) if path else None,
            }

            index.append(entry)

            sleep(delay_seconds)

    index_path = DATA_DIR / "curated_index.json"
    index_path.write_text(json.dumps(index, indent=2), encoding="utf-8")

    logger.info(f"Saved curated index ({len(index)} entries) → {index_path}")

    return index

# -----------------------------------------------------------------------------
# Index loader
# -----------------------------------------------------------------------------

def load_curated_index() -> List[Dict[str, Any]]:
    path = DATA_DIR / "curated_index.json"
    if not path.exists():
        logger.error("curated_index.json not found — run preload_curated_transcripts() first.")
        return []
    return json.loads(path.read_text(encoding="utf-8")) 