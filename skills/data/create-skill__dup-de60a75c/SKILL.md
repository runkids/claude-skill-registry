---
name: create-skill
description: >
  Claude Code Skill을 생성합니다.
  스킬 생성, SKILL.md 작성, 새 스킬 만들기 요청 시 활성화.
---

# Skill 생성

Claude Code Skill을 생성하는 가이드입니다.

## 필수 요소

| 필드 | 설명 | 제약 |
|------|------|------|
| `name` | 스킬 식별자 | 1-64자, 소문자/숫자/하이픈만, 디렉토리명과 일치 |
| `description` | 무엇 + 언제 | 1-1024자, 트리거 키워드 포함 |

## description 작성 패턴

```yaml
description: >
  [무엇을 하는지 1-2문장]
  [언제/어떤 키워드에 사용하는지]
```

**예시:**
```yaml
description: >
  PDF 파일에서 텍스트와 테이블을 추출합니다.
  PDF 작업, 문서 추출, 폼 처리 요청 시 사용.
```

## 생성 단계

### 1단계: 디렉토리 생성

```bash
mkdir -p skills/{name}/references
```

### 2단계: SKILL.md 작성

```yaml
---
name: skill-name
description: >
  무엇을 하는지 설명.
  언제 사용하는지 트리거 키워드 포함.
---

# 스킬 제목

## 개요
핵심 기능 2-3문장

## 사용 방법
단계별 지침

## 상세 정보
- [참조 문서](references/detail.md)
```

### 3단계: 상세 내용 분리

500줄 초과 시 `references/`로 분리:

```
skill-name/
├── SKILL.md           # <500줄, 핵심만
└── references/
    ├── detail.md      # 상세 가이드
    └── examples.md    # 예제 모음
```

## 선택 필드

| 필드 | 용도 | 예시 |
|------|------|------|
| `argument-hint` | 인자 힌트 | `[파일경로]` |
| `disable-model-invocation` | 사용자만 호출 | `true` (부작용 있는 작업) |
| `user-invocable` | Claude만 호출 | `false` (내부 지식) |
| `context` | 서브에이전트 실행 | `fork` |
| `agent` | 서브에이전트 유형 | `Explore`, `Plan`, `general-purpose` |
| `allowed-tools` | 도구 제한 | `Read, Grep` |

## 사용 패턴

| 패턴 | 설정 | 용도 |
|------|------|------|
| 일반 스킬 | 기본값 | 사용자/Claude 모두 호출 |
| 사용자 전용 | `disable-model-invocation: true` | 배포, DB 작업 등 부작용 |
| Claude 전용 | `user-invocable: false` | 내부 컨벤션, 배경 지식 |
| 격리 실행 | `context: fork` | 무거운 분석 작업 |

## 체크리스트

```
□ name이 1-64자, 소문자/숫자/하이픈만 사용하는가?
□ name이 디렉토리명과 일치하는가?
□ description이 무엇+언제를 명확히 설명하는가?
□ SKILL.md가 500줄 이하인가?
□ 상세 내용이 references/로 분리되었는가?
```

## 상세 가이드

- [Frontmatter 스키마](references/schema.md)
- [템플릿 모음](references/templates.md)
