#!/usr/bin/env bash
# git init 후 한 번 실행. .git/hooks/pre-commit 을 설치한다.
set -e
cd "$(dirname "$0")/.."
[ -d .git ] || { echo "먼저 git init 을 실행하라."; exit 1; }
cp scripts/hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit scripts/*.py scripts/hooks/pre-commit
echo "pre-commit 훅 설치 완료."
