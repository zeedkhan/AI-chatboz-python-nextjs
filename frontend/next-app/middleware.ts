import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";
import ApiV3 from "./lib/api-v3";


export const middleware = async (req: NextRequest): Promise<NextResponse> => {
  const jwt_token = req.cookies.getAll().find(i => i.name === "jwt_token")?.value || null;
  const refresh = req.cookies.getAll().find(i => i.name === "refresh_token")?.value || null;

  const initApi = await new ApiV3(req, NextResponse.next(), jwt_token, refresh).Authenticated();
  
  return initApi
};