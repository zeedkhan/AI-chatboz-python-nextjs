"use client"

import { startChat, getSession } from '@/lib/api-session';
import React, { useEffect, useState, useRef, ReactNode, Dispatch, SetStateAction } from 'react';
import { AiOutlineSend } from "react-icons/ai";
import { Session } from "next-auth"


function ContentEditable(
    { setStartChat, setResponse }:
        {
            setStartChat:
            Dispatch<SetStateAction<boolean>>;
            setResponse:
            Dispatch<SetStateAction<any>>;
        }
) {
    const [content, setContent] = useState<string>('');
    const [lines, setLines] = useState<number>(1);
    const [user, setUser] = useState<Session | null>(null);
    const [loading, setLoading] = useState<boolean>(false);

    const DEFAULT_AI = "Seed Junior"

    const handleSubmit = async () => {
        if (!user) {
            return;
        }
        setLoading(true);
        const response = await startChat({
            goal: content,
            ai_prefix: DEFAULT_AI,
            user: user.user?.email as string,
            language: 'English'
        });

        setContent("");

        if (response) {
            console.log(response)
            setResponse(response)
            setStartChat(true)
            setLoading(false);
        }


    }

    const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        const text = e.target.value;

        if (text === "") {
            setLines(1);
        } else {
            setLines(e.target.innerHTML.split("\n").length);
        }

        setContent(text);
    };


    const ref = React.createRef<HTMLTextAreaElement>();

    useEffect(() => {
        if (!ref.current) {
            return;
        }

        const countLines = ref.current?.innerHTML.split("\n").length || 1;
        setLines(countLines)

    }, [ref]);

    useEffect(() => {
        const getUser = async () => {
            const request = await getSession();
            if (request?.user) {
                setUser(request.user);
            }
            return request;
        };

        getUser();
    }, []);

    return (
        <div className='w-full h-full flex justify-center'>
            <div className='p-4 flex w-3/4 sm:w-2/3 md:w-1/2 shadow-xl border border-black/10 bg-white relative rounded-xl'>
                <textarea
                    ref={ref}
                    style={{ height: `${lines * 24}px` }}
                    className="max-h-[200px] overflow-y-hidden p-0 flex-1 resize-none border-0 bg-transparent focus:ring-0 focus-visible:ring-0 content-editable "
                    value={content}
                    placeholder="Send a message"
                    onChange={handleInputChange}
                />
                <div
                    onClick={async (e) => await handleSubmit()}
                    className={`absolute right-0 bottom-3 mr-2 flex items-center justify-center cursor-pointer p-2 ${content ? "bg-green-500" : "bg-white"}`}>
                    <AiOutlineSend color={content ? "white" : "black"} />
                </div>
            </div>
        </div>
    );
};

export default ContentEditable;
