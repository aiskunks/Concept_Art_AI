import { useAuth } from "@clerk/nextjs";
import { createClient } from "@supabase/supabase-js";
import { AppProps } from "next/app";
import React, { FC, useEffect, useState } from "react";
import useSupabaseClient from "./store/useSupabaseClient";
import { useRouter } from "next/router";
import { fetchUser } from "./SupabaseClient";
import useSupabaseUser from "./store/useSupabaseUser";

interface UserContextProvider {
  children?: React.ReactNode;
}

const supabaseClient = async (supabaseAccessToken) => {
  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL,
    process.env.NEXT_PUBLIC_SUPABASE_KEY,
  );
  return supabase;
};

export const UserContextProvider: FC<UserContextProvider> = ({ children }) => {
  const router = useRouter();

  const { getToken, isLoaded, isSignedIn, userId } = useAuth();

  const { setSupabaseClient, setIsSupabaseReady } = useSupabaseClient();
  const { setIsSupabaseUserReady, setUserDetails } = useSupabaseUser();

  useEffect(() => {
    if (isLoaded) {
      if (isSignedIn) {
        createSupabaseClient();
      }
    }
  }, [isLoaded, isSignedIn]);

  const createSupabaseClient = async () => {
    const supabaseAccessToken = await getToken({
      template: "art-lab-supabase",
    });

    const supabase = await supabaseClient(supabaseAccessToken);
    setSupabaseClient(supabase);
    setIsSupabaseReady(true);

    if (!(router.pathname === "/onboarding")) {
      const { data, error } = await fetchUser(supabase, userId);
      if (data.length === 0) {
        router.replace("/onboarding");
        return;
      }

      setUserDetails(data[0]);
      setIsSupabaseUserReady(true);
    }
  };

  return <>{children}</>;
};
