import Head from 'next/head'
import Header from '../components/Header';
import HeaderComponents from '../components/HeaderComponents';
import SearchResults from '../components/SearchResults';

function Search({results}){
    console.log(results)
    return(
        <div>
            <Head> 
                <title>Search Results</title>    
                <link rel="icon" href="/favicon.ico" /> 
            </Head>
            <Header/>
            <HeaderComponents />
            <SearchResults/>
        </div>
    )
}
export default Search;

