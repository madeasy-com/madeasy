import Head from "next/head";
import router from "next/router";

export default function About() {
    const Home = e => {
        router.push(`/`);
    }


    return (
        <div>
            <Head>
                <title>About MadEZ</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <header className='flex w-full p-5 justify-between text-sm text-gray-700' >
                <div className='flex space-x-4 items-center'>
                    <p className='link' onClick={Home}> Home </p>
                </div>

                <div className='flex space-x-4 items-center'>
                    <p className='link'> Dark Mode </p>
                </div>
            </header>

            <div class="flex flex-col mt-8">
                <div class="container max-w-7xl px-4">
                    <div class="flex flex-wrap justify-center text-center mb-24">
                        <div class="w-full lg:w-6/12 px-4">
                            <h1 class="text-gray-900 text-4xl font-bold mb-8">
                                Meet the Team
                            </h1>
                            <p class="text-gray-700 text-lg font-light">
                                Featuring the most racist people in UW-Madison.
                            </p>
                        </div>
                    </div>

                    <div class="flex flex-wrap">
                        <div class="w-full md:w-6/12 lg:w-3/12 mb-6 px-6 sm:px-6 lg:px-4">
                            <div class="flex flex-col">
                                <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">
                                    <img class=" rounded-lg drop-shadow-md hover:drop-shadow-xl transition-all duration-200 delay-100"
                                        src="https://images.unsplash.com/photo-1634193295627-1cdddf751ebf?fit=clamp&w=400&h=400&q=80" />
                                </a>

                                <div class="text-center mt-6">
                                    <h1 class="text-gray-900 text-xl font-bold mb-1">
                                        Pratham Baid
                                    </h1>
                                    <div class="text-gray-700 font-light mb-2">
                                        Terrified of meat
                                    </div>
                                </div>
                            </div>
                        </div>


                        <div class="w-full md:w-6/12 lg:w-3/12 mb-6 px-6 sm:px-6 lg:px-4">
                            <div class="flex flex-col">
                                <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">
                                    <img class="rounded-lg drop-shadow-md hover:drop-shadow-xl transition-all duration-200 delay-100"
                                        src="https://images.unsplash.com/photo-1634193295627-1cdddf751ebf?fit=clamp&w=400&h=400&q=80" />
                                </a>
                                <div class="text-center mt-6">
                                    <h1 class="text-gray-900 text-xl font-bold mb-1">
                                        Mr. Sex
                                    </h1>
                                    <div class="text-gray-700 font-light mb-2">
                                        So Sex
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="w-full md:w-6/12 lg:w-3/12 mb-6 px-6 sm:px-6 lg:px-4">
                            <div class="flex flex-col">
                                <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">
                                    <img class="rounded-lg drop-shadow-md hover:drop-shadow-xl transition-all duration-200 delay-100"
                                        src="https://images.unsplash.com/photo-1634193295627-1cdddf751ebf?fit=clamp&w=400&h=400&q=80" />
                                </a>

                                <div class="text-center mt-6">
                                    <h1 class="text-gray-900 text-xl font-bold mb-1">
                                        Justin Wong
                                    </h1>

                                    <div class="text-gray-700 font-light mb-2">
                                        Squid Game Person
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="w-full md:w-6/12 lg:w-3/12 mb-6 px-6 sm:px-6 lg:px-4">
                            <div class="flex flex-col">
                                <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">
                                    <img class="rounded-lg drop-shadow-md hover:drop-shadow-xl transition-all duration-200 delay-100"
                                        src="https://images.unsplash.com/photo-1634193295627-1cdddf751ebf?fit=clamp&w=400&h=400&q=80" />
                                </a>

                                <div class="text-center mt-6">
                                    <h1 class="text-gray-900 text-xl font-bold mb-1">
                                        Nithin Chinni Shwarmi
                                    </h1>

                                    <div class="text-gray-700 font-light mb-2">
                                        Most Hugest Penis
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
