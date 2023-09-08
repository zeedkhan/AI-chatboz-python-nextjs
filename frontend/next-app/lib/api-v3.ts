import { NextRequest, NextResponse } from "next/server";

interface ApiResponse {
    data: any;
    error: string | null;
}

interface Options {
    withCredentials: boolean
    headers: {
        Authorization: string
    }
}


class ApiV3 {
    private jwt_token: string | null = null;
    private baseUrl: string = "http://backend:8000";
    private refresh_token: string | null = null;
    private req: NextRequest = {} as NextRequest;
    res: NextResponse = {} as NextResponse;
    private options: Options = {
        withCredentials: true,
        headers: {
            Authorization: "" as string  // Ensure 'Bearer ' is correctly appended

        }
    }


    constructor(req: NextRequest, res: NextResponse, jwt_token: string | null, refresh_token: string | null) {
        this.req = req;
        this.res = res;
        this.jwt_token = jwt_token;
        this.refresh_token = refresh_token;
        this.options.headers = {
            ...this.options.headers,
            Authorization: "Bearer " + this.refresh_token,
        };
    }


    async getSession() {
        if (!this.Authenticated()) {
            return null;
        }
        const req = `${this.baseUrl}/user/`;
        const options: Options = {
            withCredentials: true,
            headers: {
                Authorization: "Bearer " + this.jwt_token
            }
        }

        try {
            const res = await fetch(req, options);
            const data = await res.json();
            const user = data;

            return {
                data: user, error: null
            }

        } catch {
            return {
                data: null, error: 'An error occurred while making the request'
            }
        }
    }

    async Authenticated(): Promise<NextResponse> {
        const response = NextResponse.next();

        if (!this.refresh_token) {
            return this.res
        }
        if (!this.jwt_token) {
            const request = await refreshToken(this.refresh_token);
            if (request.data) {
                response.cookies.set({
                    name: 'jwt_token',
                    value: request?.data || "",
                });
            }
        }
        return response
    }
}


export const refreshToken = async (refresh_token: string): Promise<ApiResponse> => {
    const req = `http://backend:8000/refresh-token/`;

    const options: Options = {
        withCredentials: true,
        headers: {
            Authorization: "Bearer " + refresh_token
        }
    }

    try {
        const res = await fetch(req, options);
        const data = await res.json();
        const token = data.access_token;

        return {
            data: token, error: null
        }

    } catch (error) {
        // console.error('Error making API request:', error);
        return { data: null, error: "Unauthorized" }
    }

}


export default ApiV3