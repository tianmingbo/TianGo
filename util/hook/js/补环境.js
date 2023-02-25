window = {};

function myProxy(obj) {
  return new Proxy(obj, {
    set(target, p, value, receiver) {
      console.log("set:", target, p, value);
      return Reflect.set(...arguments)
    },
    get(target, p, receiver) {
      console.log("get:", target, p);
      return target[p];
    }
  })
}

window = myProxy(window);

window.location = 1
console.log(window.location)