---
name: ui-components
description: QuickRail UI 컴포넌트 가이드. HTML/CSS UI 컴포넌트 작성 시 일관된 스타일 적용을 위한 참조 가이드. 버튼, 카드, 폼, 칩, 라벨 등의 스타일 패턴을 제공합니다.
allowed-tools: Read,Write,Edit,Glob,Grep
---

# QuickRail UI Components Guide

QuickRail 프로젝트의 UI 컴포넌트 스타일 가이드입니다.

## When to Use This Skill

- 새로운 페이지나 컴포넌트 UI를 작성할 때
- 기존 스타일과 일관성 있는 버튼, 카드, 폼 요소를 만들 때
- 다크/라이트 테마를 지원하는 UI를 구현할 때

---

## CSS Variables (테마 변수)

QuickRail은 CSS 변수 기반 테마 시스템을 사용합니다. 하드코딩된 색상 대신 항상 이 변수들을 사용하세요.

### Light Theme (기본)
```css
:root {
    --qr-bg: #f5f5f5;           /* 페이지 배경 */
    --qr-surface: #ffffff;       /* 카드, 컨테이너 배경 */
    --qr-surface-2: #f8f9fa;     /* 보조 surface (hover, nested) */
    --qr-text: #333333;          /* 기본 텍스트 */
    --qr-muted: #666666;         /* 보조 텍스트, 설명 */
    --qr-border: #e0e0e0;        /* 테두리 */
    --qr-shadow: rgba(0,0,0,0.1); /* 그림자 */
    --qr-menu-bg: #ffffff;       /* 메뉴 배경 */
    --qr-menu-text: #111111;     /* 메뉴 텍스트 */
}
```

### Dark Theme
```css
html[data-theme="dark"] {
    --qr-bg: #0f1115;
    --qr-surface: #171a21;
    --qr-surface-2: #11141b;
    --qr-text: #e6e8ee;
    --qr-muted: #a9b0c0;
    --qr-border: #2a2f3a;
    --qr-shadow: rgba(0,0,0,0.35);
    --qr-menu-bg: #171a21;
    --qr-menu-text: #e6e8ee;
}
```

---

## Buttons (버튼)

### Action Button 기본 스타일 (`qr-action-btn`)

모던하고 통일된 액션 버튼 스타일입니다. 카드 내 액션, 툴바 버튼 등에 사용합니다.

```css
.qr-action-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.45rem 0.7rem;
    border-radius: 10px;
    border: 1px solid var(--qr-border);
    background: var(--qr-surface);
    color: var(--qr-text);
    text-decoration: none;
    font-weight: 700;
    font-size: 0.9rem;
    line-height: 1;
    transition: transform 0.12s ease, background 0.12s ease, border-color 0.12s ease, color 0.12s ease;
    user-select: none;
    cursor: pointer;
}

.qr-action-btn:hover {
    transform: translateY(-1px);
    background: var(--qr-surface-2);
    border-color: rgba(52,152,219,0.45);
}

.qr-action-btn:active {
    transform: translateY(0);
}

.qr-action-btn svg {
    width: 16px;
    height: 16px;
    display: block;
    opacity: 0.9;
}
```

### Primary Button (주요 액션)

```css
.qr-action-btn.primary {
    background: rgba(52,152,219,0.12);
    border-color: rgba(52,152,219,0.35);
    color: #1f5f8b;
}

.qr-action-btn.primary:hover {
    background: rgba(52,152,219,0.18);
    border-color: rgba(52,152,219,0.55);
    color: #1b4f75;
}
```

### Danger Button (삭제, 위험 액션)

```css
.qr-action-btn.danger {
    background: rgba(231,76,60,0.10);
    border-color: rgba(231,76,60,0.35);
    color: #a93226;
}

.qr-action-btn.danger:hover {
    background: rgba(231,76,60,0.16);
    border-color: rgba(231,76,60,0.55);
    color: #922b21;
}
```

### Muted Button (보조 액션)

```css
.qr-action-btn.muted {
    background: transparent;
}
```

### 사용 예시

```html
<!-- 기본 버튼 -->
<button class="qr-action-btn" type="button">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M12 20h9"></path>
        <path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4 12.5-12.5z"></path>
    </svg>
    <span>수정</span>
</button>

<!-- Primary 버튼 (링크) -->
<a href="/cases" class="qr-action-btn primary">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M6 2h9l3 3v17a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z"></path>
    </svg>
    <span>케이스</span>
</a>

<!-- Danger 버튼 -->
<button class="qr-action-btn danger" type="button" onclick="deleteItem()">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M3 6h18"></path>
        <path d="M8 6V4h8v2"></path>
        <path d="M6 6l1 16h10l1-16"></path>
    </svg>
    <span>삭제</span>
</button>

<!-- Muted 버튼 -->
<button class="qr-action-btn muted" type="button">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M3 13h8V3H3v10z"></path>
    </svg>
    <span>대시보드</span>
</button>
```

---

## Cards (카드)

### 기본 카드

```css
.card {
    background: var(--qr-surface);
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px var(--qr-shadow);
}
```

