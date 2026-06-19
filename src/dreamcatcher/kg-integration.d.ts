export interface KnowledgeGraphDecisionInput {
  decision: string;
  rationale: string;
  category: string;
  project: string;
  tags: string[];
}

export interface KnowledgeGraphDecision {
  decision: string;
  rationale: string;
  category: string;
  project?: string;
}

export interface KnowledgeGraphFileChange {
  path: string;
  operation: string;
  modified_at: string;
}

export interface ProjectContext {
  recent_decisions: KnowledgeGraphDecision[];
  recent_files: KnowledgeGraphFileChange[];
}

export declare class KnowledgeGraphIntegration {
  logDecision(input: KnowledgeGraphDecisionInput): Promise<void>;
  findPastDecisions(query: string, project: string): Promise<KnowledgeGraphDecision[]>;
  findSimilarWork(query: string, project: string): Promise<KnowledgeGraphDecision[]>;
  getProjectContext(project: string, hours: number): Promise<ProjectContext>;
  findRecentFileChanges(project: string, hours: number): Promise<KnowledgeGraphFileChange[]>;
}
