import { useState } from "react";
import Checkbox from "./Checkbox"

const Dropdown = () => {
    const [isList, setIsList] = useState(false);
    const [isSubList, setIsSubList] = useState(0);
    return (
        <div>
            <div onClick={() => setIsList(!isList)} className="flex-grow w-64 p-4 shadow rounded bg-white text-sm font-medium leading-none flex items-center justify-between cursor-pointer">
                Filters
                <div>
                    {isList ? (
                        <div>
                            <svg width={10} height={6} viewBox="0 0 10 6" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M5.00016 0.666664L9.66683 5.33333L0.333496 5.33333L5.00016 0.666664Z" fill="#1F2937" />
                            </svg>
                        </div>
                    ) : (
                        <div>
                            <svg width={10} height={6} viewBox="0 0 10 6" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M5.00016 5.33333L0.333496 0.666664H9.66683L5.00016 5.33333Z" fill="#1F2937" />
                            </svg>
                        </div>
                    )}
                </div>
            </div>
            {isList && (
                <div className="w-200 mt-2 p-4 bg-white shadow rounded flex">
                    <div className="flex-col items-center justify-between">
                        <div className="flex items-center">
                            <svg width={12} height={12} viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M4.5 3L7.5 6L4.5 9" stroke="#4B5563" strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round" />
                            </svg>
                            <div className="flex items-center">
                                <p className="text-sm leading-normal ml-2 text-gray-800 cursor-pointer" onClick={() => setIsSubList(1)}>Breadth</p>
                            </div>
                        </div>
                        {isSubList === 1 && (
                            <div className=" pt-5">
                                <Checkbox option="Biological Sciences"/>
                                <Checkbox option="Humanities"/>
                                <Checkbox option="Literature"/>
                                <Checkbox option="Natural Sciences"/>
                                <Checkbox option="Physical Sciences"/>
                                <Checkbox option="Social Sciences"/>
                            </div>
                        )}
                    </div>
                    <div >
                        <div className="flex items-center justify-between ml-4">
                            <div className="flex items-center">
                                <svg onClick={() => setIsSubList(2)} width={12} height={12} viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M4.5 3L7.5 6L4.5 9" stroke="#4B5563" strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round" />
                                </svg>
                                <div className="pl-2 flex items-center">
                                    <p className="text-sm leading-normal text-gray-800 cursor-pointer" onClick={() => setIsSubList(2)}>GenEd</p>
                                </div>
                            </div>
                        </div>
                        {isSubList === 2 && (
                            <div className="pt-5">
                                <Checkbox option="Comm A"/>
                                <Checkbox option="Comm B"/>
                                <Checkbox option="QR A"/>
                                <Checkbox option="QR B"/>
                                <Checkbox option="Ethnic"/>
                            </div>
                        )}
                    </div>
                    <div>
                        <div className="flex-col items-center justify-between ml-4">
                            <div className="flex items-center">
                                <svg width={12} height={12} viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M4.5 3L7.5 6L4.5 9" stroke="#4B5563" strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round" />
                                </svg>
                                <div className=" flex items-center">
                                    <p className="text-sm leading-normal ml-2 text-gray-800 cursor-pointer" onClick={() => setIsSubList(3)}>Credits</p>
                                </div>
                            </div>
                            {isSubList === 3 && (
                                <div className="pt-5">
                                    <Checkbox option="1"/>
                                    <Checkbox option="2"/>
                                    <Checkbox option="3"/>
                                    <Checkbox option="4"/>
                                    <Checkbox option="5"/>     
                                </div>
                            )}
                        </div>
                    </div>
                    <div>
                        <div className="flex-col items-center justify-between ml-4">
                            <div className="flex items-center">
                                <svg width={12} height={12} viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M4.5 3L7.5 6L4.5 9" stroke="#4B5563" strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round" />
                                </svg>
                                <div className=" flex items-center">
                                    <p className="text-sm leading-normal ml-2 text-gray-800 cursor-pointer" onClick={() => setIsSubList(4)}>Level</p>
                                </div>
                            </div>
                            {isSubList === 4 && (
                                <div className="pt-5">
                                    <Checkbox option="Elementary"/>
                                    <Checkbox option="Intermediate"/>
                                    <Checkbox option="Advanced"/>
                                </div>
                            )}
                        </div>
                    </div>
                    <button className="ml-5 text-xs bg-indigo-100 hover:bg-indigo-200 rounded-md mt-3 font-medium py-2 h-12 w-12 leading-3 text-indigo-700">Select</button>
                </div>
            )}
            <style>
                {` .checkbox:checked + .check-icon {
                display: flex;
            }`}
            </style>
        </div>
    );
};
export default Dropdown;


