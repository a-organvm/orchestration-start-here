export interface WorkspaceEntry {
  name: string;
  path: string;
  tech_stack?: string[];
}

export interface OrchestratorManifest {
  components: {
    workspaces: WorkspaceEntry[];
  };
}

export declare class OrchestratorScout {
  constructor(manifestPath: string);
  loadManifest(): Promise<OrchestratorManifest>;
}
