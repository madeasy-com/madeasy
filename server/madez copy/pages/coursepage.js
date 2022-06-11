import Head from "next/head";
import { useRouter } from "next/router";
import Header from "../components/Header";
import Piechart from '../components/piechart'
import Barchart from '../components/barchart'

function coursepage(){
    const router = useRouter();
    const home = () => {
        router.push(`/`)
      }
    return(
        <div>
            <Head>
                <title>About MadEZ</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <Header/>
            <div className="flex text-gray-700 justify-evenly text-sm lg:text-base lg:justify-start lg:space-x-36
        lg:pl-60 border-b-2 my-1 items-center">
        </div>
            <div class="flex flex-col mt-8">
                <div class="container max-w-7xl px-4">
                <div class="flex flex-wrap justify-center text-center mb-5">
                        <div class="w-full lg:w-6/12 px-4">
                            <h1 class="text-gray-900 text-4xl font-bold">
                                General Chemistry I
                            </h1>
                            <p class="text-gray-700 text-lg font-light">
                                Chem 103
                            </p>
                        </div>
                    </div>

                    <div class="flex flex-wrap justify-center text-center mb-5">
                        <Piechart />
                    </div>
                    <div class="flex flex-wrap justify-center text-center mb-5">
                        <Barchart />
                    </div>
                </div>
            </div>
        </div>
    )
}
export default coursepage;