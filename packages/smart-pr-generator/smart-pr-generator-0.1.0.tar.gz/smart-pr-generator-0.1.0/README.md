# smart-pull-request

## 로컬에 CLI 설치하기

```sh
pip install .

# 개발 모드로 설치
pip install -e .
```
## GitHub에서 설치하기

```sh
pip install git+https://github.com/jeongsk/Smart-PR-Generator.git
```

## JIRA_API_TOKEN 발급 받기

https://id.atlassian.com/manage-profile/security/api-tokens

## 환경 변수 셋팅

```env
export SMART_PR_GENERATOR_API_KEY="LAAS API KEY"

export GITHUB_TOKEN="깃허브 토큰"

export JIRA_EMAIL="지라 이메일 주소"
export JIRA_API_TOKEN="지라 API 액세스 토큰"
```