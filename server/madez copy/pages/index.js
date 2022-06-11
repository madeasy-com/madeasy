import Head from 'next/head'
import {XIcon, ViewGridIcon} from "@heroicons/react/solid";
import {SearchIcon} from "@heroicons/react/outline";
import Image from 'next/image';
import { useRef , useState} from 'react';
import { useRouter } from 'next/router';
import data from '../data.json'

export default function Home() {
  
  const searchInputRef = useRef(null);
  const router = useRouter();
  const search = e => {
    e.preventDefault();
    const term = searchInputRef.current.value;
    if(!term) return
    router.push(`/search?term=${term}`);
  }
  const about = () => {
    router.push(`/about`)
  }
  const test = () => {
    router.push(`/test`)
  }

  const [filteredData, setFilteredData] = useState([]);
  const [wordEntered, setWordEntered] = useState("");

  const handleFilter = (event) => {
    const searchWord = event.target.value;
    setWordEntered(searchWord);
    const newFilter = data.filter((value) => {
      return value.title.toLowerCase().includes(searchWord.toLowerCase());
    });

    if (searchWord === "") {
      setFilteredData([]);
    } else {
      setFilteredData(newFilter);
    }
  };

  const clearInput = () => {
    setFilteredData([]);
    setWordEntered("");
  };

  const setInput = (value) => {
    setWordEntered(value);
  };


  return (
    <div>
      <Head>
        <title>MadEZ </title>
        <link rel="icon" href="/favicon.ico" /> 
      </Head> 

      <header className='flex w-full p-5 justify-between text-sm text-gray-700' >

        <div className='flex space-x-4 items-center'>
          <p className='link' onClick={about}> About </p>
        </div>

        <div className='flex space-x-4 items-center'>
          <p className='link' onClick={test}> Test </p>
        </div>

        <div className='flex space-x-4 items-center'>
          <p className='link'> Dark Mode </p>
          <ViewGridIcon className='h-10 w-10 p-2'/>
        </div>
      </header>


      <form className='flex flex-col items-center mt-44 flex-grow'>
        <Image src='https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png' 
          height = {100}
          width = {300}
        />
        <div className='flex w-full mt-5 hover:shadow-lg max-w-md rounded-full border 
          border-gray-200 px-5 py-3 items-center sm-max-w-xl lg:max-w-2xl' >
          <SearchIcon className='h-5 mr-3 text-gray-500'/>
          <input  
                  placeholder='Enter Major here' 
                  type='text' 
                  className=' flex-grow focus: outline-none' 
                  value = {wordEntered}
                  onChange={handleFilter}
                  />
          <XIcon className='h-5  text-gray-500 cursor-pointer transition-duration-100 transform hover:scale-125' onClick={clearInput}/>
        </div>
        {filteredData.length != 0 && (
          <div className="flex-col h-{50px} justify-center rounded border 
          border-gray-200">
            {filteredData.slice(0, 15).map((value) => {
              return (
                  <p className='cursor-pointer mb-2 hover:shadow-lg hover:text-blue-500' >{value.title} </p>
              );
            })}
          </div>
        )}

        <div className='flex flex-col w-1/2 space-y-2 justify-center mt-4 sm: space-y-0
        sm:flex-row sm:space-x-4'>
          <button className='btn' onClick={search}> Search </button>
        </div>
      </form> 
    </div>
  )
}
 