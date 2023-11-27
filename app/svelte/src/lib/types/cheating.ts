import type { Assignment } from './assignment'

export type CheatingResults = Record<number, { cheatCount: number; assignments: Assignment[] }>
