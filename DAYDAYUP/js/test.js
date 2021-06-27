let daan = document.getElementsByClassName('wenzi')
let a = document.getElementsByTagName('textarea')
let count = 0;
for (let i = 0; i < daan.length; i += 2) {
  try {
    a[count].value = daan[i].innerHTML.trim().split('暂无')[0].split('  ')[0];
    count += 1;
  } catch (e) {
    console.log(e)

  }
}
//首页单选
document.getElementsByClassName('wenzi')[0].innerText.replace('\n', '').trim()

//单选
a = document.getElementsByClassName('right')
daan = document.querySelectorAll('div > div > div > dl > dd')

for (let i = 0; i < a.length; i++) {

  if (a[i].innerHTML === 'A') {
    daan[i * 4].setAttribute('class', 'cho-this')
  } else if (a[i].innerHTML === 'B') {
    daan[i * 4 + 1].setAttribute('class', 'cho-this')
  } else if (a[i].innerHTML === 'C') {
    daan[i * 4 + 2].setAttribute('class', 'cho-this')
  } else if (a[i].innerHTML === 'D') {
    daan[i * 4 + 3].setAttribute('class', 'cho-this')
  }
}
