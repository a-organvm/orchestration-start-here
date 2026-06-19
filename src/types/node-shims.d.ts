type BufferEncoding = 'utf8' | 'utf-8';

declare module 'fs/promises' {
  interface MkdirOptions {
    recursive?: boolean;
  }

  type WriteFileOptions = BufferEncoding | { encoding?: BufferEncoding };

  export function mkdir(path: string, options?: MkdirOptions): Promise<void>;
  export function writeFile(
    path: string,
    data: string | Uint8Array,
    options?: WriteFileOptions,
  ): Promise<void>;

  const fsPromises: {
    mkdir: typeof mkdir;
    writeFile: typeof writeFile;
  };

  export default fsPromises;
}

declare module 'path' {
  export function dirname(path: string): string;
  export function join(...paths: string[]): string;
  export function resolve(...paths: string[]): string;

  const path: {
    dirname: typeof dirname;
    join: typeof join;
    resolve: typeof resolve;
  };

  export default path;
}
