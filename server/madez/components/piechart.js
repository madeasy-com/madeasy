import { Doughnut } from 'react-chartjs-2';
import {Chart, ArcElement} from 'chart.js'
Chart.register(ArcElement);
import { Box, Card, CardContent, CardHeader, Divider, Typography, useTheme } from '@mui/material';
import SentimentDissatisfiedIcon from '@mui/icons-material/SentimentDissatisfied';
import SentimentSatisfiedIcon from '@mui/icons-material/SentimentSatisfied';
import InsertEmoticonIcon from '@mui/icons-material/InsertEmoticon';
import MoodBadIcon from '@mui/icons-material/MoodBad';

export default function Piechart(){
  const theme = useTheme();

  const data = {
    datasets: [
      {
        data: [34,12,15,22,13,4],
        backgroundColor: ['#05ff1e','#2a590a', '#eef20f', '#f2b20f', '#bd5608','#ff0d05'],
        borderWidth: 8,
        borderColor: '#FFFFFF',
        hoverBorderColor: '#FFFFFF'
      }
    ],
    labels: ['A', 'AB', 'B', 'BC', 'C','D/F']
  };

  const options = {
    animation: false,
    cutoutPercentage: 80,
    layout: { padding: 0 },
    legend: {
      display: false
    },
    maintainAspectRatio: false,
    responsive: true,
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

  const devices = [
    {
      title: 'A',
      value: 34,
      icon: InsertEmoticonIcon,
      color: '#05ff1e'
    },
    {
      title: 'AB',
      value: 12,
      icon: SentimentSatisfiedIcon,
      color: '#2a590a'
    },
    {
      title: 'B',
      value: 15,
      icon: SentimentSatisfiedIcon,
      color: '#eef20f'
    },
    {
        title: 'BC',
        value: 22,
        icon: SentimentDissatisfiedIcon,
        color: '#f2b20f'
    },
    {
        title: 'C',
        value: 13,
        icon: SentimentDissatisfiedIcon,
        color: '#bd5608'
    },
    {
        title: 'D/F',
        value: 4,
        icon: MoodBadIcon,
        color: '#ff0d05'
    },
  ];

  return (
    <Card >
      <CardHeader title="Grade Distribution" />
      <Divider />
      <CardContent>
        <Box
          sx={{
            height: 300,
            position: 'sticky'
          }}
        >
          <Doughnut
            data={data}
            options={options}
          />
        </Box>
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
            pt: 2
          }}
        >
          {devices.map(({
            color,
            icon: Icon,
            title,
            value
          }) => (
            <Box
              key={title}
              sx={{
                p: 1,
                textAlign: 'center'
              }}
            >
              <Icon color="action" />
              <Typography
                color="textPrimary"
                variant="body1"
              >
                {title}
              </Typography>
              <Typography
                style={{ color }}
                variant="h4"
              >
                {value}
                %
              </Typography>
            </Box>
          ))}
        </Box>
      </CardContent>
    </Card>
  );
};