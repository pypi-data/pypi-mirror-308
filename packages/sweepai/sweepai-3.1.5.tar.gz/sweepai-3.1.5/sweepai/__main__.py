from datetime import datetime
import os
import subprocess
import time
from urllib.parse import urlparse

from loguru import logger
import typer
os.environ["CLI"] = "true"

from typing import Literal
from pydantic import BaseModel
import requests
from rich import print as rprint

from sweepai.config.server import DEV
from sweepai.dataclasses.code_suggestions import CodeSuggestion
from sweepai import __version__

app = typer.Typer()

subprocess_args: dict = {"capture_output": True, "text": True, "check": True}

rprint(f"[cyan]Sweep CLI v{__version__}[/cyan]")

def changes_equal(changes1: list[CodeSuggestion], changes2: list[CodeSuggestion]):
    return len(changes1) == len(changes2) and all(change1.file_path == change2.file_path and change1.original_code == change2.original_code and change1.new_code == change2.new_code for change1, change2 in zip(changes1, changes2))

class RemoteChanges(BaseModel):
    applied_changes: list[CodeSuggestion]
    branch: str
    updated_at: datetime

    @classmethod
    def from_raw_data(cls, data: dict):
        return cls(applied_changes=[CodeSuggestion.from_camel_case(change) for change in data["applied_changes"]], branch=data["branch"], updated_at=datetime.fromisoformat(data["updated_at"]))

def get_backend_url(url: str):
    if "http://localhost" in url:
        return "http://localhost:8080"
    if url.endswith("sweep.dev"):
        return url.replace("https://", "https://backend.")
    return url + ":8443"

class SyncManager(BaseModel):
    message_id: str
    github_token: str
    latest_changes: list[CodeSuggestion] | None = None
    branch: str = ""
    updated_at: datetime | None = None
    base_url: str = "http://localhost:8080" if DEV else "https://backend.app.sweep.dev"

    @classmethod
    def from_url(cls, url: str):
        parsed_url = urlparse(url)
        _c, message_id = parsed_url.path.strip('/').split('/')
        instance = cls(message_id=message_id, github_token=os.environ["GITHUB_PAT"], base_url=get_backend_url(f"{parsed_url.scheme}://{parsed_url.netloc}"))
        instance.branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], **subprocess_args).stdout.strip("\n")
        return instance

    def _request(self, method: Literal["GET", "POST"], path: str, **kwargs):
        parsed_url = urlparse(self.base_url)
        response = requests.request(method, f"{self.base_url}/backend/{path}", headers={"Authorization": f"Bearer {self.github_token}"}, proxies={"no": parsed_url.hostname or ""}, **kwargs)
        response.raise_for_status()
        return response.json()

    def _fetch_remote_changes(self):
        raw_data = self._request("GET", f"messages/{self.message_id}/changes")
        return RemoteChanges.from_raw_data(raw_data)

    def _apply_changes(self, changes: list[CodeSuggestion]):
        num_changes = 0
        for change in changes:
            if change.original_code:
                with open(change.file_path, "r") as f:
                    original_code = f.read()
                    # if it's original code, apply the change
                    # if it's already the new code, do nothing
                    if original_code not in (change.original_code, change.new_code):
                        # otherwise, ask the user
                        if not typer.confirm(f"File {change.file_path} has changed since last sync. Applying the change will overwrite it. Continue?"):
                            continue
            elif os.path.exists(change.file_path):
                typer.confirm(f"File {change.file_path} has changed since last sync. Applying the change will overwrite it. Continue?")
            with open(change.file_path, "w") as f:
                f.write(change.new_code)
            num_changes += 1
        return num_changes

    def pull_changes(self):
        remote_changes = self._fetch_remote_changes()
        if self.branch != remote_changes.branch:
            raise Exception(f"Branch mismatch, skipping sync. Expected {self.branch}, got {remote_changes.branch}")
        if self.updated_at is None or remote_changes.updated_at > self.updated_at:
            logger.info(f"Pulling changes from server, {len(remote_changes.applied_changes)} changes applied (time: {remote_changes.updated_at}).")
            n = self._apply_changes(remote_changes.applied_changes)
            self.updated_at = remote_changes.updated_at
            return n
        else:
            return 0
    
    def get_local_changes(self):
        # get list of changed files before and after the commit
        files_changed = subprocess.run(["git", "diff", "--name-only", "HEAD"], **subprocess_args).stdout.strip("\n").splitlines()
        changes: list[CodeSuggestion] = []
        for file_changed in files_changed:
            # get original code before uncommitted changes
            original_code = subprocess.run(["git", "show", f"HEAD:{file_changed}"], **subprocess_args).stdout or ""
            if not os.path.exists(file_changed):
                logger.error(f"File does not exist: {file_changed}")
                continue
            with open(file_changed, "r") as f:
                new_code = f.read()
            changes.append(CodeSuggestion(file_path=file_changed, original_code=original_code, new_code=new_code))
        return changes
    
    def write_changes(self):
        changes = self.get_local_changes()
        if self.latest_changes is not None and changes_equal(self.latest_changes, changes):
            # Don't update if no changes
            return
        logger.info(f"Writing {len(changes)} changes to server.")
        self._request("POST", f"messages/{self.message_id}/changes", json=[change.to_camel_case() for change in changes])
        self.latest_changes = changes

    def disconnect(self):
        self._request("GET", f"messages/{self.message_id}/changes?disconnected=true")

    def sync_loop(self):
        # check that local branch is clean
        logger.info("Polling for changes, press Ctrl+C to stop.")
        self.pull_changes()
        self.latest_changes = self.get_local_changes()
        try:
            while True:
                self.pull_changes()
                self.write_changes()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Stopping sync loop.")
            self.disconnect()
            raise

@app.command()
def sync(url: str):
    sync_manager = SyncManager.from_url(url)
    sync_manager.sync_loop()

def main():
    app()

if __name__ == "__main__":
    main()
