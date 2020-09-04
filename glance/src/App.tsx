import React from 'react';
import './App.css';
import Fab from '@material-ui/core/Fab';
import { Item, ItemProps } from './components/Item';
import InputAdornment from '@material-ui/core/InputAdornment';
import TextField from '@material-ui/core/TextField';
import SearchIcon from '@material-ui/icons/Search';
import { ThemeProvider } from '@material-ui/styles';
import { createMuiTheme } from '@material-ui/core/styles';
import { Typography } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import axios from 'axios';

const theme = createMuiTheme({
  typography: {
    fontFamily: 'Roboto Mono'
  }
});

const useStyles = makeStyles({
  searchContainer: {
    display: 'flex',
    marginTop: 25,
    flexDirection: 'row'
  },
  defaultSearchBar: {
    marginTop: 25,
    width: '100%'
  },
  resultsSearchBar: {
    width: '50%'
  },
  defaultSearchButton: {
    boxShadow: 'none',
    marginTop: 10
  },
  resultsSearchButton: {
    boxShadow: 'none',
    marginLeft: 15
  },
  results: {
    marginTop: 25
  },
  item: {
    marginTop: 15
  }
});

enum Status {
  Main,
  Results
};

const App: React.FC = () => {
  const classes = useStyles();

  const [status, setStatus] = React.useState<Status>(Status.Main);
  const [snippet, setSnippet] = React.useState<string>('');
  const [error, setError] = React.useState<boolean>(false);
  const [helperText, setHelperText] = React.useState<string>('');
  const [results, setResults] = React.useState<ItemProps[]>([]);

  const handleSnippetChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSnippet(event.target.value);
  };

  const handleSearch = () => {
    if (snippet) {
      if (validateRegex(snippet)) {
        setStatus(Status.Results);
        setError(false);
        setHelperText('');

        axios.get(`https://glance3.azurewebsites.net/regex/.*${snippet}.*`).then(({data}) => {
          setResults(data);
        })
      } else {
        setError(true);
        setHelperText('Incorrect Regular Expression');
      }
    }
  };

  const validateRegex = (text: string) => {
    let isValid = true;
    try {
      new RegExp(text);
    } catch(e) {
      isValid = false;
    }

    return isValid;
  };

  return (
    <ThemeProvider theme={theme}>
      {status === Status.Results && 
        <div className="Results">
          <div className={classes.searchContainer}>
            <TextField
                className={classes.resultsSearchBar}
                label="Code Snippet"
                InputProps={{
                    startAdornment: <InputAdornment position="start">&lt;&gt;</InputAdornment>,
                }}
                variant="outlined"
                defaultValue={snippet}
                onChange={handleSnippetChange}
            />
            <Fab className={classes.resultsSearchButton} variant="extended" onClick={handleSearch}> 
              <SearchIcon />
              Search
            </Fab>
          </div>
          <Typography className={classes.results} variant="h4" component="h2">Results</Typography>
          <Typography variant="body1">{results.length === 0 ? 'No Results ' : results.length} Found</Typography>
          {results.map((item) => 
            <Item
              repo_name={item.repo_name}
              username={item.username}
              avatar={item.username[0].toUpperCase()}
              filename={item.filename}
              file_link={item.file_link}
              snippet={item.snippet}
              language={item.language}
              repo_link={item.repo_link}/>
          )}
        </div>
      }
      {status === Status.Main &&
        <div className="Landing">
          <Typography variant='h1'>Glance</Typography>       
          <TextField
              error={error}
              className={classes.defaultSearchBar}
              label="Code Snippet"
              InputProps={{
                  startAdornment: <InputAdornment position="start">&lt;&gt;</InputAdornment>,
              }}
              variant="outlined"
              helperText={helperText}
              onChange={handleSnippetChange}
          />
          <Fab className={classes.defaultSearchButton} variant="extended" onClick={handleSearch}> 
            <SearchIcon />
            Search
          </Fab>
        </div>          
      }
    </ThemeProvider>
  );
}

export default App;
