import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://hyeifxvxifhrapfdvfry.supabase.co'
const supabaseAnonKey = 'sb_publishable_RMMpXpKBjUDFNQt9_X0aog_GzLv4jzd'

export const supabase = createClient(supabaseUrl, supabaseAnonKey) 