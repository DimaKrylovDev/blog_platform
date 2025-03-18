import * as React from 'react'
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import axios from 'axios';
import Box from '@mui/material/Box';



interface TabPanelProps {
    children?: React.ReactNode;
    index: number;
    value: number;
  }
  
  function CustomTabPanel(props: TabPanelProps) {
    const { children, value, index, ...other } = props;
  
    return (
      <div
        role="tabpanel"
        hidden={value !== index}
        id={`simple-tabpanel-${index}`}
        aria-labelledby={`simple-tab-${index}`}
        {...other}
      >
        {value === index && <Box sx={{ p: 1 }}>{children}</Box>}
      </div>
    );
  }
  
  function a11yProps(index: number) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }
  
export default function SignInDialog() {
    
    const email = React.useRef('')
    const password = React.useRef('')

    const[userState, setState] = React.useState(false)
    
    const [value, setValue] = React.useState(0);

    const handleChange = (event: React.SyntheticEvent, newValue: number) => {
        setValue(newValue);
      };


    const userLogin = () => {
        setState(true);
    }

    const[open, setOpen] = React.useState(false);

    const handleClickOpen = () => {
        setOpen(true);
    };
    const handleClickClose = () => {
        setOpen(false)
    };

    const handleLogin = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const formData = new FormData(event.currentTarget);
        const formJson = Object.fromEntries((formData as any).entries());
        console.log(formJson)
        try {
          await axios.post('http://0.0.0.0:8000/auth/login', formJson);
          handleClickClose();
        } catch (error) {
          console.error('Login failed:', error);
        }
      };

    const handleRegister = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const formData = new FormData(event.currentTarget);
        const formJson = Object.fromEntries((formData as any).entries());
        console.log(formJson)
        try {
          await axios.post('http://0.0.0.0:8000/auth/login', formJson);
          handleClickClose();
        } catch (error) {
          console.error('Login failed:', error);
        }
      };

    return (
        <>
            <Button variant='outlined' onClick={handleClickOpen} style={{position: 'absolute', top: '20px', right: '30px'}}>
                Sign In
            </Button>
            <Dialog
                open={open}
                onClose={handleClickClose}
                component="form"
            >
            <Box sx={{ width: '3000'}}>
              <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                <Tabs value={value} onChange={handleChange} aria-label="basic tabs example">
                  <Tab label="Login" {...a11yProps(0)} />
                  <Tab label="Registration" {...a11yProps(1)} />
                </Tabs>
              </Box>
              <CustomTabPanel value={value} index={0}>
              <DialogTitle variant="h4">Log In</DialogTitle>
                <DialogContent>
                    <TextField
                        autoFocus
                        required
                        id="email"
                        name="email"
                        label="Email Address"
                        type="email"
                        fullWidth
                        variant="standard"
                        inputRef={email}
                    />
                    <TextField
                        autoFocus
                        required
                        id="id"
                        name="password"
                        label="password"
                        type="password"
                        fullWidth
                        variant="standard"
                        inputRef={password}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={userLogin} type='submit'>Sign In</Button>
                </DialogActions>
              </CustomTabPanel>
              <CustomTabPanel value={value} index={1}>
              <DialogTitle variant='h4'>Registration</DialogTitle>
              <DialogContent>
                    <TextField
                        autoFocus
                        required
                        name="name"
                        label="Username"
                        type="name"
                        fullWidth
                        variant="standard"
                    />
                    <TextField
                        autoFocus
                        required
                        name="email"
                        label="Email Address"
                        type="email"
                        fullWidth
                        variant="standard"
                    
                    />
                    <TextField
                        autoFocus
                        required
                        name="password"
                        label="password"
                        type="password"
                        fullWidth
                        variant="standard"
                    />
                </DialogContent>
                <DialogActions>
                    <Button type='submit'>Create Account</Button>
                </DialogActions>
              </CustomTabPanel>
            </Box>
            </Dialog>
        </>
    )
}


