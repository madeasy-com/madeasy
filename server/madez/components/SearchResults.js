import { v4 as uuid } from 'uuid';
import PerfectScrollbar from 'react-perfect-scrollbar';
import {
    Box,
    Card,
    CardHeader,
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableRow,
    TableSortLabel,
    Tooltip
} from '@mui/material';
import PaginationButtons from './PaginationButtons';
import { useRouter } from 'next/router';
import { useRef } from 'react';


const orders = [
    {
        id: uuid(),
        ref: 'CDD1049',
        courseName: 'Introduction to Chemistry',
        courseNumber: 'Chem103',
        averageGPA: 2.98,
        status: 'pending'
    },
    {
        id: uuid(),
        ref: 'CDD1049',
        courseName: 'Introduction to Chemistry',
        courseNumber: 'Chem103',
        averageGPA: 2.98,
        status: 'pending'
    },
    {
        id: uuid(),
        ref: 'CDD1049',
        courseName: 'Introduction to Chemistry',
        courseNumber: 'Chem103',
        averageGPA: 2.98,
        status: 'pending'
    },
    {
        id: uuid(),
        ref: 'CDD1049',
        courseName: 'Introduction to Chemistry',
        courseNumber: 'Chem103',
        averageGPA: 2.98,
        status: 'pending'
    },
    {
        id: uuid(),
        ref: 'CDD1049',
        courseName: 'Introduction to Chemistry',
        courseNumber: 'Chem103',
        averageGPA: 2.98,
        status: 'pending'
    },
    {
        id: uuid(),
        ref: 'CDD1049',
        courseName: 'Introduction to Chemistry',
        courseNumber: 'Chem103',
        averageGPA: 2.98,
        status: 'pending'
    }
];

function SearchResults({ results }) {
    const router = useRouter();
    const coursepage = e => {
        e.preventDefault();
        router.push(`/coursepage`);
      }
    return (
        <div className="mx-auto w-full px-3 sm:pl-[5%] md:pl-[14%] lg:pl-52">
            <Card >
                <CardHeader title="Courses" />
                <PerfectScrollbar>
                    <Box sx={{ minWidth: 800 }}>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell>
                                        Course Name
                                    </TableCell>
                                    <TableCell>
                                        Course Number
                                    </TableCell>
                                    <TableCell sortDirection="desc">
                                        <Tooltip
                                            enterDelay={300}
                                            title="Sort"
                                        >
                                            <TableSortLabel
                                                active
                                                direction="desc"
                                            >
                                                Average GPA
                                            </TableSortLabel>
                                        </Tooltip>
                                    </TableCell>
                                    <TableCell>
                                        Status
                                    </TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {orders.map((order) => (
                                    <TableRow
                                        hover
                                        key={order.id}
                                    >
                                        <TableCell>
                                            <p onClick={coursepage} className='cursor-pointer'>{order.courseName}</p>
                                        </TableCell>
                                        <TableCell>
                                            {order.courseNumber}
                                        </TableCell>
                                        <TableCell>
                                            {order.averageGPA}
                                        </TableCell>
                                        <TableCell>
                                            {order.status}
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </Box>
                </PerfectScrollbar>
                <Box
                    sx={{
                        display: 'flex',
                        justifyContent: 'space-evenly',
                        p: 2
                    }}
                    className='w-full justify-center' 
                >
                    <PaginationButtons />
                </Box>
            </Card>
        </div>
    )
}

export default SearchResults;