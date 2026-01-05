---
name: avalonia-collectionview
description: "AvaloniaUI에서 CollectionView 대안 (DataGridCollectionView, ReactiveUI)"
---

# 6.7 CollectionView를 사용한 MVVM 패턴

**⚠️ 중요: AvaloniaUI는 WPF의 CollectionViewSource를 지원하지 않습니다.**

AvaloniaUI에서는 다음 방법들을 사용:

#### 6.7.1 DataGridCollectionView 사용 (권장)

```csharp
// NuGet: Avalonia.Controls.DataGrid
// Service Layer
namespace MyApp.Services;

using Avalonia.Controls;

public sealed class MemberCollectionService
{
    private ObservableCollection<Member> Source { get; } = [];

    // DataGridCollectionView 반환
    // Returns DataGridCollectionView
    public IEnumerable CreateView(Predicate<Member>? filter = null)
    {
        var view = new DataGridCollectionView(Source);

        if (filter is not null)
        {
            view.Filter = item => filter((Member)item);
        }

        return view;
    }

    public void Add(Member item) => Source.Add(item);
    public void Remove(Member? item) { if (item is not null) Source.Remove(item); }
    public void Clear() => Source.Clear();
}
```

#### 6.7.2 ReactiveUI 사용 (대안)

```csharp
// NuGet: ReactiveUI.Avalonia
namespace MyApp.ViewModels;

using ReactiveUI;
using DynamicData;

public sealed class MainViewModel : ReactiveObject
{
    private readonly SourceList<Member> _sourceList = new();
    private readonly ReadOnlyObservableCollection<Member> _members;

    public ReadOnlyObservableCollection<Member> Members => _members;

    public MainViewModel()
    {
        _sourceList
            .Connect()
            .Filter(m => m.IsActive) // 필터링
                                     // Filtering
            .Sort(SortExpressionComparer<Member>.Ascending(m => m.Name)) // 정렬
                                                                          // Sorting
            .Bind(out _members)
            .Subscribe();
    }

    public void AddMember(Member member) => _sourceList.Add(member);
    public void RemoveMember(Member member) => _sourceList.Remove(member);
}
```

