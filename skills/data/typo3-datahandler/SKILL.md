---
name: typo3-datahandler
description: Agent Skill for TYPO3 DataHandler patterns. Use when working with TYPO3 database operations, record manipulation (create, update, copy, move, delete, localize), workspaces, versioning, staging, publishing, TCEmain hooks, cache clearing, or backend record processing. Essential for TYPO3 extension development.
---

# TYPO3 DataHandler Skill

Expert patterns for working with TYPO3's DataHandler (formerly TCEmain) - the central API for all database record operations in the TYPO3 backend.

## What is DataHandler?

The DataHandler (`\TYPO3\CMS\Core\DataHandling\DataHandler`) is TYPO3's core class for:
- **Creating** new records in any TCA-configured table
- **Updating** existing records
- **Copying** records (with optional child elements)
- **Moving** records between pages
- **Deleting/Undeleting** records (soft delete)
- **Localizing** records for multilingual sites
- **Versioning** and **Workspaces** (staging, publishing, approval workflows)
- **Cache clearing** operations

All operations respect TCA configuration, user permissions, and workspace states.

### Workspaces Overview

Workspaces allow staging changes before publishing:
- **Live workspace** (`id = 0`): Published content visible to visitors
- **Custom workspaces** (`id > 0`): Staging areas for draft changes
- DataHandler **automatically creates versions** when editing in a workspace
- Use `version` command for publish/swap/discard operations

## Quick Reference

### Basic Usage Pattern

```php
<?php
declare(strict_types=1);

use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Utility\GeneralUtility;

// NEVER inject DataHandler - always create new instance
$dataHandler = GeneralUtility::makeInstance(DataHandler::class);
$dataHandler->start($data, $cmd);
$dataHandler->process_datamap();  // For data operations
$dataHandler->process_cmdmap();   // For command operations

// Check for errors
if ($dataHandler->errorLog !== []) {
    foreach ($dataHandler->errorLog as $error) {
        // Handle error
    }
}
```

### Data Array Syntax (Create/Update)

```php
// Create new record (use NEW + unique ID)
$data['pages']['NEW123'] = [
    'pid' => 1,           // Parent page ID
    'title' => 'My Page',
    'hidden' => 0,
];

// Update existing record
$data['tt_content'][42] = [
    'header' => 'Updated Header',
    'bodytext' => 'New content',
];

// Reference NEW record in another NEW record
$data['sys_category']['NEW_cat'] = ['title' => 'New Category', 'pid' => 1];
$data['tt_content']['NEW_content'] = [
    'pid' => 1,
    'categories' => 'NEW_cat',  // References the category above
];
```

### Command Array Syntax (Copy/Move/Delete)

```php
// Delete record
$cmd['tt_content'][42]['delete'] = 1;

// Undelete record
$cmd['tt_content'][42]['undelete'] = 1;

// Copy to page (positive = first in page)
$cmd['tt_content'][42]['copy'] = 10;

// Copy after record (negative = after that UID)
$cmd['tt_content'][42]['copy'] = -55;

// Move to page
$cmd['tt_content'][42]['move'] = 10;

// Localize to language
$cmd['tt_content'][42]['localize'] = 2;  // Language UID

// Copy to language (free mode, no parent reference)
$cmd['tt_content'][42]['copyToLanguage'] = 2;
```

## Expertise Areas

### Data Operations (`process_datamap()`)
- Record creation with NEW placeholders
- Record updates with field values
- Inline (IRRE) record handling
- FlexForm data submission
- File references (FAL)
- MM relation handling

### Command Operations (`process_cmdmap()`)
- `copy` - Duplicate records with children
- `move` - Relocate records
- `delete` - Soft delete (respects TCA delete field)
- `undelete` - Restore deleted records
- `localize` - Create language overlays (connected mode)
- `copyToLanguage` - Copy to language (free mode)
- `version` - Workspace operations

### Getting Created Record UIDs

```php
// After process_datamap(), get the real UID
$realUid = $dataHandler->substNEWwithIDs['NEW123'];

// For copied records
$dataHandler->copyMappingArray_merged['tt_content'][42]; // Returns new UID
```

### Cache Operations

```php
$dataHandler->start([], []);
$dataHandler->clear_cacheCmd('pages');    // Clear all page cache
$dataHandler->clear_cacheCmd('all');      // Clear all caches (admin only)
$dataHandler->clear_cacheCmd(123);        // Clear specific page cache
```

## Reference Files

- `references/data-array.md` - Data array patterns and examples
- `references/command-array.md` - Command operations reference
- `references/workspaces.md` - Workspaces, versioning, staging, publishing
- `references/hooks-events.md` - Hook into DataHandler operations
- `references/common-patterns.md` - Typical use cases and solutions

## Critical Rules

### ⚠️ NEVER Inject DataHandler
```php
// ❌ WRONG - DataHandler is stateful
public function __construct(private DataHandler $dataHandler) {}

// ✅ CORRECT - Always create new instance
$dataHandler = GeneralUtility::makeInstance(DataHandler::class);
```

### ⚠️ Backend Context Required
DataHandler requires `$GLOBALS['BE_USER']`. In CLI commands:
```php
\TYPO3\CMS\Core\Core\Bootstrap::initializeBackendAuthentication();
```

