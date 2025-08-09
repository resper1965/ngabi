import { createClient, SupabaseClient } from '@supabase/supabase-js'
import { environment } from '../config/environment'

let supabase: SupabaseClient | null = null

export function getSupabase(): SupabaseClient | null {
  if (supabase) return supabase

  const url = environment.production.supabaseUrl || environment.development.supabaseUrl
  const key = environment.production.supabaseAnonKey || environment.development.supabaseAnonKey

  if (!url || !key) {
    if (import.meta.env.DEV) {
      // eslint-disable-next-line no-console
      console.warn('Supabase não configurado: defina VITE_SUPABASE_URL e VITE_SUPABASE_ANON_KEY')
    }
    return null
  }

  supabase = createClient(url, key)
  return supabase
}

export { supabase } 