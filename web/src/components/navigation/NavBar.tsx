import Link from "next/link";
import { SVGProps } from "react";
import Image from "next/image";

function NavBar() {
  return (
    <header className="px-8 lg:px-16 h-14 flex items-center">
        <Link className="flex items-center justify-center gap-x-4" href="/">
        <Image
          alt="FERNEC icon"
          className="h-14 w-14"
          src="/FERNEC_icon.png"
          width="240"
          height="240"
        />
        <h1 className="text-2xl font-bold">FERNEC</h1>
        </Link>
        <nav className="ml-auto flex gap-4 sm:gap-6">
        </nav>
    </header>
  );
}

export default NavBar;
