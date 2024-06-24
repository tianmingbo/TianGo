debugger;
window = new Proxy(window, {
  set(obj, prop, value) {
    console.log('set', obj, prop, value);
    return Reflect.set(...arguments);
  },
  get: function (target, property, receiver) {
    console.log('get', target, property, receiver);
    return target[property];
  }
})

window.tian = '666';