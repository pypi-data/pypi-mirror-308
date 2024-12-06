import argparse
import logging
import os

import requests
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from packaging import version

from smart_pr_generator.config import Config
from smart_pr_generator.helpers import get_git_info
from smart_pr_generator.helpers.github_client import GitHubClient
from smart_pr_generator.tools import fetch_jira_issue

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

VERSION = "0.1.2"


def check_package_updates():
    """현재 설치된 패키지와 PyPI의 최신 버전을 비교"""
    try:
        # PyPI API 호출
        response = requests.get("https://pypi.org/pypi/smart-pr-generator/json")
        if response.status_code == 200:
            latest_version = response.json()["info"]["version"]

            # 버전 비교
            update_available = version.parse(latest_version) > version.parse(VERSION)

        # 업데이트 메시지 출력
        if update_available:
            print("-" * 60)
            print("📦 패키지 업데이트가 필요합니다:")
            print(f"현재 버전: {VERSION}")
            print(f"최신 버전: {latest_version}")
            print("\n업데이트 명령어: pip install --upgrade smart-pr-generator")
            print("-" * 60)
            print("")
    except Exception:
        pass


# main() 함수 시작 부분에 추가
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        action="version",
        version=f"v{VERSION}",
        help="현재 버전을 출력합니다",
    )
    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="커밋되지 않은 변경사항 체크를 스킵합니다",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="GitHub PR 생성 단계를 스킵합니다",
    )
    args = parser.parse_args()

    check_package_updates()

    Config().load_env_files()

    print("🚀 PR 생성 프로세스를 시작합니다...")

    commits, branch, owner, repo, default_branch = get_git_info(
        no_verify=args.no_verify
    )
    print(f"commits: {len(commits)}, branch: {branch}, owner: {owner}, repo: {repo}")

    print("🤖 AI로 PR 내용을 생성하는 중...")
    try:
        llm = ChatOpenAI(
            model="gpt-4o",
            api_key=os.environ["LAAS_API_KEY"],
            base_url="https://api-laas.wanted.co.kr/api/preset/v2/",
            default_headers={
                "apiKey": os.environ["LAAS_API_KEY"],
                "Content-Type": "application/json",
                "project": "SMART_PR_GENERATOR",
            },
            extra_body={
                "hash": "e86358af60cf8366835060943349c2ab1954950253ab35d36abd2e7089d5f39a",
            },
        )

        messages = [
            ("user", f"# Branch:\n {branch}\n\n# Commits:\n" + "\n".join(commits))
        ]

        answer: AIMessage = llm.invoke(messages)

        if answer.response_metadata["finish_reason"] == "tool_calls":
            # print("도구 호출")
            for tool_call in answer.tool_calls:
                # tool 정보 추출
                # print("tool_call", tool_call)
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                # print("tool_args", tool_args)

                # tool 실행
                if tool_name == "fetch_jira_issue":
                    tool_result = fetch_jira_issue.invoke(tool_args)
                else:
                    raise ValueError(f"Unknown tool: {tool_name}")

                # tool 실행 결과를 OpenAI에 전달
                messages.extend(
                    [
                        answer,
                        {
                            "role": "tool",
                            "name": tool_name,
                            "content": str(tool_result),
                            "tool_call_id": tool_call["id"],
                        },
                    ]
                )

                answer: AIMessage = llm.invoke(messages)

        print("✅ AI 응답 생성 완료")
        pr_data = JsonOutputParser().invoke(answer)

        if args.test:
            print("🧪 테스트 모드: GitHub PR 생성을 스킵합니다")
            return

        print("📨 GitHub PR을 생성하는 중...")
        print(f"https://api.github.com/repos/{owner}/{repo}/pulls")
        github_client = GitHubClient(os.environ["GITHUB_TOKEN"])
        pr_response = github_client.create_pull_request(
            owner=owner,
            repo=repo,
            title=pr_data["title"],
            body=pr_data["description"],
            head=branch,
            base=default_branch,
        )
        pr_url = pr_response["html_url"]
        print("✨ PR이 성공적으로 생성되었습니다!")
        print(f"🔗 PR URL: {pr_url}")
    except Exception as e:
        print(f"❌ AI 응답 생성 실패 (에러: {e})")


if __name__ == "__main__":
    main()
