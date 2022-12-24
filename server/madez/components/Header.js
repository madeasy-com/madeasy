import { SearchIcon, XIcon } from '@heroicons/react/solid';
import Image from 'next/image'
import { useRouter } from 'next/router';
import {useRef} from 'react'


function Header(){
    const router = useRouter();
    const searchInputRef = useRef(null);
    const search = e => {
        e.preventDefault();
        const term = searchInputRef.current.value;
        if(!term) return
        router.push(`/search?term=${term}`);
      }

    return( 
        <header className='sticky top-0 bg-white'>
            <div className='flex w-full p-6 items-center'>
                <Image src='https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png' 
                height = {40}
                width = {120}
                 className = 'cursor-pointer'
                onClick={() => router.push('/')}
                />
                <form className='flex flex-grow border border-gray-200 
                rounded-full flex-grow shadow-lg max-w-3xl px-6 py-3 ml-10 mr-10 items-center'>
                    <input ref={searchInputRef} className="flex-grow w-full focus:outline-none" type='text'/>
                    <XIcon 
                    onClick={() => searchInputRef.current.value = ""}
                    className='h-7 sm:mr-3 text-gray-500 cursor-pointer transition-duration-100 transform hover:scale-125'/>
                    <SearchIcon className='h-6 text-blue-500 hidden sm:inline-flex'/>
                    <button hidden type='submit' onClick={search}/>
                </form>
            </div>
        </header>
    ) 

}

export default Header;