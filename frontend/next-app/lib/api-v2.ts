import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import { cookies } from "next/headers"
import { NextResponse, NextRequest } from 'next/server'


type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE'; // Add other methods as needed

interface ApiResponse {
    data: any;
    error: string | null;
}

class ApiV2 {
    private jwt_token: string | null = null;
    private baseUrl: string;
    private refresh_token: string | null = null;

    constructor() {
        const cStore = cookies();
        this.baseUrl = "http://backend:8000"; // Set your base URL here
        this.jwt_token = cStore.get("jwt_token")?.value || null;
        this.refresh_token = cStore.get("refresh_token")?.value || null;
    }

    private async refreshToken() {
        const req = "http://backend:8000/refresh-token/";
        const options = {
            withCredentials: true,
            headers: {
                'Authorization': 'Bearer ' + this.refresh_token // Ensure 'Bearer ' is correctly appended
            }
        }

        try {
            const res: AxiosResponse = await axios.get(req, options);
            const token = await res.data.access_token;

            this.jwt_token = token;

            return token

        } catch (error) {
            // console.error('Error making API request:', error);
            return { data: null, error: 'An error occurred while making the request' };
        }

    }

    async getToken() {
        if (!this.jwt_token && !this.refresh_token) {
            return;
        }

        if (!this.jwt_token) {
            const token = await this.refreshToken();
            if (token) {
                return {
                    access_token: token,
                    refresh_token: this.refresh_token
                };
            }
        }
    }

    private async request(method: HttpMethod, endpoint: string, data?: {}): Promise<ApiResponse> {
        if (!this.jwt_token) {
            await this.getToken()
        }

        const headers = {
            Authorization: `Bearer ${this.jwt_token}`,
            'Content-Type': 'application/json',
        };

        const config: AxiosRequestConfig = {
            method,
            headers,
            withCredentials: true,
        };

        if (data) {
            config.data = data;
        }

        try {
            const response: AxiosResponse = await axios(`${this.baseUrl}${endpoint}`, config);
            return {
                data: response.data,
                error: null,
            };
        } catch (error) {
            // console.error('Error making API request:', error);
            return { data: null, error: 'An error occurred while making the request' };
        }
    }

    async get(endpoint: string): Promise<ApiResponse> {
        return this.request('GET', endpoint);
    }

    async post(endpoint: string, data: any): Promise<ApiResponse> {
        return this.request('POST', endpoint, data);
    }

    async get_user(): Promise<ApiResponse> {
        return this.request('GET', '/user/');
    }

    async logout(): Promise<ApiResponse> {
        return this.request("GET", '/logout/')
    }

    // Add other methods like put() and delete() as needed
}

export default ApiV2;


