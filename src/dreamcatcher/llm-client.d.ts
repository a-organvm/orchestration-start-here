export interface LLMResponse {
  content: string;
}

export declare class LLMClient {
  callAnthropic(model: string, systemPrompt: string, prompt: string): Promise<LLMResponse>;
  callOpenAI(model: string, systemPrompt: string, prompt: string): Promise<LLMResponse>;
  callGemini(model: string, systemPrompt: string, prompt: string): Promise<LLMResponse>;
}
