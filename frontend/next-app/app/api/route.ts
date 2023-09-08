import type { NextApiRequest, NextApiResponse } from "next"


type ResponseData = {
  message: string
}

export async function GET(request: NextApiRequest, res: NextApiResponse<ResponseData>) {


  return res.status(200).json({ message: 'Hello from Next.js!' })
}
