import type { CheatingResults } from '$lib/types'
import { writable } from 'svelte/store'

export const cheaters = writable<CheatingResults>({})
