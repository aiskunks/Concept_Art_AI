import Link from "next/link";
import React from "react";

const Logo = () => {
  return (
    <Link href={"/"}>
      <h1 className="font-Josefin font-semibold text-white text-3xl">Art Lab</h1>
    </Link>
  );
};

export default Logo;
