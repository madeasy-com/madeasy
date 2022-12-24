import { Bar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
  } from 'chart.js';
  ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
  );
  import { Box, Card, CardContent, CardHeader, Divider, useTheme } from '@mui/material';

export default function Barchart(){
  const theme = useTheme();

  const data = {
    datasets: [
      {
        backgroundColor: '#3F51B5',
        barPercentage: 0.5,
        barThickness: 7,
        borderRadius: 4,
        categoryPercentage: 0.5,
        data: [2.43, 2.51, 2.63, 2.37, 2.14, 2.88, 2.94, 2.44],
        label: 'Thomas Brunold',
        maxBarThickness: 10
      },
      {
        backgroundColor: '#ff0d05',
        barPercentage: 0.5,
        barThickness: 7,
        borderRadius: 4,
        categoryPercentage: 0.5,
        data: [2.53, 2.14, 2.73, 2.53, 2.78, 2.32, 2.40, 2.31],
        label: 'Liana B.Lamont',
        maxBarThickness: 10
      },
      {
        backgroundColor: '#f2b20f',
        barPercentage: 0.5,
        barThickness: 7,
        borderRadius: 4,
        categoryPercentage: 0.5,
        data: [2.96, 2.51, 2.95, 2.01, 2.24, 2.16, 2.85, 2.24],
        label: 'Overall',
        maxBarThickness: 10
      }
    ],
    labels: ['Fall 2019', 'Spring 2020', 'Fall 2020','Spring 2021', 'Fall 2021', 'Spring 2021', 'Fall 2021', 'Spring 2021']
  };

  const options = {
    animation: false,
    cornerRadius: 20,
    layout: { padding: 0 },
    legend: { display: false },
    maintainAspectRatio: false,
    responsive: true,
    xAxes: [
      {
        ticks: {
          fontColor: theme.palette.text.secondary
        },
        gridLines: {
          display: false,
          drawBorder: false
        }
      }
    ],
    yAxes: [
      {
        ticks: {
          fontColor: theme.palette.text.secondary,
          beginAtZero: true,
          min: 0
        },
        gridLines: {
          borderDash: [2],
          borderDashOffset: [2],
          color: theme.palette.divider,
          drawBorder: false,
          zeroLineBorderDash: [2],
          zeroLineBorderDashOffset: [2],
          zeroLineColor: theme.palette.divider
        }
      }
    ],
    tooltips: {
      backgroundColor: theme.palette.background.paper,
      bodyFontColor: theme.palette.text.secondary,
      borderColor: theme.palette.divider,
      borderWidth: 1,
      enabled: true,
      footerFontColor: theme.palette.text.secondary,
      intersect: false,
      mode: 'index',
      titleFontColor: theme.palette.text.primary
    }
  };

  return (
    <Card sx={{
        width: 1050,
        position: 'relative'
      }}>
      <CardHeader title="GPA per instructor "/>
      <Divider />
      <CardContent>
        <Box
          sx={{
            height: 400,
            position: 'relative'
          }}
          className='cursor-pointer'
        >
          <Bar
            data={data}
            options={options}
          />
        </Box>
      </CardContent>
    </Card>
  );
};