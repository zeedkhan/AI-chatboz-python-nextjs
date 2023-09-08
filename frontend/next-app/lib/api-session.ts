"use server"

import { cookies } from 'next/headers'


export const getSession = async () => {
    const ck = cookies().getAll();

    const jwt_token = ck.find(i => i.name === "jwt_token")?.value || null;

    const request = await fetch("http://backend:8000/user/", {
        credentials: "include",
        headers: {
            Authorization: "Bearer " + jwt_token
        }
    });

    if (request.ok) {
        const data = await request.json();
        console.log(data);
        return data
    }

    return null
}