"use server"

import { Session } from 'next-auth';
import { cookies } from 'next/headers'

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE'; // Add other methods as needed

type ToolsResponse = {
    tools: [Tool]
} | null

type Tool = {
    name: string, description: string, parent_function: string | null, parameters: any
}

type User = {
    user: Session
} | null

async function customFetch<T>(url: string, method: HttpMethod, data?: Record<string, any>): Promise<T | null> {
    const ck = cookies().getAll();
    const jwt_token = ck.find(i => i.name === "jwt_token")?.value || null;

    const headers: HeadersInit = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + jwt_token,
    };

    const config: RequestInit = {
        method,
        headers,
        credentials: "include",
        body: (method === 'POST' || method === 'PUT') && data ? JSON.stringify(data) : undefined,
    };

    try {
        const response = await fetch(url, config);

        if (!response.ok) {
            // Instead of throwing an error, return null for HTTP errors
            return null;
        }

        const responseData = await response.json();
        return responseData;
    } catch (error) {
        // Instead of throwing an error, return null for network errors
        return null;
    }
}

let user: User | null = null

export const getSession = async (): Promise<User | null> => {
    if (user !== null) {
        return user
    }
    const request = await customFetch<User>('http://backend:8000/user/', 'GET')

    if (request?.user) {
        user = request
        return request
    }

    return null
}


export const getTools = async (): Promise<[Tool] | null> => {
    const request = await customFetch<ToolsResponse>('http://backend:8000/chat/tools', 'GET')

    if (request?.tools) {
        return request.tools
    }

    return null
}

interface StartChat {
    goal: string;
    language: string;
    ai_prefix: string;
    user: string;
}


export const startChat = async (data: StartChat): Promise<any> => {
    const request = await customFetch<any>('http://backend:8000/chat/chat/', "POST", data);

    if (request) {
        return request
    }

    return null;
}

// example test
// const test = async () => {
//     const data = {
//         cookies: ['test-1', 'test-2', 'test-3']
//     }

//     const request = await customFetch<any>("http://backend:8000/chat/test", 'POST', data);

//     if (request) {
//         console.log(request)
//         return request
//     }

//     return null
// }