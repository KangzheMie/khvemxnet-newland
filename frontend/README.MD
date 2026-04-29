# NewLand Frontend

A simple and neet frontend for NewLand project.

the frontend css is based on [neet.css](https://github.com/codazoda/neatcss). it is prity cool.

## Installation

### Requirements

you should add [KaTeX](https://github.com/KaTeX/KaTeX) and [marked](https://github.com/markedjs/marked) to your project. using below command:

``` sh
npm install
```
the [highlight](https://github.com/highlightjs/highlight.js) is a static file, and it is already included.

### Usage

1. css
if you want to change css, you can add your css into the `./_lib/custom.css`.

2. javascript
the `./_lib/sectionLoad.js` includes the function to fetch section from api or local file.  
before you use the api, you should set your api url in the `./_lib/sectionLoad.js`.
the api is based on [NewLand backend](https://github.com/KangzheMie/khvemxnet-newland-backend).

3. local file
you can add local pages in the `./_pages` directory.


