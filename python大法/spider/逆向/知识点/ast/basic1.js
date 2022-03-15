//https://astexplorer.net/    网站查看ast
import {parse} from "@babel/parser"
import generate from "@babel/generator"
import fs from "fs";

const code =fs.readFileSync('demo.js','utf-8');
let ast=parse(code);  //转换成ast对象
const {code:output}=generate(ast); //把AST对象转换成代码
console.log(output);