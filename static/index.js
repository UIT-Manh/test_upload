window.onload = () => {
    $('#sendbutton').click(() => {
        const formData = new FormData();
        const input = $(`input[name=image1]`)[0];
        if (input.files && input.files[0]) {
            formData.append('file', input.files[0]);
        }
        // Hiển thị thông tin trong console cho mục đích debug
        for (const value of formData.values()) {
            console.log('haha',value);
        }

        $.ajax({
            url: "http://localhost:5000/chart-data", // Update this to your backend endpoint
            type: "POST",
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            error: function (data) {
                console.log("upload error", data);
                console.log(data.getAllResponseHeaders());
            },
            success: function(data) {
                $('#filecsv').empty();
                data['images'].forEach((imageData, index) => {
                    if (index < 1) {  
                        let bytestring = imageData['status'];
                        let image = bytestring.split('\'')[1]; // Extract the base64 string
                        let imageElement = $('<csv>', {
                            src: 'data:image/jpeg;base64,' + image,
                            class: 'processed-image'
                        });

                        // Append to the corresponding image box
                        $('#box').append(imageElement);
                    }
                });
            }
        });
    });
};