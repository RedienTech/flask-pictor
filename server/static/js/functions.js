function createPreview(file) {
    var imgUrl = URL.createObjectURL(file)
    $("#preview").attr("src", imgUrl)
}