# Glance
Enter a regex expression and find semantically similar code snippets from popular OSS projects.

## What it does
Given any regular expression it searches for snippets of code which match it and gives links to the full code. It also matches synonims and similar-meaning words (using ML algorithms) to names entered in the regular expression. This way it ensures that it will display code which matches what you want.

## Work-flow
1. A frontend application takes a regex expression which is spellchecked. 
2. A word2vec model generates embeddings for the words in the regex expression. 
3. The embeddings are used to generate a regex that includes semantically similar expressions. 
4. The altered regular expression is then sent to a cluster of Elastic search nodes hosted on the Azure cloud which searches for matches among popular OSS repositories previously loaded onto the cluster. 
5. The best matches are then displayed according to their similarity score.

## Screens

### Starting screen 
Enter a regular expression to search for:
![start](https://github.com/avaspataru/hackcambridge101/blob/master/screens/start_screen.JPG)

### Results screen for regex
Displays results that match your search: 
![search](https://github.com/avaspataru/hackcambridge101/blob/master/screens/regex_search_screen.JPG)

### Results screen for function definitions
Displays results which match the intent behind your function definition:
![func](https://github.com/avaspataru/hackcambridge101/blob/master/screens/func_search_screen.JPG)


## Technologies 
* React (frontend)
* Bing Spell Check API from Azure Cognitive Services (spellchecking)
* Python (word embeddings) 
* Elastic Search (fast searching through code) 
* Azure Cloud (hosting) 
