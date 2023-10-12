import { Input } from "components/ui/input";
import { Button } from "components/ui/button";

export default function Page() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-12 px-4">
      <h1 className="mb-8 text-2xl font-bold">Login Page</h1>
      <form className="p-6 rounded shadow-md w-96">
        <div className="mb-4">
          <label htmlFor="email" className="block mb-2 text-sm font-bold">
            Email
          </label>
          <Input id="email" type="email" placeholder="Enter your email" required />
        </div>
        <div className="mb-4">
          <label htmlFor="password" className="block mb-2 text-sm font-bold">
            Password
          </label>
          <Input id="password" type="password" placeholder="Enter your password" required />
        </div>
        <Button type="submit" className="w-full mt-4">
          Login
        </Button>
      </form>
    </div>
  );
}
