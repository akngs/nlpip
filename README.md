# nlpip - A natural language based unix pipeline utility

`nlpip` takes a text written in natural language as input, and performs a
specified command also written in natural language, and then outputs the result
in natural language.

Here's a demo:

<img width="600" src="https://github.com/akngs/nlpip/raw/main/nlpip.svg" alt="screen recording">

## Installation

First, you need to install `nlpip` using `pip`:

    pip install nlpip

Then, set your OpenAI's API key as an environment variable:

    export OPENAI_API_KEY=WRITE_YOUR_KEY_HERE

Default model is `gpt-3.5-turbo`. If you want to use a different model, you can set it as an
environment variable. For example, if you want to use `gpt-4` model, you can run:

    export OPENAI_MODEL=gpt-4

## How to use

`nlpip` or just `nlp` for short, provides following default commands:

- `keywords`: Extract keywords from input text
- `poem`: Write poem using input text
- `summarize`: Summarize input text
- `sentiment`: Analyze sentiment of input text

For example, if you want summarize `input.txt` and turn it into a poem, you can
run the following command:

    cat input.txt | nlp summarize | nlp poem

## How to create a new command

To create a new command, you just need to create a text file containing the
command in natural language. For example, if you want to create a command that
translates input text into French, you can create a file named
`~/.nlpip/prompts/fr.txt` in with:

    Translate into French

Then, you can run the following command:

    echo Hello | nlp fr

And you will get the following output:

    Bonjour

You may override default commands by creating a file with the same name in
`~/.nlpip/prompts/`.

## Credit

- `nlpip` is inspired by
  [Schillace Laws of Semantic AI](https://learn.microsoft.com/en-us/semantic-kernel/howto/schillacelaws).
