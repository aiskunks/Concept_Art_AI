"use client";

import React, { useEffect, useState } from "react";
import { Input } from "components/ui/input";
import { Button } from "components/ui/button";
import signInWithGoogle from "lib/socialSignIn";

const Login = ()=> {
  // const { supabase } = useSupabase();

  const [isSignedUp, setIsSignedUp] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    setIsSignedUp(params.get("signedup") === "true");
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-12 px-4">
      <h1 className="mb-8 text-2xl font-bold">Login Page</h1>
      {isSignedUp && <p>You've successfully signed up! Please log in.</p>}

      <form
        className="p-6 rounded shadow-md w-96"
        method="post"
      >
        <div className="mb-4">
          <label htmlFor="email" className="block mb-2 text-sm font-bold">
            Email
          </label>
          <Input
            id="email"
            type="email"
            placeholder="Enter your email"
            name="email"
          />
        </div>
        <div className="mb-4">
          <label htmlFor="password" className="block mb-2 text-sm font-bold">
            Password
          </label>
          <Input
            id="password"
            type="password"
            placeholder="Enter your password"
            name="password"
          />
        </div>
        <div className="flex justify-evenly">
          <Button formAction="/auth/login">Sign In</Button>
          <Button variant={"outline"} formAction="/auth/sign-up">
            Sign Up
          </Button>
        </div>
      </form>

      <div className="flex justify-evenly mt-2">
        <Button variant={"outline"} 
          onClick={signInWithGoogle}
          >
            Sign In With Google
          </Button>
        </div>
    </div>
  );
}

export default Login;