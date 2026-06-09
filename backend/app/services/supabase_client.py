from __future__ import annotations

from typing import Any
from urllib.parse import quote

import httpx
from fastapi import HTTPException, status

from app.core.config import Settings


class SupabaseService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.rest_url = f"{settings.supabase_url}/rest/v1"
        self.storage_url = f"{settings.supabase_url}/storage/v1"
        self.auth_url = f"{settings.supabase_url}/auth/v1"
        self.service_headers = {
            "apikey": settings.supabase_service_role_key,
            "Authorization": f"Bearer {settings.supabase_service_role_key}",
        }

    async def signup(self, email: str, password: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{self.auth_url}/signup",
                headers={"apikey": self.settings.supabase_anon_key},
                json={"email": email, "password": password},
            )
        self._raise_for_supabase(response)
        return response.json()

    async def login(self, email: str, password: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{self.auth_url}/token?grant_type=password",
                headers={"apikey": self.settings.supabase_anon_key},
                json={"email": email, "password": password},
            )
        self._raise_for_supabase(response)
        return response.json()

    async def insert_row(self, table: str, payload: dict[str, Any]) -> dict[str, Any]:
        headers = {**self.service_headers, "Prefer": "return=representation"}
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(f"{self.rest_url}/{table}", headers=headers, json=payload)
        self._raise_for_supabase(response)
        rows = response.json()
        return rows[0] if rows else {}

    async def upsert_user(self, user_id: str, email: str | None) -> None:
        headers = {
            **self.service_headers,
            "Prefer": "resolution=merge-duplicates,return=minimal",
        }
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{self.rest_url}/users",
                headers=headers,
                params={"on_conflict": "id"},
                json={"id": user_id, "email": email},
            )
        self._raise_for_supabase(response)

    async def update_policy_type(self, policy_id: str, insurance_type: str | None) -> None:
        if not insurance_type:
            return
        headers = {**self.service_headers, "Prefer": "return=minimal"}
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.patch(
                f"{self.rest_url}/policies",
                headers=headers,
                params={"id": f"eq.{policy_id}"},
                json={"insurance_type": insurance_type},
            )
        self._raise_for_supabase(response)

    async def select_rows(
        self,
        table: str,
        filters: dict[str, str] | None = None,
        order: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        params: dict[str, str | int] = filters.copy() if filters else {}
        if order:
            params["order"] = order
        if limit:
            params["limit"] = limit
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(f"{self.rest_url}/{table}", headers=self.service_headers, params=params)
        self._raise_for_supabase(response)
        return response.json()

    async def get_policy_for_user(self, policy_id: str, user_id: str) -> dict[str, Any]:
        rows = await self.select_rows("policies", {"id": f"eq.{policy_id}", "user_id": f"eq.{user_id}"}, limit=1)
        if not rows:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
        return rows[0]

    async def upload_policy_pdf(self, path: str, content: bytes, content_type: str) -> None:
        headers = {
            **self.service_headers,
            "Content-Type": content_type or "application/pdf",
            "x-upsert": "false",
        }
        url = f"{self.storage_url}/object/{self.settings.supabase_storage_bucket}/{quote(path)}"
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(url, headers=headers, content=content)
        self._raise_for_supabase(response)

    async def download_policy_pdf(self, path: str) -> bytes:
        url = f"{self.storage_url}/object/{self.settings.supabase_storage_bucket}/{quote(path)}"
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.get(url, headers=self.service_headers)
        self._raise_for_supabase(response)
        return response.content

    async def create_signed_url(self, path: str, expires_in: int = 3600) -> str:
        url = f"{self.storage_url}/object/sign/{self.settings.supabase_storage_bucket}/{quote(path)}"
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, headers=self.service_headers, json={"expiresIn": expires_in})
        self._raise_for_supabase(response)
        signed = response.json().get("signedURL") or response.json().get("signedUrl")
        if not signed:
            return ""
        return f"{self.settings.supabase_url}/storage/v1{signed}" if signed.startswith("/") else signed

    @staticmethod
    def _raise_for_supabase(response: httpx.Response) -> None:
        if response.status_code < 400:
            return
        try:
            detail: Any = response.json()
        except ValueError:
            detail = response.text
        raise HTTPException(status_code=response.status_code, detail=detail)
