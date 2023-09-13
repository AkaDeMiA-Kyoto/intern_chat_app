const buttons = document.getElementById("button");

function resize() {
    /* 文字数が少なくなったときのため、フォントサイズを戻せるようにします。
    他にstyleの属性があればfont-sizeに関するところを除いてstyleに上書きしましょう。
    今回はないのでstyle属性ごと削除します。*/
    textElem.removeAttribute('style');
    console.log(textElem.getBoundingClientRect().height , textElem.scrollHeight);
    for (
      let size = 30;
      textElem.getBoundingClientRect().height　< textElem.scrollHeight && size > 10;
      size -= 3
      /* 文字がはみ出すサイズが存在していたので、1ずつ減らすのを3ずつ減らすという少し速いペースでフォントサイズを小さくしてみました。
      こちらには正解不正解はなく、場合によって調整して遊んでみてください。*/
    ) {
      textElem.style.fontSize = size + "px";
      // textElem.setAttribute("style", `font-size: ${size}px`); // こちらも可能
    }

//ウインドウサイズを変えたとき
window.addEventListener('resize', () => {
    resize();
  });