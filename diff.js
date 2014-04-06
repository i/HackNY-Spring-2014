function hashDiff(a, b) {
  var diff = 0;
  for (var i = 0; i < a.length && i < b.length; i++) {
    x = atoi(a[i]);
    y = atoi(b[i]);
    diff += Math.min(
        Math.abs(Math.min(x,y) + 16 - Math.max(x,y)),
        Math.abs(x - y));
  }
  return diff;
}

function atoi(c) {
  return parseInt('0x' + c);
}

console.log(hashDiff(process.argv[2], process.argv[3]));
