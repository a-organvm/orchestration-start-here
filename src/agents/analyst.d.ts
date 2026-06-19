import type { OrchestratorScout } from './scout.js';

export interface WorkspaceAnalysis {
  status: 'healthy' | 'drifted' | 'error';
  missing_modules: string[];
}

export declare class OrchestratorAnalyst {
  constructor(scout: OrchestratorScout);
  analyze(workspaceName: string, targetRoot: string): Promise<WorkspaceAnalysis>;
}
