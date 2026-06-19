import type { OrchestratorScout } from './scout.js';

export interface TestResult {
  success: boolean;
}

export declare class OrchestratorTester {
  constructor(scout: OrchestratorScout);
  runTests(workspaceName: string, targetRoot: string): Promise<TestResult>;
}
