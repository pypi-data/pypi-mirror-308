import subprocess
import sys
from typing import Optional


def get_git_info(no_verify: Optional[bool] = False):
    print("🔍 Git 정보를 확인하는 중...")
    try:
        # Get default branch
        try:
            default_branch = (
                subprocess.check_output(
                    ["git", "symbolic-ref", "refs/remotes/origin/HEAD"], text=True
                )
                .strip()
                .split("/")[-1]
            )
        except subprocess.CalledProcessError:
            # Fallback method
            remote_info = subprocess.check_output(
                ["git", "remote", "show", "origin"], text=True
            )
            default_branch = next(
                line.split()[-1]
                for line in remote_info.splitlines()
                if "HEAD branch" in line
            )

        # Rest of your existing code...
        if not no_verify:
            status = subprocess.check_output(
                ["git", "status", "--porcelain"], text=True
            ).strip()
            if status:
                print(
                    "❌ Error: 커밋되지 않은 변경사항이 있습니다. 먼저 커밋하거나 스태시해주세요."
                )
                sys.exit(1)

        print("📝 커밋 메시지를 가져오는 중...")
        commits = subprocess.check_output(
            ["git", "log", f"{default_branch}..HEAD", "--oneline"], text=True
        ).strip()
        if not commits:
            print("❌ 커밋 메시지를 찾을 수 없습니다.")
            sys.exit(1)

        print("🌿 브랜치 정보를 가져오는 중...")
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True
        ).strip()
        remote = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"], text=True
        ).strip()
        # owner, repo = remote.replace('.git', '').split('github.com/')[-1].split('/')
        # URL 형식에 따라 파싱하는 로직
        if "git@github.com:" in remote:
            # SSH 형식: git@github.com:owner/repo.git
            owner, repo = (
                remote.split("git@github.com:")[-1].replace(".git", "").split("/")
            )
        else:
            # HTTPS 형식: https://github.com/owner/repo.git
            owner, repo = remote.replace(".git", "").split("github.com/")[-1].split("/")

        print(
            f"✅ Git 정보 확인 완료 (브랜치: {branch}, 기본 브랜치: {default_branch}, 저장소: {owner}/{repo})"
        )
        return commits.split("\n"), branch, owner, repo, default_branch
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 에러: {e}")
        sys.exit(1)
