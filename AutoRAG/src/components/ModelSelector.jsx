// import React from 'react';
import PropTypes from 'prop-types';

const models = [
  { name: 'Ollama/llama2', value: 'ollama/llama2' },
  { name: 'Ollama/mistral', value: 'ollama/mistral' },
  { name: 'Ollama/vicuna', value: 'ollama/vicuna' },
  { name: 'HuggingFace/gpt2', value: 'hf/gpt2' },
  { name: 'HuggingFace/bert-base-uncased', value: 'hf/bert-base-uncased' },
  { name: 'HuggingFace/t5-base', value: 'hf/t5-base' },
  { name: 'Anthropic Claude', value: 'anthropic/claude' },
  { name: 'OpenAI GPT-3.5', value: 'openai/gpt-3.5-turbo' },
  { name: 'OpenAI GPT-4', value: 'openai/gpt-4' },
];

const ModelSelector = ({ onSelect }) => {
  return (
    <div className="mb-4">
      <select
        onChange={(e) => onSelect(e.target.value)}
        className="w-full p-2 border rounded shadow-sm focus:ring-2 focus:ring-green-500 focus:border-green-500 bg-white"
      >
        <option value="">Choose a model</option>
        {models.map((model) => (
          <option key={model.value} value={model.value}>
            {model.name}
          </option>
        ))}
      </select>
    </div>
  );
};

ModelSelector.propTypes = {
  onSelect: PropTypes.func.isRequired,
};

export default ModelSelector;