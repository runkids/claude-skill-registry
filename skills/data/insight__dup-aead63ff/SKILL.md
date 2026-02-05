---
name: insight
description: This skill should be used after project is working to get AI suggestions for improvements, optimizations, and integrations. AI proactively suggests based on project understanding - things user may not have considered. Practical only, no theoretical fluff.
description_vi: Dung sau khi project da chay on de nhan suggestions tu AI ve cai tien, toi uu, tich hop. AI chu dong suggest dua tren hieu biet ve project - nhung thu user chua nghi toi. Chi thuc te, khong ve voi.
keywords: [insight, suggest, improve, optimize, enhance, integrate]
keywords_vi: [goc nhin, de xuat, cai tien, toi uu, nang cap]
---

# Insight

AI chu dong suggest cai tien dua tren hieu biet ve project. Goc nhin moi, thuc te, khong ve voi.

## When to Use

Goi `/insight` khi:
- Project da chay on dinh
- AI da hieu codebase (da load/doc project)
- Muon goc nhin ngoai su hieu biet cua minh
- Tim kiem cai tien thuc te

KHONG goi khi:
- Chua hieu project (goi /load truoc)
- Dang giua implement (tap trung xong da)

## Process

### Step 1: Xac nhan da hieu project

Neu chua doc project:
```
Tao chua hieu project. Cho tao /load truoc.
```

Neu da hieu:
```
Tao da hieu [ten project] - [mo ta ngan 1 dong].
Dang phan tich...
```

### Step 2: Phan tich va suggest

Xem xet cac goc do:

1. **Performance** - bottleneck, caching, lazy load
2. **UX** - friction points, missing features nguoi dung can
3. **DX** - code structure, maintainability
4. **Security** - lo hong, best practices thieu
5. **Integration** - API/service huu ich co the tich hop

### Step 3: Output

```
INSIGHTS: [ten project]

1. [PERFORMANCE/UX/DX/SECURITY/INTEGRATION]
   Van de: [mo ta ngan]
   Suggest: [giai phap cu the]
   Impact: [High/Medium/Low]

2. [Category]
   Van de: [mo ta ngan]
   Suggest: [giai phap cu the]
   Impact: [High/Medium/Low]

3. ...

---
Muon tao elaborate cai nao? (1/2/3/skip)
```

## Rules

- **Thuc te**: Chi suggest cai THUC SU co ich, khong ly thuyet
- **Cu the**: "Them Redis cache cho API /users" khong phai "Consider caching"
- **Co loi**: Giai thich impact ro rang
- **Khong ve voi**: Khong suggest tech moi chi vi no "cool"
- **Gioi han**: Toi da 5 insights, uu tien high impact

## Example

```
User: /insight

AI:
Tao da hieu blog-app - Next.js blog voi markdown posts.
Dang phan tich...

INSIGHTS: blog-app

1. [PERFORMANCE]
   Van de: Moi request doc lai tat ca markdown files
   Suggest: Cache parsed posts trong memory, invalidate khi file thay doi
   Impact: High - giam response time 80%

2. [UX]
   Van de: Khong co search, user phai scroll tim bai
   Suggest: Them full-text search voi Fuse.js (client-side, khong can backend)
   Impact: Medium - UX tot hon khi co nhieu posts

3. [DX]
   Van de: Khong co preview khi viet markdown
   Suggest: Them /admin route voi live preview editor
   Impact: Low - chi tac dong den author

---
Muon tao elaborate cai nao? (1/2/3/skip)
```

## After Selection

Khi user chon 1 insight:
- Giai thich chi tiet hon
- Dua ra implementation steps
- Hoi muon /workflow de plan khong
