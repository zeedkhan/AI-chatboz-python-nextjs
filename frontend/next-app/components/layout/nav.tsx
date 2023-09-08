"use server"

import { getSession } from "@/lib/api-session";
import Navbar from "./navbar";


export default async function Nav() {
  const session = await getSession();
  return (

    <Navbar session={session} />

  );
}


