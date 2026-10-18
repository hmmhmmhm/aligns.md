<p align="center">
  <img src="../../assets/aligns-header.png" alt="노란색과 하늘색 배경에 연결된 점과 ALIGNS.md 제목" width="100%">
</p>

<h1 align="center">ALIGNS.md</h1>

<p align="center"><a href="https://aligns.md/ko/">aligns.md</a></p>

<p align="center">
  <a href="../../README.md" lang="en">English</a> · <strong lang="ko">한국어</strong> · <a href="ja.md" lang="ja">日本語</a>
</p>

<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="라이선스: MIT"></a>
  <a href="https://github.com/hmmhmmhm/aligns.md/stargazers"><img src="../../assets/badges/github-star.svg" alt="GitHub 스타"></a>
  <a href="#install-align"><img src="https://img.shields.io/badge/Format-Markdown-222222.svg?logo=markdown" alt="문서 형식: Markdown"></a>
  <a href="https://skills.sh/hmmhmmhm/aligns.md/align"><img src="../../assets/badges/skills-sh.svg" alt="skills.sh에서 설치"></a>
</p>

## 좋은 결과의 기준을 정하세요

ALIGNS.md에는 에이전트가 따라야 할 목표와, 선택이 필요할 때 무엇을 우선할지 적습니다. **align** 스킬로 이 기준을 함께 정하고, 작업이 달라지면 다시 살펴볼 수 있습니다.

<p align="center">
  <img src="../../assets/define-what-good-means.png" alt="여러 경로가 하나의 기준점으로 모이는 모습" width="100%">
</p>

## 기대하는 바를 따로 관리하세요

개인의 판단 기준은 ALIGNS.md에, 여러 프로젝트에서 쓸 정렬 방법은 스킬에 둡니다. AGENTS.md나 CLAUDE.md처럼 주로 쓰는 에이전트 지시 파일에서 ALIGNS.md를 참조하게 하세요. Git을 쓰는 프로젝트라면 변경 사항은 Git 이력으로 추적합니다. 스킬을 업데이트해도 합의한 기준은 바뀌지 않습니다.

전문 스킬도 이 기준에 맞춰 사용합니다. 스킬의 기본 스타일을 내 취향으로 저장하지 않으며, ALIGNS.md에서 이미 정한 사항은 다시 묻지 않습니다. 개발·디자인·검토·글쓰기에 함께 쓸 스킬은 [추천 스킬 문서](../recommended-skills.md)(영어)에 정리했습니다.

<p align="center">
  <img src="../../assets/keep-expectations-separate.png" alt="실행 환경, 지시, 기대 사항을 나타내는 세 패널이 따로 나뉘어 연결된 모습" width="100%">
</p>

## 내 취향을 설명하는 수고가 줄어듭니다

한 번 맞춰둔 기준은 다음 작업에도 이어집니다. 에이전트가 이미 아는 취향을 바탕으로 판단하니, 매번 원하는 방식을 설명하거나 선택해줄 일이 줄어듭니다.

생각과 다른 결과가 나오면 기준을 함께 고쳐, 다음 작업에 반영합니다.

[실험 결과와 방법](../../RETENTION_BENCHMARK.md)

<p align="center">
  <a href="../../RETENTION_BENCHMARK.md"><img src="../../assets/benchmarks/retention-comparison.svg" alt="가상실험: 일반 지시 조건은 과제 중 답변 9회, 저장된 선호와 align을 제공한 조건은 0회. 가정한 초기 설정 답변 4회는 별도 표시. 두 조건 모두 최종 결과 12개가 기준 충족" width="100%"></a>
</p>

## 필요할 때 다시 정렬하세요

자가정렬(self-alignment)은 에이전트와 자신의 선호와 판단 기준을 정리하고, 그 기준에 맞게 작업했는지 점검하는 과정입니다.

중요한 판단이 의도와 어긋났거나, 같은 수정을 반복하며 빠진 기준을 발견했거나, 다음에 무엇을 해야 할지 막막할 때 정렬을 다시 진행하세요. 선택한 PR 피드백과 접근 가능한 프로젝트 대화에서 반복해서 드러나는 판단 기준, 즉 취향 불변성을 찾아 적용 범위와 예외도 살펴볼 수 있습니다. 예상 시간을 확인한 뒤 최근 이력부터 볼지, 전체를 볼지 고르세요. 에이전트에게 긴 작업을 맡기기 전에는 가상의 선택 상황 몇 가지로 판단을 맞춰 봅니다. 명백한 오류는 바로 고치고, 이미 답한 질문은 되풀이하지 않습니다.

짧게 요청해도 됩니다. 에이전트는 기존 맥락을 먼저 확인하고, 결과를 크게 바꿀 정보가 빠졌을 때만 질문합니다. 언제 묻고 언제 판단해서 진행할지도 함께 정할 수 있습니다. ALIGNS.md에는 앞으로도 적용하기로 확인한 선호만 남깁니다.

<p align="center">
  <img src="../../assets/continuous-self-alignment.png" alt="기준선에서 벗어난 경로가 점차 방향을 바로잡는 모습" width="100%">
</p>

<a id="install-align"></a>

## align 설치하기

에이전트에게 다음 요청을 붙여 넣으세요.

```text
https://github.com/hmmhmmhm/aligns.md 의 최신 설치 가이드에 따라 align 스킬을 설정해 주세요. 기존 설정을 확인하고, 주로 쓰는 CLI에서 지원하는 방식으로 설치한 뒤 이 프로젝트에 ALIGNS.md를 연결하고 지원되는 방식으로 스킬을 업데이트하도록 설정해 주세요. 기존 지침과 확인된 제 기준은 보존하고, 아직 정해지지 않은 사항만 질문해 주세요.
```

직접 설치할 수도 있습니다.

```sh
npx skills add hmmhmmhm/aligns.md --skill align
```

설치 후 **“이 프로젝트 자가정렬 진행해봅시다”**라고 요청하세요. 명령어나 정확한 문구를 외울 필요는 없습니다.

[설치·업데이트 및 여덟 가지 시작점](../usage.md)(영어)

## 팀에서 활용하기

코드 리뷰와 에이전트 대화에서 검토한 판단 사례를 코딩 에이전트 학습용 데이터로 준비할 수 있습니다. 학습과 결과 검증은 팀이 진행합니다.

[MLOps·팀 도입 검토 문서](../translated-briefs/ko.md) · [수동 제출 가이드](../team-training-data.md)(영어)

## 프로젝트에 배지 붙이기

ALIGNS.md를 쓰는 프로젝트라면 README에 이 배지를 붙일 수 있습니다. 에이전트에게 추가해 달라고 요청하거나, 선택지에 나오는 7번을 고르세요. 배지가 없을 때만 제안합니다. 아래 Markdown을 직접 복사해도 됩니다.

[![Uses ALIGNS.md](../../assets/badges/uses-aligns.svg)](https://github.com/hmmhmmhm/aligns.md)

```markdown
[![Uses ALIGNS.md](https://raw.githubusercontent.com/hmmhmmhm/aligns.md/main/assets/badges/uses-aligns.svg)](https://github.com/hmmhmmhm/aligns.md)
```

## 라이선스

[MIT](../../LICENSE). Copyright (c) 2026 hmmhmmhm.

<p align="center">
  <img src="../../assets/aligns-footer.png" alt="초록색 배경에 겹쳐진 좌표 격자와 ALIGNS.md 제목" width="100%">
</p>
