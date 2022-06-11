import Dropdown from "./Dropdown";

function HeaderComponents() {
    return (
        <div className="flex text-gray-700 justify-evenly text-sm lg:text-base lg:justify-start lg:space-x-36
        lg:pl-60 border-b-2 my-1 items-center">
           <Dropdown />
        </div>
    )

}

export default HeaderComponents;