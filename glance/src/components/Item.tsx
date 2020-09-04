import * as React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Typography } from '@material-ui/core';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Chip from '@material-ui/core/Chip';
import SyntaxHighlighter from 'react-syntax-highlighter';

const useStyles = makeStyles({
    card: {
        width: '75%',
        marginTop: 15
    },
    owner: {
        display: 'flex',
        alignItems: 'center',
        marginBottom: 15,
        marginTop: 10
    },
    ownerName: {
        marginLeft: 10
    },
    code: {
        marginTop: 25
    }
  });

export type ItemProps = {
    repo_name: string;
    file_link?: string;
    username: string;
    avatar?: string;
    filename: string;
    snippet: string;
    language: string;
    repo_link: string;
};

export const Item: React.FunctionComponent<ItemProps> = (props: ItemProps) => {
    const classes = useStyles();

    return (
        <Card className={classes.card} variant="outlined">
            <CardContent>
                <Typography variant="h5" component="h2">
                    {props.repo_name}
                </Typography>
                <div className={classes.owner}>
                    <Avatar>{props.avatar}</Avatar>
                    <Typography className={classes.ownerName} variant="h6" component="h3">
                        {props.username}
                    </Typography>
                </div>
                <a href={props.file_link}>
                    <Typography>
                        {props.filename}
                    </Typography>
                </a>
                <SyntaxHighlighter className={classes.code} language="javascript" showLineNumbers={true}>
                    {props.snippet}
                </SyntaxHighlighter>
                <Chip label={props.language}/>
            </CardContent>
            <CardActions>
                <Button href={props.repo_link} size="small">Go To Repo</Button>
            </CardActions>
      </Card>
    );
}