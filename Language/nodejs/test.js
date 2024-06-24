async function test() {
    return "hello world!"
}

async function main() {
    var data = await test();
    console.log(data);// hello world!
}
main()
console.log(test())// Promise { 'hello world!' }