### 클릭 가능한 카드

```css
.project-card {
    cursor: pointer;
    transition: transform 0.2s;
}

.project-card:hover {
    transform: translateY(-2px);
}
```

---

## Chips (칩/태그)

상태나 카운트를 표시하는 작은 인라인 요소입니다.

```css
.qr-chip-row {
    margin-top: 0.85rem;
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    align-items: center;
    color: var(--qr-muted);
    font-size: 0.85rem;
}

.qr-chip {
    border: 1px solid var(--qr-border);
    background: var(--qr-surface-2);
    padding: 0.2rem 0.5rem;
    border-radius: 999px;
    display: inline-flex;
    gap: 0.35rem;
    align-items: center;
    white-space: nowrap;
}

.qr-chip strong {
    color: var(--qr-text);
    font-weight: 700;
}
```

### 사용 예시

```html
<div class="qr-chip-row">
    <span class="qr-chip">TC <strong>42</strong></span>
    <span class="qr-chip">진행중 런 <strong>3</strong></span>
    <span class="qr-chip">완료 런 <strong>12</strong></span>
</div>
```

---

## Labels (라벨)

프로젝트나 항목에 붙이는 컬러 라벨입니다.

```css
.qr-label-row {
    margin-top: 0.65rem;
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
    align-items: center;
    min-height: 24px;
}

.qr-label {
    padding: 0.25rem 0.65rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
    color: white;
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    white-space: nowrap;
}

.qr-label-manage-btn {
    padding: 0.2rem 0.5rem;
    border: 1px dashed var(--qr-border);
    background: transparent;
    color: var(--qr-muted);
    border-radius: 999px;
    font-size: 0.75rem;
    cursor: pointer;
    transition: all 0.15s ease;
}

.qr-label-manage-btn:hover {
    border-color: rgba(52,152,219,0.5);
    color: #3498db;
}
```

### 사용 예시

```html
<div class="qr-label-row">
    <span class="qr-label" style="background: #e74c3c;">중요</span>
    <span class="qr-label" style="background: #3498db;">API</span>
    <span class="qr-label" style="background: #2ecc71;">완료</span>
    <button class="qr-label-manage-btn" type="button">+ 라벨 추가</button>
</div>
```

---

## Search & Filters (검색 및 필터)

### 검색 입력

```css
.qr-search-row {
    display: flex;
    gap: 0.75rem;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    margin: 0 0 1.25rem 0;
}

.qr-search {
    position: relative;
    flex: 1 1 360px;
    min-width: 260px;
}

.qr-search svg {
    position: absolute;
    left: 10px;
    top: 50%;
    transform: translateY(-50%);
    width: 18px;
    height: 18px;
    opacity: 0.65;
}

.qr-search input {
    padding-left: 36px;
}
```

### 필터 영역

```css
.qr-filters {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
    justify-content: flex-end;
}

.qr-filters .form-control {
    width: auto;
    min-width: 180px;
    padding: 0.45rem 0.6rem;
    font-size: 0.95rem;
}
```

### 사용 예시

```html
<div class="qr-search-row">
    <div class="qr-search">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="7"></circle>
            <path d="M20 20l-3.2-3.2"></path>
        </svg>
        <input class="form-control" type="text" placeholder="검색...">
    </div>
    <div class="qr-filters">
        <select class="form-control">
            <option>필터: 전체</option>
            <option>필터: 즐겨찾기</option>
        </select>
        <select class="form-control">
            <option>정렬: 최근 업데이트</option>
            <option>정렬: 이름</option>
        </select>
    </div>
</div>
```

---

## Favorite Button (즐겨찾기 버튼)

```css
.qr-fav-btn {
    border: none;
    background: transparent;
    cursor: pointer;
    padding: 0.25rem;
    border-radius: 6px;
    color: #7f8c8d;
}

.qr-fav-btn:hover {
    background: rgba(52,152,219,0.12);
    color: #2c3e50;
}

.qr-fav-btn.is-favorite {
    color: #f1c40f;
}

.qr-fav-btn svg {
    width: 18px;
    height: 18px;
}
```

### 사용 예시

```html
<button class="qr-fav-btn" type="button" aria-label="즐겨찾기">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M12 17.3l-6.2 3.7 1.7-7.1L2 9.2l7.2-.6L12 2l2.8 6.6 7.2.6-5.5 4.7 1.7 7.1z"></path>
    </svg>
</button>

<!-- 즐겨찾기 활성화 상태 -->
<button class="qr-fav-btn is-favorite" type="button" aria-label="즐겨찾기 해제">
    <svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2">
        <path d="M12 17.3l-6.2 3.7 1.7-7.1L2 9.2l7.2-.6L12 2l2.8 6.6 7.2.6-5.5 4.7 1.7 7.1z"></path>
    </svg>
</button>
```

---

## Meta Information (메타 정보)

날짜, 생성자 등의 부가 정보를 표시합니다.

```css
.qr-meta-row {
    margin-top: 0.45rem;
    color: var(--qr-muted);
    font-size: 0.85rem;
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
}
```

### 사용 예시

