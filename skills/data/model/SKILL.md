---
name: model
description: Create a new Eloquent model following this project's patterns. Use when adding new database entities with relationships, traits, and constants.
argument-hint: [ModelName]
disable-model-invocation: true
---

# Create Eloquent Model

Create a new Eloquent model for `$ARGUMENTS` following this project's established patterns.

## Model Location
All models are in `app/Models/`

## Standard Model Structure

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ModelName extends Model
{
    use HasFactory;

    // Status/Type Constants (common pattern in this project)
    const STATUS_INACTIVE = 0;
    const STATUS_ACTIVE = 1;

    const TYPE_DEFAULT = 0;
    const TYPE_SPECIAL = 1;

    protected $table = 'table_name';

    protected $fillable = [
        'name',
        'description',
        'status',
        'type',
        // ... other fields
    ];

    protected $casts = [
        'data' => 'array',        // For JSON columns
        'is_active' => 'boolean',
        'created_at' => 'datetime',
    ];

    // Relationships
    public function category()
    {
        return $this->belongsTo(Category::class);
    }

    public function items()
    {
        return $this->hasMany(Item::class);
    }

    // Scopes
    public function scopeActive($query)
    {
        return $query->where('status', self::STATUS_ACTIVE);
    }
}
```

## Project-Specific Patterns

### Constants Pattern (from Invoice model)
```php
const STATUS_REFUNDED = 0;
const STATUS_PAYED = 1;
const STATUS_ON_THE_HOUSE = 2;
```

### JSON Column Pattern (from Invoice, Order models)
```php
protected $casts = [
    'order' => 'array',  // Stores order items as JSON
];
```

### Filtering Trait Pattern (from Invoice, Sales, Inventory)
```php
use App\Models\Traits\Revenue;
// or
use App\Models\Traits\SalesRevenue;
// or
use App\Models\Traits\InventoryFilters;

class Invoice extends Model
{
    use Revenue;

    // The trait provides filter() scope
}
```

### UUID Trait (from SalesImportDetail)
```php
use App\Models\Traits\HasUuid;

class SalesImportDetail extends Model
{
    use HasUuid;

    public $incrementing = false;
    protected $keyType = 'string';
}
```

### Warehouse Status Pattern
```php
const TYPE_IN = 0;      // Stock received
const TYPE_OUT = 1;     // Stock consumed (sales)
const TYPE_RESET = 2;   // Inventory count reset
```

### Sold By Pattern (from Inventory)
```php
const SOLD_BY_PIECE = 0;
const SOLD_BY_HALF_PORTION = 1;
const SOLD_BY_GRAMS = 2;

public static function skuMask($sku)
{
    return str_pad($sku, 4, '0', STR_PAD_LEFT);
}
```

## Common Relationships in This Project

```php
// Table -> Orders -> Invoices flow
class Table extends Model {
    public function orders() { return $this->hasMany(Order::class); }
}

class Order extends Model {
    public function table() { return $this->belongsTo(Table::class); }
}

class Invoice extends Model {
    public function table() { return $this->belongsTo(Table::class); }
    public function user() { return $this->belongsTo(User::class); }
    public function refundReason() { return $this->belongsTo(RefundReason::class); }
}

// Inventory -> Category
class Inventory extends Model {
    public function category() { return $this->belongsTo(Category::class); }
    public function pricing() { return $this->hasMany(InventoryPricing::class); }
}

// Warehouse system
class WarehouseStatus extends Model {
    public function warehouse() { return $this->belongsTo(Warehouse::class); }
    public function inventory() { return $this->belongsTo(Inventory::class); }
}
```

## Steps

1. Create model in `app/Models/`
2. Define constants for status/type fields
3. Set `$fillable` array with all mass-assignable fields
4. Define `$casts` for JSON, boolean, and date fields
5. Add relationships (belongsTo, hasMany, etc.)
6. Add any filtering traits if needed
7. Create corresponding migration
8. Create factory in `database/factories/` if needed for testing
