"use client"

import ContentEditable from '@/components/chat/content-edit'
import Image from 'next/image'
import { useState } from "react"

export default function ContainerChat() {
    const [startChat, setStartChat] = useState<boolean>(false);
    const [response, setResponse] = useState<any>(null)

    return (
        <div className='z-10 w-full h-screen h-min-screen flex flex-col justify-between p-6 items-center'>

            <div className='rounded-full md:h-48 md:w-48 h-40 w-40 relative cursor-pointer mt-8'>
                <div className='image-circle p-2 relative'>
                    <div className='line absolute inset-0 rounded-full'></div>
                    <Image
                        src="/seed-jr.jpg"
                        width={250}
                        height={250}
                        className='rounded-full '
                        alt="Seed Jr."
                    />
                </div>
            </div>

            {response && (
                <div>
                    {JSON.stringify(response)}
                </div>
            )}

            <div className='w-full '>
                <ContentEditable
                    setStartChat={setStartChat}
                    setResponse={setResponse}
                />
            </div>
        </div>
    )
}

