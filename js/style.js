fetch(
  "https://github.com/tsuzukihashi/tsuzukihashi.github.io/blob/master/header.html"
)
  .then((response) => response.text())
  .then((data) => (document.querySelector("#header").innerHTML = data));

fetch(
  "https://github.com/tsuzukihashi/tsuzukihashi.github.io/blob/master/footer.html"
)
  .then((response) => response.text())
  .then((data) => (document.querySelector("#footer").innerHTML = data));

$(function () {
  $("#open").show();
  $("#close").hide();
  // アイコンをクリック
  $("#open").click(function () {
    // ulメニューを開閉する
    $("#navi").slideToggle();
    $("#open").hide();
    $("#close").show();
  });

  // アイコンをクリック
  $("#close").click(function () {
    // ulメニューを開閉する
    $("#navi").slideToggle();
    $("#open").show();
    $("#close").hide();
  });
});

$(function () {
  var topBtn = $("#pagetop");
  topBtn.hide();
  //スクロールが300に達したらボタン表示
  $(window).scroll(function () {
    if ($(this).scrollTop() > 300) {
      topBtn.fadeIn();
    } else {
      topBtn.fadeOut();
    }
  });
  //スクロールでトップへもどる
  topBtn.click(function () {
    $("body,html").animate(
      {
        scrollTop: 0,
      },
      500
    );
    return false;
  });
});
