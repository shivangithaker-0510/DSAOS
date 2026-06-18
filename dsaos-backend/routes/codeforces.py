from typing import Any, Dict, List

import httpx
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/codeforces", tags=["codeforces"])

CODEFORCES_API_BASE = "https://codeforces.com/api"


async def fetch_codeforces_json(endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(f"{CODEFORCES_API_BASE}/{endpoint}", params=params)
        response.raise_for_status()
        payload = response.json()
        if payload.get("status") != "OK":
            raise HTTPException(status_code=404, detail="Codeforces user not found")
        return payload["result"]


@router.get("/user/{handle}")
async def get_user_info(handle: str) -> Any:
    user_info = await fetch_codeforces_json("user.info", {"handles": handle})
    if not user_info:
        raise HTTPException(status_code=404, detail="Codeforces user not found")

    user = user_info[0]
    rating_history = await fetch_codeforces_json("user.rating", {"handle": handle})

    return {
        "handle": user.get("handle"),
        "rating": user.get("rating"),
        "max_rating": user.get("maxRating"),
        "rank": user.get("rank"),
        "rating_history": rating_history,
    }


@router.get("/user/{handle}/solved")
async def get_user_solved(handle: str) -> Any:
    submissions = await fetch_codeforces_json("user.status", {"handle": handle})
    solved: List[Dict[str, Any]] = []
    seen = set()

    for submission in submissions:
        if submission.get("verdict") != "OK":
            continue
        problem = submission.get("problem") or {}
        problem_key = (problem.get("contestId"), problem.get("index"))
        if problem_key in seen:
            continue
        seen.add(problem_key)
        solved.append(
            {
                "problem_id": f"{problem.get('contestId')}-{problem.get('index')}",
                "title": problem.get("name"),
                "rating": problem.get("rating"),
                "tags": problem.get("tags", []),
            }
        )

    return solved
