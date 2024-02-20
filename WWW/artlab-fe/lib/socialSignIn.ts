import { supabase } from "./supabase";

export default async function signInWithGoogle() {
    const { data, error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
    })

    if (error) console.log(error);
}  