### ⚠️ TCA Configuration Required
Fields must be configured in TCA to be processed. If `type` is `none` or invalid, DataHandler ignores the field.

### ⚠️ sys_file Table Blocked
Direct modifications to `sys_file` are blocked since TYPO3 11.5.35/12.4.11/13.0.1 for security.

## Common Patterns

### Create Page with Content

```php
$data = [
    'pages' => [
        'NEW_page' => [
            'pid' => 1,
            'title' => 'New Page',
            'doktype' => 1,
        ],
    ],
    'tt_content' => [
        'NEW_content' => [
            'pid' => 'NEW_page',  // Reference to new page
            'CType' => 'text',
            'header' => 'Welcome',
            'bodytext' => 'Content here',
        ],
    ],
];

$dataHandler = GeneralUtility::makeInstance(DataHandler::class);
$dataHandler->start($data, []);
$dataHandler->process_datamap();

$pageUid = $dataHandler->substNEWwithIDs['NEW_page'];
$contentUid = $dataHandler->substNEWwithIDs['NEW_content'];
```

### Bulk Operations with Ordering

```php
// Create multiple records in correct order
$data = [
    'pages' => [
        'NEW_1' => ['pid' => 1, 'title' => 'Page 1'],
        'NEW_2' => ['pid' => 1, 'title' => 'Page 2'],
    ],
];

$dataHandler = GeneralUtility::makeInstance(DataHandler::class);
$dataHandler->reverseOrder = true;  // Preserve array order
$dataHandler->start($data, []);
$dataHandler->process_datamap();
```

### Copy Record with Modifications

```php
$cmd = [
    'tt_content' => [
        42 => [
            'copy' => [
                'action' => 'paste',
                'target' => 10,  // Page UID
                'update' => [
                    'header' => 'Copied: ' . $originalHeader,
                ],
            ],
        ],
    ],
];
```

### Workspace Operations

```php
// Publish (swap) a workspace version
$cmd['pages'][42]['version'] = [
    'action' => 'swap',
    'swapWith' => 123,  // Workspace version UID
];

// Discard workspace changes
$cmd['pages'][42]['version'] = [
    'action' => 'clearWSID',
];

// Set approval stage
$cmd['pages'][42]['version'] = [
    'action' => 'setStage',
    'stageId' => 10,  // -1=rejected, 0=editing, 1=review, 10=publish
    'comment' => 'Ready for review',
];

// Bypass workspace restrictions (use carefully!)
$dataHandler->bypassWorkspaceRestrictions = true;
```

See `references/workspaces.md` for complete workspace patterns.

## Hooking Into DataHandler

### Legacy Hooks (still supported)

```php
// ext_localconf.php
$GLOBALS['TYPO3_CONF_VARS']['SC_OPTIONS']['t3lib/class.t3lib_tcemain.php']['processDatamapClass'][]
    = \MyVendor\MyExt\Hook\DataHandlerHook::class;

$GLOBALS['TYPO3_CONF_VARS']['SC_OPTIONS']['t3lib/class.t3lib_tcemain.php']['processCmdmapClass'][]
    = \MyVendor\MyExt\Hook\DataHandlerHook::class;
```

### Hook Methods

```php
class DataHandlerHook
{
    // Before record is saved
    public function processDatamap_preProcessFieldArray(
        array &$fieldArray,
        string $table,
        string|int $id,
        DataHandler $dataHandler
    ): void {}

    // After record is saved
    public function processDatamap_postProcessFieldArray(
        string $status,  // 'new' or 'update'
        string $table,
        string|int $id,
        array $fieldArray,
        DataHandler $dataHandler
    ): void {}

    // After all records processed
    public function processDatamap_afterAllOperations(DataHandler $dataHandler): void {}

    // Before command executed
    public function processCmdmap_preProcess(
        string $command,
        string $table,
        int $id,
        mixed $value,
        DataHandler $dataHandler,
        bool|string $pasteUpdate
    ): void {}

    // After command executed
    public function processCmdmap_postProcess(
        string $command,
        string $table,
        int $id,
        mixed $value,
        DataHandler $dataHandler,
        bool|string $pasteUpdate,
        bool|string $pasteDatamap
    ): void {}
}
```

## Error Handling

```php
$dataHandler = GeneralUtility::makeInstance(DataHandler::class);
$dataHandler->start($data, $cmd);
$dataHandler->process_datamap();
$dataHandler->process_cmdmap();

if ($dataHandler->errorLog !== []) {
    foreach ($dataHandler->errorLog as $error) {
        $this->logger->error('DataHandler error', ['message' => $error]);
    }
}
```

## Verification Checklist

Before using DataHandler:
- [ ] TCA is properly configured for all tables/fields
- [ ] Backend user context exists (`$GLOBALS['BE_USER']`)
- [ ] User has permissions for the operation
- [ ] Creating new instance (not injecting)
- [ ] Checking `errorLog` after operations
- [ ] Using `substNEWwithIDs` to get created record UIDs

---

> **Documentation:** [TYPO3 DataHandler Reference](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/DataHandler/Index.html)

