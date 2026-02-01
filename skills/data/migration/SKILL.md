---
name: migration
description: Create a new database migration following this project's patterns. Use when adding tables, columns, or modifying schema.
argument-hint: [description]
disable-model-invocation: true
---

# Create Database Migration

Create a new database migration for `$ARGUMENTS` following Laravel conventions.

## Migration Location
`database/migrations/`

## Naming Convention
`YYYY_MM_DD_HHMMSS_description.php`

Example: `2024_01_15_143022_create_products_table.php`

## Create Table Migration

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::create('table_name', function (Blueprint $table) {
            $table->id();

            // Common field patterns from this project:
            $table->string('name');
            $table->text('description')->nullable();
            $table->integer('status')->default(1);
            $table->integer('type')->default(0);
            $table->decimal('price', 10, 2)->default(0);
            $table->integer('qty')->default(0);
            $table->integer('order')->default(0);  // For sorting
            $table->boolean('active')->default(true);
            $table->json('data')->nullable();  // For flexible data

            // Foreign keys
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->foreignId('category_id')->nullable()->constrained();

            // Position fields (from tables)
            $table->integer('position_x')->default(0);
            $table->integer('position_y')->default(0);

            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('table_name');
    }
};
```

## Add Column Migration

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::table('existing_table', function (Blueprint $table) {
            $table->string('new_column')->nullable()->after('existing_column');
        });
    }

    public function down()
    {
        Schema::table('existing_table', function (Blueprint $table) {
            $table->dropColumn('new_column');
        });
    }
};
```

## Common Field Patterns From This Project

### Invoice Table Pattern
```php
$table->foreignId('user_id')->constrained();
$table->foreignId('table_id')->constrained();
$table->integer('status')->default(1);  // 0=refunded, 1=paid, 2=on-house
$table->json('order');  // Array of order items
$table->decimal('total', 10, 2);
$table->string('payment_type')->nullable();
$table->text('note')->nullable();
$table->foreignId('refund_reason_id')->nullable()->constrained();
$table->decimal('discount', 5, 2)->default(0);
```

### Inventory Table Pattern
```php
$table->foreignId('category_id')->constrained();
$table->string('name');
$table->text('description')->nullable();
$table->boolean('active')->default(true);
$table->integer('sold_by')->default(0);  // 0=piece, 1=half, 2=grams
$table->decimal('price', 10, 2);
$table->string('sku')->nullable();
$table->integer('qty')->default(0);
$table->string('color')->nullable();
$table->integer('order')->default(0);
$table->string('unit')->nullable();
```

### Warehouse Status Pattern
```php
$table->foreignId('warehouse_id')->constrained();
$table->foreignId('inventory_id')->nullable()->constrained();
$table->decimal('quantity', 10, 2)->default(0);
$table->integer('type')->default(0);  // 0=IN, 1=OUT, 2=RESET
$table->date('date');
$table->string('batch_id')->nullable();  // Links to invoice
$table->text('comment')->nullable();
```

### Table (dining) Pattern
```php
$table->string('name');
$table->integer('table_number');
$table->integer('area')->default(0);  // 0=Sala, 1=Basta
$table->integer('size')->default(1);
$table->integer('rotate')->default(0);
$table->integer('position_x')->default(0);
$table->integer('position_y')->default(0);
$table->integer('position_x_middle')->default(0);
$table->integer('position_y_middle')->default(0);
```

## Artisan Command

```bash
# Create migration
php artisan make:migration create_products_table

# Create migration for adding column
php artisan make:migration add_column_to_table

# Run migrations
php artisan migrate

# Rollback last batch
php artisan migrate:rollback

# Fresh migration (drops all tables)
php artisan migrate:fresh
```

## Steps

1. Generate migration with `php artisan make:migration`
2. Define schema in `up()` method
3. Define rollback in `down()` method
4. Run `php artisan migrate`
5. Create or update corresponding Model
