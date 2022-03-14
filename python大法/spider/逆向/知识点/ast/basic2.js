import {parse} from "@babel/parser"
import traverse from "@babel/traverse"  //遍历所有节点
import fs from "fs";

const code =fs.readFileSync('demo.js','utf-8');
let ast=parse(code);
traverse(ast,{enter(path){
  console.log(path);
  }})