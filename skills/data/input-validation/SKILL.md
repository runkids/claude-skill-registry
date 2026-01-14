---
name: input-validation
description: Input validation patterns for the .NET 8 WPF widget host app. Use when implementing form validation, data annotations, command can-execute logic, and error display in MVVM ViewModels.
---

# Input Validation

## Overview

Provide consistent, user-friendly validation across forms and data entry points using MVVM patterns.

## Validation Approaches

### 1. CommunityToolkit.Mvvm Validation

```csharp
public partial class SettingsViewModel : ObservableValidator
{
    [ObservableProperty]
    [NotifyDataErrorInfo]
    [Required(ErrorMessage = "Name is required")]
    [MinLength(3, ErrorMessage = "Name must be at least 3 characters")]
    private string _name = "";

    [RelayCommand(CanExecute = nameof(CanSave))]
    private void Save()
    {
        ValidateAllProperties();
        if (HasErrors) return;
        
        // Proceed with save
    }

    private bool CanSave() => !HasErrors && !string.IsNullOrEmpty(Name);
}
```

### 2. INotifyDataErrorInfo (Built-in)

```csharp
public partial class MyViewModel : ObservableValidator
{
    public MyViewModel()
    {
        // Validate on property change
        ErrorsChanged += (s, e) => OnPropertyChanged(nameof(CanSave));
    }

    [ObservableProperty]
    [NotifyDataErrorInfo]
    [Range(1, 100, ErrorMessage = "Value must be between 1 and 100")]
    private int _value;
}
```

### 3. Custom Validation Logic

```csharp
[CustomValidation(typeof(MyValidator), nameof(MyValidator.ValidateUrl))]
private string _url = "";

public static class MyValidator
{
    public static ValidationResult ValidateUrl(string url, ValidationContext context)
    {
        if (string.IsNullOrEmpty(url))
            return ValidationResult.Success!;
            
        if (!Uri.TryCreate(url, UriKind.Absolute, out _))
            return new ValidationResult("Invalid URL format");
            
        return ValidationResult.Success!;
    }
}
```

---

## XAML Error Display

### Validation Error Template

```xaml
<TextBox Text="{Binding Name, UpdateSourceTrigger=PropertyChanged, ValidatesOnDataErrors=True}">
    <Validation.ErrorTemplate>
        <ControlTemplate>
            <StackPanel>
                <AdornedElementPlaceholder/>
                <TextBlock Text="{Binding [0].ErrorContent}"
                           Foreground="{DynamicResource Brushes.Error}"
                           FontSize="11"
                           Margin="4,2,0,0"/>
            </StackPanel>
        </ControlTemplate>
    </Validation.ErrorTemplate>
</TextBox>
```

### Border Highlight on Error

```xaml
<Style TargetType="TextBox">
    <Style.Triggers>
        <Trigger Property="Validation.HasError" Value="True">
            <Setter Property="BorderBrush" Value="{DynamicResource Brushes.Error}"/>
            <Setter Property="ToolTip" 
                    Value="{Binding (Validation.Errors)[0].ErrorContent, RelativeSource={RelativeSource Self}}"/>
        </Trigger>
    </Style.Triggers>
</Style>
```

---

## Command Can-Execute

```csharp
[RelayCommand(CanExecute = nameof(CanSubmit))]
private async Task SubmitAsync()
{
    // ...
}

private bool CanSubmit()
{
    return !string.IsNullOrWhiteSpace(Name) 
        && Email.Contains("@") 
        && !HasErrors
        && !IsLoading;
}

// Notify when dependencies change
partial void OnNameChanged(string value) => SubmitCommand.NotifyCanExecuteChanged();
partial void OnEmailChanged(string value) => SubmitCommand.NotifyCanExecuteChanged();
```

---

## Definition of Done (DoD)

- [ ] All user inputs have appropriate validation
- [ ] Validation errors displayed inline near the control
- [ ] Commands disabled when validation fails (CanExecute)
- [ ] Error messages are user-friendly (not technical)
- [ ] Required fields clearly indicated
- [ ] Validation runs on property change or blur
- [ ] HasErrors property prevents form submission

---

## Common Validation Attributes

| Attribute | Purpose |
|-----------|---------|
| `[Required]` | Field cannot be empty |
| `[MinLength(n)]` | Minimum string length |
| `[MaxLength(n)]` | Maximum string length |
| `[Range(min, max)]` | Numeric range |
| `[EmailAddress]` | Valid email format |
| `[Url]` | Valid URL format |
| `[RegularExpression]` | Pattern matching |
| `[CustomValidation]` | Custom validation logic |

---

## Anti-Patterns

- ❌ Validation only on submit (validate on change)
- ❌ Technical error messages ("NullReferenceException")
- ❌ Allowing submit with errors
- ❌ Silent validation failures
- ❌ Validation in code-behind

---

## Integration with Forms

```csharp
// Full form validation before save
public bool ValidateForm()
{
    ValidateAllProperties();
    return !HasErrors;
}

// Clear validation state
public void ResetValidation()
{
    ClearErrors();
}
```

