import { createServerComponentClient } from "@supabase/auth-helpers-nextjs";
import { cookies } from "next/headers";
import { Database } from "../../lib/database.types";
// import AccountForm from './account-form'
import Main from "components/pages/main";
import { Button } from "components/ui/button";
export default async function Account() {
  const supabase = createServerComponentClient<Database>({ cookies });

  const {
    data: { session },
  } = await supabase.auth.getSession();
  
  return (
    <>
      <h1>{session?.user.email}</h1>
      <form action="/auth/logout" method="post">
        <Button>Logout</Button>
      </form>

      <Main/>
    </>
  );
}
