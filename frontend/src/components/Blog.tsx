import * as React from 'react'
import { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader'; 
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import axios from 'axios';

export default function OutlinedCard() {
  const [data, setData] = useState([]); 

  useEffect(() => {
    axios.get('http://0.0.0.0:8000/blog/read')
      .then(response => {
        setData(response.data); 
      })
  }, []); 


  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-GB', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
    });
  };

  return (
    <Box sx={{ 
      display: 'flex',
      justifyContent: 'space-between',
      padding: 2, 
      width: '1000',
      backgroundColor: "white"
    }}>
      {data.map((item) => (
        <Card key={item.id} variant="outlined" sx={{ 
          width: 500, 
          backgroundColor: 'grey.200', 
          border: '2px solid', 
          borderColor: 'primary.main', 
          boxShadow: 5,
          margin: 2, 
        }}>
          <CardHeader 
            title={item.tittle}
            subheader={formatDate(item.created_at)}
            sx={{
              color: 'white', 
              backgroundColor: 'primary.main', 
            }}
          />
          <CardContent>
            <Typography variant="body4">
              {item.information} 
            </Typography>
          </CardContent>
          <CardActions>
            <Button size="small">Learn More</Button>
          </CardActions>
        </Card>
      ))}
    </Box>
  );
}