---
name: ai-integration
description: Use when integrating LLMs (OpenAI, Qwen, Claude), extracting structured data from text, building prompts, parsing AI responses, handling JSON output, or implementing multi-step AI workflows
---

# AI Integration Patterns

**When to use**: Any LLM integration, structured data extraction, prompt engineering, or AI-powered content analysis.

## Overview

Battle-tested patterns for integrating AI models with reliable structured output parsing, multi-provider support, and comprehensive error handling.

## Supported Providers

- ✅ OpenAI (GPT-4, GPT-3.5)
- ✅ Qwen (通义千问)
- ✅ Anthropic Claude
- ✅ Custom API endpoints

## Key Capabilities

### 1. Structured Output Parsing

**Problem**: AI models return text, but you need JSON.

**Solution**: Multi-strategy parsing with automatic fallback:

```javascript
function parseStructuredOutput(text) {
  // Strategy 1: Direct JSON parse
  try {
    var parsed = JSON.parse(text);
    if (parsed && typeof parsed === 'object') {
      return parsed;
    }
  } catch (e) {}

  // Strategy 2: Extract from markdown code block
  var codeBlockMatch = text.match(/```(?:json)?\s*\n([\s\S]*?)\n```/);
  if (codeBlockMatch) {
    try {
      return JSON.parse(codeBlockMatch[1]);
    } catch (e) {}
  }

  // Strategy 3: Find JSON-like content
  var jsonMatch = text.match(/\{[\s\S]*\}/);
  if (jsonMatch) {
    try {
      return JSON.parse(jsonMatch[0]);
    } catch (e) {}
  }

  throw new Error('Failed to parse structured output');
}
```

### 2. Prompt Template Building

**Effective prompt structure**:
```javascript
function buildStructuredPrompt(content, schema) {
  var prompt = 'Analyze the following content and extract information.\n\n';
  prompt += 'Content:\n' + content + '\n\n';
  prompt += 'Return ONLY a JSON object with this exact structure:\n';
  prompt += JSON.stringify(schema, null, 2) + '\n\n';
  prompt += 'Rules:\n';
  prompt += '1. Return valid JSON only, no markdown\n';
  prompt += '2. Follow the schema exactly\n';
  prompt += '3. Use null for missing data\n';
  return prompt;
}
```

### 3. Multi-Provider Request Handler

**ES5 compatible HTTP request**:
```javascript
var https = require('https');

function callAI(provider, prompt, apiKey) {
  var options = {
    hostname: provider === 'openai' ? 'api.openai.com' : 'dashscope.aliyuncs.com',
    path: provider === 'openai' ? '/v1/chat/completions' : '/api/v1/services/aigc/text-generation/generation',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + apiKey
    }
  };

  var body = provider === 'openai'
    ? JSON.stringify({
        model: 'gpt-4',
        messages: [{role: 'user', content: prompt}],
        temperature: 0.1
      })
    : JSON.stringify({
        model: 'qwen-max',
        input: {prompt: prompt},
        parameters: {temperature: 0.1}
      });

  return new Promise(function(resolve, reject) {
    var req = https.request(options, function(res) {
      var data = '';
      res.on('data', function(chunk) { data += chunk; });
      res.on('end', function() {
        if (res.statusCode !== 200) {
          reject(new Error('API error: ' + res.statusCode));
        } else {
          resolve(JSON.parse(data));
        }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}
```

### 4. Schema Validation

```javascript
function validateSchema(data, schema) {
  var errors = [];

  for (var key in schema) {
    if (!data.hasOwnProperty(key)) {
      errors.push('Missing field: ' + key);
    } else if (typeof data[key] !== typeof schema[key]) {
      errors.push('Type mismatch for ' + key);
    }
  }

  if (errors.length > 0) {
    throw new Error('Schema validation failed: ' + errors.join(', '));
  }

  return true;
}
```

## Complete Workflow Pattern

```
Input Text
    ↓
[Build Prompt]
    - Add schema requirements
    - Add formatting rules
    - Add examples (few-shot)
    ↓
[Call AI API]
    - Select provider (OpenAI/Qwen/Claude)
    - Handle rate limits
    - Retry on errors
    ↓
[Parse Response]
    - Try direct JSON parse
    - Extract from code blocks
    - Find JSON patterns
    ↓
[Validate Schema]
    - Check required fields
    - Verify data types
    - Handle missing data
    ↓
Structured Output
```

## n8n Implementation

### Basic Structure
```javascript
// Code node 1: Build Prompt
var schema = {
  title: '',
  summary: '',
  tags: [],
  category: ''
};

var prompt = buildStructuredPrompt($input.item.json.content, schema);

return {
  json: Object.assign({}, $input.item.json, {
    prompt: prompt,
    schema: schema
  })
};
```

```javascript
// Code node 2: Call AI
var apiKey = process.env.OPENAI_API_KEY;
var response = await callAI('openai', $input.item.json.prompt, apiKey);

return {
  json: Object.assign({}, $input.item.json, {
    aiResponse: response
  })
};
```

```javascript
// Code node 3: Parse & Validate
var text = $input.item.json.aiResponse.choices[0].message.content;
var parsed = parseStructuredOutput(text);
validateSchema(parsed, $input.item.json.schema);

return {
  json: Object.assign({}, $input.item.json, parsed)
};
```

## Best Practices

1. **Low Temperature**: Use 0.1-0.3 for structured output
2. **Explicit Instructions**: "Return ONLY JSON, no markdown"
3. **Schema in Prompt**: Show exact structure expected
4. **Multi-Strategy Parsing**: Try multiple extraction methods
5. **Validate Always**: Check schema before using data
6. **Error Handling**: Retry on parse failures with adjusted prompt
7. **Few-Shot Examples**: Include 1-2 examples for complex schemas

## Common Patterns

### Pattern 1: Content Analysis
```
Text → AI Analysis → Structured Data (title, summary, tags)
```

### Pattern 2: Batch Processing
```
Multiple Items → Aggregate → Single AI Call → Split Results
```

### Pattern 3: Multi-Step Analysis
```
Extract → Classify → Enrich → Validate → Store
```

## Troubleshooting

### AI returns markdown instead of JSON
```javascript
// Add to prompt:
"CRITICAL: Return raw JSON only. No markdown formatting. No code blocks."
```

### Inconsistent field names
```javascript
// Add normalization:
var normalized = {
  title: data.title || data.Title || data.heading || '',
  // ... other fields
};
```

### Rate limiting
```javascript
// Add delay between requests
await new Promise(function(resolve) {
  setTimeout(resolve, 1000);  // 1 second
});
```

## Integration with Other Skills

- **video-processing**: Analyze video transcripts
- **notion-operations**: Save structured analysis to Notion
- **error-handling**: Retry AI calls on failures
- **debugging**: Validate AI output quality

## Full Code and Documentation

Complete implementations:
`/mnt/d/work/n8n_agent/n8n-skills/ai-integration/`

Files:
- `structured-output-handler.js` - Complete parsing solution
- `README.md` - Detailed patterns and examples
- Prompt templates and schemas
