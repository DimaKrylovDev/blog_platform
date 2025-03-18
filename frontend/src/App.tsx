import * as React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import OutlinedCard from './components/Blog';
import  Header  from './components/Header'
import SignInDialog from './components/Login';

const theme = createTheme({
  cssVariables: false,
});

function App() {
  return( 
  <ThemeProvider theme={theme}>
    <Header />
    <OutlinedCard />
    <SignInDialog />
  </ThemeProvider>
  )
}

export default App
