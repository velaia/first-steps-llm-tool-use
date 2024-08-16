# Use a pipeline as a high-level helper
import json
from transformers import pipeline
import safe_tools


messages = [
    {"role": "system", "content": 
"""
You are a function calling AI model. You are provided with function signatures within <tools></tools> XML tags. You may call one or more functions to assist with the user query. Don't make assumptions about what values to plug into functions. For each function call return a json object with function name and arguments within <tool_call></tool_call> XML tags as follows:
<tool_call>
{"name": <function-name>,"arguments": <args-dict>}
</tool_call>

Here are the available tools:
<tools> {
    "name": "calculate_sum",
    "description": "Calculate the sum of all arguments",
    "parameters": {
        "properties": {
            "addends": {
                "description": "Addends being summed up",
                "type": "string"
            },
        },
        "required": [
            "addends"
        ],
        "type": "object"
    }
},
{
    "name": "calculate_product",
    "descriptin": "Calculate the product of the supplied factors",
    "parameters": {
        "properties": {
            "factors": {
                "description": "Comma-delimited list of factors of the product",
                "type": "string"
            }
        },
        "required": [
            "factors"
        ],
        "type": "object"
    }
},
{
    "name": "count_characters",
    "descriptin": "Count the number of characters of a given type within a word or phrase",
    "parameters": {
        "properties": {
            "word_phrase": {
                "description": "Word or phrase of which the characters shall be counted",
                "type": "string"
            }
        },
        "required": [
            "word_phrase"
        ],
        "type": "object"
    }
}
</tools>
"""},
    {"role": "user", "content": "How often does the character n occur in the word 'functioning'?"},
]
pipe = pipeline("text-generation", model="Groq/Llama-3-Groq-8B-Tool-Use", device='mps', 
                temperature=0.1, top_p=0.65)
output = pipe(messages)
command =  json.loads(output[0]['generated_text'][2]['content'])

function_to_call = getattr(safe_tools, command['name'])
result = function_to_call(command['arguments']['word_phrase'], 'n')
print(f"{result = }")