```html
<div class="qr-meta-row">
    <span>최근 업데이트: 2026-01-22</span>
    <span>생성: 2026-01-15</span>
    <span>작성자: admin</span>
</div>
```

---

## Icon Buttons (아이콘 버튼)

아이콘만 있는 버튼 또는 아이콘+텍스트 버튼 공통 스타일입니다.

```css
.qr-icon-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    line-height: 1;
}

.qr-icon-btn svg {
    width: 18px;
    height: 18px;
    display: block;
}
```

---

## View Toggle (그리드/리스트 토글)

```css
.qr-view-toggle {
    padding: 0.5rem 0.6rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.35rem;
    min-width: 44px;
}

.qr-view-toggle .qr-view-ico {
    display: none;
    align-items: center;
    justify-content: center;
}

/* 현재 grid 뷰일 때 list 아이콘 표시 (전환용) */
.qr-view-toggle[data-view="grid"] .qr-view-ico-list { display: inline-flex; }
/* 현재 list 뷰일 때 grid 아이콘 표시 (전환용) */
.qr-view-toggle[data-view="list"] .qr-view-ico-grid { display: inline-flex; }
```

---

## Common SVG Icons

자주 사용하는 SVG 아이콘 참조입니다.

### 수정 (Edit/Pencil)
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M12 20h9"></path>
    <path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4 12.5-12.5z"></path>
</svg>
```

### 삭제 (Delete/Trash)
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M3 6h18"></path>
    <path d="M8 6V4h8v2"></path>
    <path d="M6 6l1 16h10l1-16"></path>
    <path d="M10 11v6"></path>
    <path d="M14 11v6"></path>
</svg>
```

### 복제 (Copy/Duplicate)
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M8 8h13v13H8z"></path>
    <path d="M3 16V3h13"></path>
</svg>
```

### 대시보드 (Dashboard)
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M3 13h8V3H3v10z"></path>
    <path d="M13 21h8V11h-8v10z"></path>
    <path d="M13 3h8v6h-8V3z"></path>
    <path d="M3 21h8v-6H3v6z"></path>
</svg>
```

### 문서/케이스 (Document/Cases)
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M6 2h9l3 3v17a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z"></path>
    <path d="M15 2v4h4"></path>
    <path d="M8 9h8"></path>
    <path d="M8 13h8"></path>
    <path d="M8 17h6"></path>
</svg>
```

### 런 (Run/List)
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M3 7h18"></path>
    <path d="M7 7V3"></path>
    <path d="M17 7V3"></path>
    <path d="M5 11h14"></path>
    <path d="M5 15h10"></path>
    <path d="M5 19h8"></path>
</svg>
```

### 검색 (Search)
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <circle cx="11" cy="11" r="7"></circle>
    <path d="M20 20l-3.2-3.2"></path>
</svg>
```

### 별/즐겨찾기 (Star/Favorite)
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M12 17.3l-6.2 3.7 1.7-7.1L2 9.2l7.2-.6L12 2l2.8 6.6 7.2.6-5.5 4.7 1.7 7.1z"></path>
</svg>
```

### 라벨/태그 (Label/Tag)
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
    <line x1="7" y1="7" x2="7.01" y2="7"></line>
</svg>
```

### 그리드 뷰 (Grid View)
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <rect x="3" y="3" width="7" height="7" rx="1"></rect>
    <rect x="14" y="3" width="7" height="7" rx="1"></rect>
    <rect x="3" y="14" width="7" height="7" rx="1"></rect>
    <rect x="14" y="14" width="7" height="7" rx="1"></rect>
</svg>
```

### 리스트 뷰 (List View)
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M8 6h13"></path>
    <path d="M8 12h13"></path>
    <path d="M8 18h13"></path>
    <path d="M3 6h1"></path>
    <path d="M3 12h1"></path>
    <path d="M3 18h1"></path>
</svg>
```

### 눈 (보이기/숨기기)
```html
<!-- 보이기 -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
    <circle cx="12" cy="12" r="3"></circle>
</svg>

<!-- 숨기기 -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
    <line x1="1" y1="1" x2="23" y2="23"></line>
</svg>
```

---

## Best Practices

1. **항상 CSS 변수 사용**: 하드코딩된 색상 대신 `var(--qr-*)` 변수 사용
2. **다크 테마 지원**: 모든 컴포넌트가 다크/라이트 테마에서 올바르게 표시되는지 확인
3. **접근성**: `aria-label`, `title` 속성 추가
4. **일관된 간격**: `rem` 단위 사용, 0.25rem 배수로 설정
5. **부드러운 전환**: `transition` 속성으로 hover 효과 부드럽게
6. **SVG 아이콘**: 이미지 대신 인라인 SVG 사용 (크기/색상 제어 용이)

---

## Related Files

- `app/templates/base.html` - 전역 CSS 변수 및 기본 스타일
- `app/templates/main/projects.html` - 버튼, 카드, 필터 UI 참조
- `app/templates/main/cases.html` - 테이블, 체크박스 UI 참조
- `app/templates/main/runs.html` - 리스트, 상태 표시 UI 참조
