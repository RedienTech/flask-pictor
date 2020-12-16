$(document).ready(function () {
    
    $(document).on("change", "#file", function(){
        console.log(this.files)
        var files = this.files
        var supportedFormats = ["image/png", "image/jpeg"]
        var element
        for (var i = 0; i < files.length; i++){
            element = files[i]
            if (supportedFormats.indexOf(element.type) != -1){
                createPreview(element)
            } else {
                alert("Se han subido archivos con extensiones invalidas")
            }
        }
    })

})