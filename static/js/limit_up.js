$(document).ready(function(){
    $("#renderPdf").click(function(){
          html2canvas(document.body, {
              onrendered:function(canvas) {
                var imgData = canvas.toDataURL();
                var canWidth = canvas.width;
                var canHeight = canvas.height;
                console.log(canWidth, canHeight);

                var pageData = canvas.toDataURL('image/jpeg', 1.0);

                //方向默认竖直，尺寸ponits，格式a4【595.28,841.89]
                var pdf = new jsPDF('', 'pt', 'a4');
                //需要dataUrl格式
                pdf.addImage(pageData, 'JPEG', 0, 0, canvas.width, canvas.height);
                pdf.save('content.pdf');
              }
          })
    })
})
